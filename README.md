# 加强版 B2B 线索清洗与背调

一个用于 Codex 的可复用技能，将海关线索清洗与一般 B2B 客户背调整合到同一条可审计流程中。

支持海关 XLSX/CSV、客户名单、公司名称/网址、询盘/RFQ、截图及已有 CRM 记录。默认完成企业身份核实、经营与采购能力研究、联系方式补全、独立评级，再生成 Zoho 导入 Excel 或严格 CRM JSON。

> 本仓库是技能指令与辅助脚本，不是一键自动获客软件。背调需要 Codex 的搜索/浏览工具；实际 CRM 查询需要可用连接器。生成文件不会自动导入 Zoho，生成文案不会自动发送。

## 安装

### 仅在一个项目中使用

在目标项目根目录执行：

```bash
mkdir -p .agents/skills
git clone https://github.com/chnwh168-sketch/b2b-lead-cleaning-research-pro.git .agents/skills/b2b-lead-cleaning-research-pro
```

### 个人技能目录

```bash
git clone https://github.com/chnwh168-sketch/b2b-lead-cleaning-research-pro.git ~/.codex/skills/b2b-lead-cleaning-research-pro
```

同名目录已存在时先核对其来源与本地修改，再更新；不要覆盖未备份的自定义版本。若技能尚未出现在可用列表，可重新打开项目或启动新的会话。

## 快速使用

### 海关表批量清洗

```text
使用 $b2b-lead-cleaning-research-pro 清洗并背调这份海关表。
目标产品：剪叉式升降平台。
目标市场：表格中的进口国。
P1 示例：明确写有 scissor lift 或经确认的目标机型。
P2 示例：只写 aerial work platform，机型不足以确认。
P3 示例：疑似相邻的其他升降设备。
P4 示例：明确为叉车等非目标产品。
请先确认本批次分类规则，保留所有来源行和公司映射，输出到 outputs/scissor-lift/。
暂不消耗邮箱验证额度。
```

P1–P4 必须按实际产品线定义；上述只是示例，不应直接套用到其他产品。未授权付费验证时，可以完成清洗背调并交付无邮箱草稿、候选邮箱审计和待完成说明。

### 单条公司或询盘背调

```text
使用 $b2b-lead-cleaning-research-pro 背调以下公司/询盘：……
我们的产品是……，已有沟通记录是……。
请确认主体、经营状态、采购与渠道能力，寻找业务联系方式，说明客户价值、风险与下一步。
```

### 严格 JSON 输出

```text
使用 $b2b-lead-cleaning-research-pro 背调这些线索，最终仅输出符合 CRM 合约的 JSON 数组。
保留输入顺序，证据账本和输入输出 ID 映射另存。
```

默认使用 references/crm-contract.md 的字段与枚举。若实际 Zoho 自定义字段不同，请提供字段 API 名称及允许值，先确定适配 profile，不要直接导入未经适配的 JSON。

### 仅整理或拟跟进文案

```text
使用 $b2b-lead-cleaning-research-pro，只整理、不背调：规范这份名单并标记重复与未知，不联网。
```

```text
使用 $b2b-lead-cleaning-research-pro，根据这份询盘和已发生的沟通拟一条英文回复，推进到确认型号与数量。
```

仅整理不会伪造新评分、研究或验证结果；拟稿不会自动发送。

## 工作流程

1. 盘点来源文件、字段、行数和哈希，给每行建立稳定 Source_Row_ID。
2. 海关入口逐交易分类，只提取实际进口商/买方/收货人；一般询盘入口保留原文、产品需求和沟通历史。
3. 保守去重，分开维护公司和联系人，冻结 Company_ID 和来源映射。
4. 研究身份、当前经营、采购进口与渠道能力，对重点及冲突记录定向复核。
5. 从已闭合身份的公开来源补全联系方式，逐字段保存证据。
6. 分别判断产品匹配、业务关系、客户价值、当前优先级、已发生销售阶段和 CRM 纳入决策。
7. 完整研究后，对最终去重邮箱执行同一批最终验证并核对完整报告。
8. 导出、逐 ID 对账、检查工作簿并交付；待复核、阻断和未完成验证均明确标注。

