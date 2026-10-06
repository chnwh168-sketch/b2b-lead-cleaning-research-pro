# Field schema

Use stable English field names for machine processing where practical; bilingual headers are acceptable in user-facing workbooks. Do not remove customs-value fields merely because Zoho lacks a matching field.

## Row-level trade audit

- `Source_Row_ID`
- `Original Excel Row`
- `Importer / Buyer / Consignee`
- `Exporter / Supplier`
- `Country`
- `Import Date`
- `HS Code`
- `Product Description Full`
- `Brand`
- `Model`
- `Quantity`
- `Weight`
- `Import Value`
- `Currency`
- `Product Match`
- `Product Type`
- `Product Match Reason`
- `Entered Next Stage`
- `Not Entered Reason`

## Frozen company master

- `Company_ID`
- `Company Standard Name`
- `Original Company Name Variants`
- `Country`
- `City`
- `Import Count`
- `First Import Date`
- `Latest Import Date`
- `Total Import Value`
- `Total Quantity`
- `Total Weight`
- `P1 Import Count`
- `P2 Import Count`
- `P3 Import Count`
- `P4 Import Count`
- `Product Match`
- `P2 Verification`
- `Product Type`
- `Product Description Summary`
- `Imported Brands`
- `Main Suppliers`
- `Supplier Count`
- `Source Row IDs`
- `Original Company_ID Mapping`

## Research and contact master

- `Website`
- `Website Status`
- `Company Type`
- `Main Business`
- `Application Industry`
- `Light/Target Product Related`
- `Construction Equipment Related`
- `Rental Related`
- `Security/Other Adjacent Industry Related`
- `General Email`
- `Contact Name`
- `Contact Title`
- `Personal Email`
- `Company Phone`
- `Mobile`
- `WhatsApp`
- `LinkedIn Company`
- `LinkedIn Contact`
- `Facebook`
- `Instagram`
- `X/Twitter`
- `Address`
- `匹配等级`
- `开发优先级`
- `背调结果`
- `建议`
- `Research Sources`
- `Contact Confidence`
- `Contact Status`
- `Manual Review Needed`
- `Duplicate Action`
- `Master Company_ID`
- `CRM Eligibility`
- `CRM Exclusion Reason`
- `Marketing Permission`

## Controlled values

`P2 Verification`: `P2-A`, `P2-B`, `P2-C`, `P2-D`.

`匹配等级`: keep the user's existing values; default to `A-直接匹配`, `B-相邻渠道`, `不匹配`, `无有效官网`.

`开发优先级`: `High`, `Medium`, `Low`.

`Contact Confidence`:

- `High`: official source and company identity confirmed;
- `Medium`: official social page or credible third party with strong identity closure;
- `Low`: directory-only or single-source contact.

`Contact Status`: `Ready to Contact`, `Partial Contact`, `No Contact Found`, `Manual Review`.

`Duplicate Action`: `Keep`, `Merge`, `Keep Separate`.

`CRM Eligibility`: `Include`, `Exclude`, `Manual Review`.

`Marketing Permission`: default `Unknown`. A public business contact is not automatically an opted-in Zoho Campaigns subscriber.

## Final Zoho-facing minimum columns

Keep at least:

- `Company_ID`, `Company`, `Country`, `City`, `Address`;
- `Website`, `Email`, `Phone`, `WhatsApp`;
- `Contact Name`, `Contact Title`, `LinkedIn`, `Facebook`;
- `匹配等级`, `开发优先级`, `背调结果`, `建议`;
- `Import Count`, `Latest Import Date`, `Total Import Value`, `Main Supplier`;
- `MillionVerifier Result`, `MillionVerifier Task ID`, `Research Sources`;
- `Marketing Permission`, `Duplicate Action`, `Master Company_ID`.

## Unified additions and scope
一般名单无交易数据时交易字段留空。公司表保持每 Company_ID 一行；联系人表保持每 Contact_ID 一行并关联公司；JSON sidecar 保留 Source_Row_ID/Company_ID/Contact_ID。
增加 Research Status、Research Timestamp、Entity Confidence、Evidence IDs、Business Match、Match_Grade、Lead_Tag、Lead_Source、Negotiation_Stage、Email Ownership Confidence、Email Deliverability Status、Email Policy、Frozen Version。
CRM 字段名称与枚举以 crm-contract.md 或用户实际提供的 profile 为准；不得自行覆盖实际 Zoho schema。联系人与公司字段分配见 crm-contract.md。
金额按币种、数量按单位汇总；Total Import Value 若不同币种无法换算则留空，另存分币种值；贸易统计仅代表输入数据覆盖。
CRM Eligibility=Manual Review 的记录放第三表待复核，明确不是确认非候选。Match_Grade C、Low、P2-C 不自动 Exclude。
