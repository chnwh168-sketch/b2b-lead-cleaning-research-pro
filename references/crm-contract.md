# Zoho CRM Output Contract

Use this exact object shape and key order. Never omit a key.

```json
{
  "Lead_Name": "",
  "Company": "",
  "Email": "",
  "Secondary_Email": "",
  "Phone": "",
  "Whatsapp": "",
  "WeChat": "",
  "Country": "中文国家名",
  "Website": "",
  "X_Profile": "",
  "Facebook_Profile": "",
  "Instagram_Profile": "",
  "LinkedIn_Profile": "",
  "YouTube_Channel": "",
  "Interested_Products": "",
  "Interest_Categories": [],
  "Negotiation_Stage": "-None-",
  "Match_Grade": "-None-",
  "Lead_Tag": "-None-",
  "Customer_Type": "-None-",
  "Lead_Source": "-None-",
  "Description": "事实：...；推断：...；未知：...；客户价值：...；风险：...；下一步：..."
}
```

## Null and formatting rules

- Unknown ordinary string: `""`.
- Unknown enum: `"-None-"`.
- Unknown categories: `[]`.
- Country must be in Chinese.
- Email fields: one plain email address only. No Markdown, name wrapper, `mailto:`, multiple emails, or guessed address.
- URL fields: full plain `http://` or `https://` URL only. No Markdown.
- Strip tracking parameters when a clean canonical URL exists.
- Never put citations, source URLs, search queries, Markdown, or research narration inside `Description`.
- `Description` should normally stay within about 400 Chinese characters; keep only decision-useful facts.

## Lead_Name

- Verified real person -> full name.
- No verified person -> natural public brand/company short name + `Team`.
- Strip legal suffixes and generic group words from the Team display name.
- Do not mechanically create acronyms.
- Examples: `CFK Creaciones Team`, `Nido Machineries Team`.

## Company

Prefer the currently verified legal/company identity. If the marketing brand and legal entity differ, use the entity that the sales lead actually belongs to and record the relationship/conflict in `Description`.

Do not replace a source company with a same-name or related company without strong cross-identification.

## Email / Secondary_Email

邮箱归属与投递状态分开。默认 strict-good 模式：两个字段都必须是本批次最终 MillionVerifier 任务 good/ok；其他地址保存在审计，不写 CRM 邮箱。
- 已核实个人工作邮箱优先 Email；Team 记录可用公司邮箱。
- 已核实个人但只有公司邮箱：Email 留空，公司邮箱放 Secondary_Email。
- 第二邮箱须独立归属同主体且符合相同投递门槛；不得与主邮箱相同。
- 用户明确要求保留其自供询盘邮箱时可选 source-preserving：只保留未被反证的自供地址，不把网上找到的未验证邮箱混入。投递状态与该策略写 sidecar/分析报告，不能称验证通过或放入“带已验证邮箱”文件。
- 不猜邮箱；只填写一个纯地址，不混来源链接。

## Phone / Whatsapp / WeChat

- `Phone` may contain multiple verified numbers separated by ` / ` when useful.
- `Whatsapp` may be filled only when explicitly verified by a WhatsApp chat, official WhatsApp button/number, `wa.me`, official social labeling, or a platform field that explicitly says WhatsApp.
- Never copy a mobile phone into `Whatsapp` merely because it is mobile.
- WeChat also requires explicit verification.

## Negotiation_Stage

Allowed values only:
- `-None-`
- `快速回复询盘`
- `背景调查`
- `发送目录册`
- `发送公司资料`
- `初步沟通客户意向需求`
- `明确客户需求`
- `发送报价单`
- `确定型号数量`
- `发送 PI`

Use the furthest stage that actually happened:
- fresh inbound inquiry -> `快速回复询盘`
- research only -> `背景调查`
- catalog already sent -> `发送目录册`
- company profile already sent -> `发送公司资料`
- initial needs discussed -> `初步沟通客户意向需求`
- specs/application/requirements clarified -> `明确客户需求`
- formal quotation sent -> `发送报价单`
- model + quantity confirmed -> `确定型号数量`
- PI sent -> `发送 PI`

Never move an existing CRM stage backward.

## Interest_Categories

Allowed values only:
- `钢筋机械`
- `路面机械`
- `混凝土机械`
- `压实机械`
- `地坪机械`
- `小型工程机械`
- `高空作业设备`
- `仓储设备`
- `清洁设备`
- `环卫设备`
- `电动工程车辆`
- `农业市政设备`
- `工业通风设备`
- `其他设备`

Useful mappings:
- mobile lighting tower -> `小型工程机械`
- forklift / pallet truck / stacker -> `仓储设备`
- scissor / boom lift -> `高空作业设备`
- scrubber / sweeper -> `清洁设备`
- garbage/sanitation vehicle -> `环卫设备`; add `电动工程车辆` when electric and commercially relevant
- industrial/tunnel ventilation -> `工业通风设备`
- road saw/asphalt cutting -> `路面机械`
- roller/plate compactor/rammer -> `压实机械`
- power trowel/laser screed/floor grinder -> usually `地坪机械`, add `混凝土机械` only when the actual use supports it

