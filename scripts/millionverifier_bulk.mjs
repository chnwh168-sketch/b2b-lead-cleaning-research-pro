#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

function option(name) {
  const index = process.argv.indexOf(name);
  return index >= 0 ? process.argv[index + 1] : "";
}

const csvArg = option("--csv");
const workArg = option("--work-dir");
const execute = process.argv.includes("--execute");

if (!csvArg || !workArg) {
  console.error("Usage: node millionverifier_bulk.mjs --csv <email-only.csv> --work-dir <audit-dir> [--execute]");
  process.exit(2);
}

const csvPath = path.resolve(csvArg);
const workDir = path.resolve(workArg);
const key = process.env.MILLIONVERIFIER_API_KEY ?? "";
const csvBytes = await fs.readFile(csvPath);
const csvText = csvBytes.toString("utf8").replace(/^\uFEFF/, "");
const lines = csvText.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);

function oneCsvField(line) {
  if (line.startsWith('"') && line.endsWith('"')) return line.slice(1, -1).replace(/""/g, '"').trim();
  return line.trim();
}

if (!lines.length || oneCsvField(lines[0]).toLowerCase() !== "email") {
  throw new Error("Candidate CSV must be email-only with header: email");
}

const rawEmails = lines.slice(1).map(oneCsvField).map((value) => value.toLowerCase());
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!rawEmails.length) throw new Error("Candidate CSV has no email rows.");
if (rawEmails.some((email) => !emailPattern.test(email))) throw new Error("Candidate CSV contains an invalid email format.");
const emails = [...new Set(rawEmails)];
if (emails.length !== rawEmails.length) throw new Error("Candidate CSV contains duplicate emails; deduplicate before verification.");

const sha256 = crypto.createHash("sha256").update(csvBytes).digest("hex");
await fs.mkdir(workDir, { recursive: true });
const snapshotPath = path.join(workDir, "millionverifier_candidate_snapshot.json");

let priorSnapshot = null;
try {
  priorSnapshot = JSON.parse(await fs.readFile(snapshotPath, "utf8"));
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
}
if (priorSnapshot && priorSnapshot.candidateCsvSha256 !== sha256) {
  throw new Error("This work directory belongs to a different candidate CSV hash. Use a new work directory for a changed candidate set.");
}

const snapshot = {
  candidateCsv: csvPath,
  candidateCount: emails.length,
  candidateCsvSha256: sha256,
  createdAt: priorSnapshot?.createdAt ?? new Date().toISOString(),
};
await fs.writeFile(snapshotPath, JSON.stringify(snapshot, null, 2));

if (!execute) {
  console.log(JSON.stringify({ mode: "dry-run", ...snapshot }, null, 2));
  process.exit(0);
}
if (!key) throw new Error("MILLIONVERIFIER_API_KEY is not set.");

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function fetchRetry(url, options = {}, attempts = 5) {
  let lastError;
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 Chrome/140 Safari/537.36",
          Accept: "application/json,text/csv,*/*",
          ...(options.headers ?? {}),
        },
        signal: AbortSignal.timeout(120000),
      });
      if (response.ok) return response;
      const body = await response.text();
      throw new Error(`HTTP ${response.status}: ${body.slice(0, 500)}`);
    } catch (error) {
      lastError = error;
      if (attempt < attempts) await wait(1500 * attempt);
    }
  }
  throw lastError;
}

async function getJson(apiPath, params) {
  const url = new URL(`https://bulkapi.millionverifier.com${apiPath}`);
  url.searchParams.set("key", key);
  for (const [name, value] of Object.entries(params)) url.searchParams.set(name, String(value));
  return (await fetchRetry(url)).json();
}