无官网、无邮箱、低优先级不自动排除可信买方。名称相似不自动合并；共享邮箱/电话不自动证明同一法律实体。公开搜索无结果不等于没有进口或企业停业。

## 三份 Excel 交付

| 文件 | 收录规则 |
| --- | --- |
| 01_Zoho上传_带已验证邮箱_项目名.xlsx | Include 且主邮箱通过最终任务 good/ok |
| 02_Zoho上传_不带邮箱_项目名.xlsx | Include 但没有可用 Good 主邮箱 |
| 03_待复核及未进入Zoho候选_项目名.xlsx | Manual Review、Exclude 或合并从记录，保留原因/映射 |

三表互斥，其 Company_ID 并集必须精确等于冻结 ID 集合。待复核不代表确认无价值。零候选邮箱不调用付费服务，第一表保留空表结构。JSON-only 模式不强制生成 Excel。

## 邮箱验证与脚本

Python 3.9+；表格校验需安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

MillionVerifier 辅助脚本需要 Node.js 20+。先准备只含 email 表头的一列 CSV（去重、正确归属），默认 dry-run：

```bash
node scripts/millionverifier_bulk.mjs --csv work/final_email_candidates.csv --work-dir work/millionverifier
```

实际验证仅在用户授权消耗额度且本机环境变量 MILLIONVERIFIER_API_KEY 已配置后，在以上命令添加 `--execute`。密钥只在运行时读取，不写入提示词、代码、表格或 Git。服务 API 路径及列名应在真实执行前核对官方文档；本仓库尚未做在线服务兼容性测试。

上传结果不明时停止核对服务任务，禁止盲目重复上传；同工作目录仅可恢复相同候选哈希。默认 Email 与 Secondary_Email 都只接受最终同任务 good/ok，其他状态留审计。公开发布的邮箱不自动证明可以投递。

```bash
python3 scripts/reconcile_email_reports.py \
  --candidates work/final_email_candidates.csv \
  --full work/millionverifier/millionverifier_full_report.csv \
  --good work/millionverifier/millionverifier_good_only.csv

python3 scripts/validate_three_workbooks.py \
  --with-email outputs/01.xlsx \
  --without-email outputs/02.xlsx \
  --not-candidate outputs/03.xlsx \
  --frozen-ids work/frozen_company_ids.json \
  --good-only-csv work/millionverifier/millionverifier_good_only.csv

python3 scripts/validate_crm_json.py work/leads.json
```

冻结 ID 文件是唯一非空字符串数组，例如 `["C001", "C002"]`。主表须包含 Company_ID、Email、CRM Eligibility；Secondary_Email 可选。第二及第三表两个邮箱字段都留空。Full Report 列名不同时传 `--status-column` / `--quality-column`。零邮箱生成仅 email 表头的空 Good CSV，跳过无报告的服务对账。

校验脚本不能替代身份真实性检查、证据审核、公式检查和工作簿视觉检查。默认不允许多个公司共享同一导出邮箱；若业务确需允许，应明确分配政策并调整验证器，不能绕过报错。

## 文件结构

- SKILL.md：入口、模式和核心约束。
- agents/openai.yaml：技能显示信息。
- references/：流程、证据、评分、CRM 字段、联系规则、邮箱协议和交付规则。
- scripts/：本地校验、邮箱报告对账和可选付费验证助手。

## 验证范围与数据保护

本地已检查14个模拟情景（三表分区8个、CRM类型校验3个、邮箱报告对账3个）、脚本语法和参考链接；未调用真实 Zoho 或付费邮箱服务。官方 skill quick_validate 所需 PyYAML 在当时环境中缺失，因此采用独立结构检查，不能视为该工具通过。

只提交技能代码和说明。原始客户名单、海关数据、背调结果、验证报告和 CRM 导出放在被忽略的 inputs/、work/、outputs/ 中。实际导入、发信、购买额度或订阅需要用户相应授权；公开联系人不等于订阅同意。

## 来源与许可

合并自用户提供的 customs-lead-cleaning-zoho 与 b2b-lead-research-crm 技能。前者继承代码的 MIT 声明保留在 LICENSE；该声明不代表后者素材另获一份可确认的 MIT 授权。对外再分发第二份源技能的素材时，应确认原作者许可。
