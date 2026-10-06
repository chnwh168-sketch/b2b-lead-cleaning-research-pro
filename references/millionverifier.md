# MillionVerifier final-task protocol

## When to run

Run MillionVerifier only after:

1. the frozen company set has been fully researched;
2. contact enrichment is complete for the batch;
3. company duplicates are resolved or mapped;
4. email syntax, attribution, role suitability, and exact-email deduplication are complete;
5. the company-to-email mapping is saved.

Do not combine results from earlier, partial, or unrelated tasks.

## Candidate snapshot

Create an email-only CSV with header `email`. Save:

- candidate count;
- exact SHA-256;
- creation timestamp;
- company-to-email mapping count;
- number of companies represented.

If the candidate file changes, create a new task. Do not reuse a task created from a different hash.

## Authorization and secret handling

- Require explicit user authorization before consuming credits.
- Read the API key from `MILLIONVERIFIER_API_KEY` at runtime.
- Never hard-code the key, print it, commit it, place it in a workbook, or save it in task manifests.
- Do not purchase credits or subscriptions.

The bundled helper is dry-run by default:

```bash
node scripts/millionverifier_bulk.mjs \
  --csv work/final_email_candidates.csv \
  --work-dir work/millionverifier
```

After authorization:

```bash
export MILLIONVERIFIER_API_KEY="..."
node scripts/millionverifier_bulk.mjs \
  --csv work/final_email_candidates.csv \
  --work-dir work/millionverifier \
  --execute
```

The helper resumes the same task from its work directory. A different candidate hash is rejected.

## Final status mapping

- `ok` / quality `good`: eligible for the final Zoho `Email` field.
- `catch_all`: keep only in audit; user-facing `Email` stays blank.
- `unknown`: keep only in audit; user-facing `Email` stays blank.
- `invalid` / `bad`: keep only in audit; user-facing `Email` stays blank.
- `disposable`: keep only in audit; user-facing `Email` stays blank.
- unfinished, no result, or missing from the Full Report: treat as unverified and leave blank.

Do not describe `found` as `deliverable`. Deliverability is supported only by the final same-task result.

## Required task evidence

Retain in the working audit:

- task/upload response and task ID;
- latest task status;
- Good-only report;
- Full Report;
- candidate CSV hash;
- report hashes;
- completion timestamp;
- exact set reconciliation between candidates and Full Report;
- selected Good email per company, including shared-email allocation rules.

When multiple companies share one Good email, assign it to only one CRM master record unless the user's deduplication policy explicitly allows duplicate emails.

## Retry, empty set and reconciliation
零邮箱跳过 API，状态 Skipped-No Candidates，任务 ID 空；生成仅 email 表头的空 Good CSV 供本地检查。无付费授权时可完成清洗背调和无邮箱草稿，报告验证待完成。
上传 POST 不能自动重试；网络超时或结果不明时写 upload_attempt.json 阻止重复上传。先通过官方任务界面/支持确认是否已创建，确认未创建后方可显式清除阻断再重试；不得根据未找到本地响应直接重传。
完成后解析 CSV，以精确邮箱集合核对 candidates == Full Report 的集合；检查重复行、遗漏、额外地址、结果状态及 Good-only 与 Full Report good/ok 一致。任一不符不得用于严格邮箱导出。报告哈希不能替代此集合校验。
当前 API 路径和返回字段是继承实现，执行前核查官方文档；本地验证不是在线 API 成功证明。

执行本地集合检查：
```bash
python3 scripts/reconcile_email_reports.py --candidates work/final_email_candidates.csv --full work/millionverifier/millionverifier_full_report.csv --good work/millionverifier/millionverifier_good_only.csv
```
服务字段不同则传 --status-column / --quality-column；不能以未知列名猜测状态。零候选无完整报告时跳过此项并记 Skipped-No Candidates。