const uploadPath = path.join(workDir, "millionverifier_upload_response.json");
let upload;
try {
  upload = JSON.parse(await fs.readFile(uploadPath, "utf8"));
  if (!upload.file_id) throw new Error("Missing file_id");
  console.log(`Resuming MillionVerifier task ${upload.file_id}; no new upload was created.`);
} catch (error) {
  if (error?.code !== "ENOENT" && error?.message !== "Missing file_id") throw error;
  const attemptPath = path.join(workDir, "millionverifier_upload_attempt.json");
  try {
    await fs.access(attemptPath);
    throw new Error("Prior upload outcome needs reconciliation; do not automatically upload again. Check provider tasks before clearing attempt marker.");
  } catch (checkError) {
    if (checkError?.code !== "ENOENT") throw checkError;
  }
  const creditsUrl = new URL("https://api.millionverifier.com/api/v3/credits");
  creditsUrl.searchParams.set("api", key);
  const credits = await (await fetchRetry(creditsUrl)).json();
  await fs.writeFile(path.join(workDir, "millionverifier_credits_before.json"), JSON.stringify({ ...credits, checkedAt: new Date().toISOString() }, null, 2));
  const available = Number(credits.bulk_credits ?? credits.credits ?? 0);
  if (available < emails.length) throw new Error(`Insufficient MillionVerifier credits: ${available} available, ${emails.length} required.`);

  const form = new FormData();
  form.append("file_contents", new Blob([csvBytes], { type: "text/csv" }), path.basename(csvPath));
  const uploadUrl = new URL("https://bulkapi.millionverifier.com/bulkapi/v2/upload");
  uploadUrl.searchParams.set("key", key);
  await fs.writeFile(attemptPath, JSON.stringify({ candidateCsvSha256: sha256, attemptedAt: new Date().toISOString() }, null, 2));
  upload = await (await fetchRetry(uploadUrl, { method: "POST", body: form }, 1)).json();
  if (!upload.file_id || upload.error) throw new Error(`MillionVerifier upload failed: ${JSON.stringify(upload)}`);
  await fs.writeFile(uploadPath, JSON.stringify(upload, null, 2));
  console.log(`Created MillionVerifier task ${upload.file_id} for ${emails.length} unique emails.`);
}

let info;
for (let poll = 1; poll <= 120; poll += 1) {
  info = await getJson("/bulkapi/v2/fileinfo", { file_id: upload.file_id });
  await fs.writeFile(path.join(workDir, "millionverifier_fileinfo_latest.json"), JSON.stringify({ ...info, polledAt: new Date().toISOString() }, null, 2));
  console.log(`Task ${upload.file_id}: ${info.status} ${info.percent ?? 0}% (${info.verified ?? 0}/${info.unique_emails ?? emails.length})`);
  if (info.status === "finished") break;
  if (["error", "canceled"].includes(info.status)) throw new Error(`MillionVerifier task ended with ${info.status}: ${info.error ?? ""}`);
  if (poll === 120) throw new Error("MillionVerifier polling timed out; rerun with the same work directory to resume the same task.");
  await wait(15000);
}

async function download(filter, filename) {
  const url = new URL("https://bulkapi.millionverifier.com/bulkapi/v2/download");
  url.searchParams.set("key", key);
  url.searchParams.set("file_id", upload.file_id);
  url.searchParams.set("filter", filter);
  const response = await fetchRetry(url);
  const bytes = Buffer.from(await response.arrayBuffer());
  if (/json/i.test(response.headers.get("content-type") ?? "")) {
    throw new Error(`Download returned JSON: ${bytes.toString("utf8").slice(0, 500)}`);
  }
  await fs.writeFile(path.join(workDir, filename), bytes);
  return {
    filename,
    bytes: bytes.length,
    sha256: crypto.createHash("sha256").update(bytes).digest("hex"),
  };
}

const goodOnly = await download("ok", "millionverifier_good_only.csv");
const fullReport = await download("all", "millionverifier_full_report.csv");
const manifest = {
  taskId: String(upload.file_id),
  candidateCount: emails.length,
  candidateCsvSha256: sha256,
  completedAt: new Date().toISOString(),
  taskSummary: info,
  reports: { goodOnly, fullReport },
};
await fs.writeFile(path.join(workDir, "millionverifier_manifest.json"), JSON.stringify(manifest, null, 2));
console.log(JSON.stringify(manifest, null, 2));