## Customer_Type

Allowed values only:
- `-None-`
- `设备制造商`
- `工程设备经销租赁`
- `批发商`
- `承包商`
- `清洁设备经销租赁`
- `仓储设备经销租赁`
- `零售商`
- `工程施工承包商`
- `个体用户`
- `清洁服务承包商`
- `保洁公司`
- `工业品供应商`
- `生产制造企业`
- `仓储物流企业`
- `市政公共渠道`
- `其他相关企业`
- `不相关企业`
- `未确认`
- `其他行业进口商`
- `租赁公司`
- `其他行业`

Use verified business evidence. Do not infer customer type only from the product purchased or a keyword.

## Lead_Source

Allowed values only:
- `-None-`
- `阿里巴巴IDEAL`
- `阿里巴巴SWANTECH`
- `中国制造IDEAL`
- `中国制造GODWIN`
- `阿里巴巴I-RFQ`
- `阿里巴巴S-RFQ`
- `海关数据`
- `谷歌搜索`
- `转介绍`
- `微信`
- `网站hnmachines`
- `网站cngodwin`
- `网站hnideal`
- `X (Twitter)`
- `Facebook`
- `Instagram`
- `Linkedin`
- `展会`
- `AI搜索`
- `Facebook I推广`
- `Facebook G推广`
- `谷歌ADS I推广`
- `阿里巴巴IDEAL-新`
- `阿里巴巴IDEA新-RFQ`
- `中国制造IDEAL-LIFT`
- `来发信导入`

Rules:
- `Lead_Source` is the original acquisition source, not the current chat channel or research source.
- Made-in-China screenshot -> use the evidenced account/source; platform alone does not establish IDEAL/GODWIN/LIFT. If uncertain, use `-None-`.
- `hnmachines.com` form with Google Ads parameters such as `gclid`, `gad_source`, `gad_campaignid`, `campaignid` -> `谷歌ADS I推广`.
- Direct `hnmachines.com` website form without ad evidence -> `网站hnmachines`.
- Apply the actual domain for `hnideal` and `cngodwin`.
- Internal forwarding by staff is not `转介绍`.
- A reply to a Zoho development email does not overwrite the original CRM source.
- WhatsApp labels, CRM tags, and internal notes do not prove lead source.
- Google used during due diligence does not make the lead source `谷歌搜索`.
- If the source is not reliably known, use `-None-`.

## Lead_Tag

Allowed values only:
- `-None-`
- `重点跟进`
- `一般跟进`
- `周跟进`
- `月跟进`
- `无需跟进`

Guidance:
- live high-intent inquiry / quote cycle / near-term A opportunity -> `重点跟进`
- A-value account without a current trigger -> `周跟进`
- ordinary B-value relevant lead -> usually `一般跟进`
- old or weak but still relevant -> `月跟进`
- irrelevant / permanently closed / no practical sales value -> `无需跟进`

## Match_Grade

Allowed values only: `-None-`, `A`, `B`, `C`.

Evaluate the customer, not merely the inquiry:
- product/business fit 50%
- procurement/channel ability 30%
- verified operating strength 20%

### A
Real entity + high fit + strong commercial foundation such as repeat imports, mature distribution/rental, China sourcing, stock/service capability, OEM/private label, stable project/fleet procurement, or organized purchasing.

### B
Real and relevant, but procurement/scale evidence is weaker; or one meaningful real project purchase; or a smaller/ordinary end user/contractor.

A company-unverified buyer may still be B only when the contact channel is real, purchase intent is explicit, and there is specific product/model/quantity/specification or another concrete buying action. Keep `Customer_Type` conservative and record identity risk.

### C
Weak fit, low value, peripheral/high-risk prospect, or direct competitor/manufacturer without demonstrated external-buy/OEM/line-gap opportunity.

### -None-
Identity/business is too weak to assess, or only shallow browsing/price inquiry exists.

Do not make a company A simply because it is large. Do not make a lead B/A simply because someone asked for a price.

## Interested_Products

Select 1–5 products using this priority:
1. explicit inquiry/RFQ product
2. verified recent imported/purchased product
3. current sold/rented product with a realistic second-supplier/OEM/price-band/line-gap opportunity
4. strong business-use fit

Do not copy the customer's whole catalog. Do not invent unsupported tonnage, size, power, or model numbers.

## Description

Use one compact Chinese paragraph in this exact logical order:

`事实：...；推断：...；未知：...；客户价值：...；风险：...；下一步：...`

Include only:
- verified identity/operating evidence
- verified contact status
- products/brands/projects/fleet/service/import signals that affect sales
- material corrections/conflicts
- why the grade/tag makes sense
- best next action

Do not include citations, URLs, search queries, UTM parameters, or verbose source narration.
