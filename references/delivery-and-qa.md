# Three-workbook delivery and QA

## Partition

Create exactly three mutually exclusive files:

1. `01_Zoho上传_带已验证邮箱_<project>.xlsx`
   - `CRM Eligibility = Include`;
   - one master company per row;
   - `Email` contains only a final-task `good/ok` address.
2. `02_Zoho上传_不带邮箱_<project>.xlsx`
   - remaining `CRM Eligibility = Include` companies;
   - `Email` is blank, including Catch-all, Unknown, invalid, disposable, unverified, and no-email cases.
3. `03_待复核及未进入Zoho候选_<project>.xlsx`
   - `CRM Eligibility = Exclude` or `Manual Review`;
   - confirmed non-match, logistics intermediary, false match, or duplicate source ID mapped into a master;
   - includes an explicit reason and source/master ID mapping.

Do not put a company in the third file merely because it has no website or contact information when customs product evidence remains credible.

## Reconciliation

Assert all of the following:

```text
with_good_email + without_good_email + not_candidate = final_frozen_company_count
```

- Company_ID is unique within each file.
- No Company_ID overlaps between files.
- The three-file union exactly equals the final frozen company set.
- Every source Company_ID appears either as a master row or in the alias/duplicate mapping.
- The Good-email workbook contains no email absent from the final task's Good-only set.
- The no-email and non-candidate workbooks have a blank user-facing Email field.
- Catch-all, Unknown, invalid, disposable, and unverified emails do not appear in user-facing Email fields.

Run [scripts/validate_three_workbooks.py](../scripts/validate_three_workbooks.py) as an additional partition check.

## Workbook quality

Each workbook should include:

- a clearly named main data sheet;
- a compact `清洗汇总` sheet showing source counts, frozen counts, alias merges, final partition, MillionVerifier task ID, status counts, and PASS/FAIL formulas;
- filters, frozen header rows, readable widths, wrapped long text, consistent date/number formats, and no broken formulas;
- the alias mapping in the third workbook or an audit sheet when duplicates were merged.

Inspect formulas for `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, and `#N/A`. Render and visually review every sheet, including the empty-state third workbook.

## Delivery

1. Validate all three local files.
2. Copy them to the user-specified destination.
3. Verify each source/destination SHA-256 pair.
4. Keep working audits by default.
5. Delete local copies only when explicitly requested and only after external integrity is confirmed.
6. Never delete the external original or external final files.

Do not upload Zoho during this workflow. The output is for manual review and import unless the user separately authorizes a live CRM operation.

## Strengthened mandatory checks
冻结集合以 frozen_company_ids.json 为准，不仅核总数。运行验证器须传 --frozen-ids 和 --good-only-csv（零候选传仅有 email 表头的空报告）。按当前冻结版本核对。主表含 CRM Eligibility 和 Company_ID；Email、Secondary_Email 两字段在第二及第三表均为空，非 Good 地址仅留 work/ 审计。
个人 JSON 无主邮箱但有 Good Secondary_Email 时，批量公司主表可选同主体 Good 公司邮箱作 Email；保留分配映射，不复制个人 JSON 的空主邮箱逻辑。
共享 Good 邮箱默认只分配一个公司主记录，其他公司的邮箱留审计并标 shared-email，除非用户明确允许。
空表仍有主数据表头和清洗汇总；摘要应区分交易行、冻结实体、主记录、合并从记录、联系人和 Pending/Blocked。未完成研究或待邮箱授权时标草稿，不称全量完成。
源行和别名映射可放独立审计文件，用户三表是冻结 ID 的完整分区。工作簿渲染/公式检查与该验证器是不同检查，不可互相代替。
