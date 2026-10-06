# 证据账本

保存在 work/，严格 CRM JSON 不新增审计字段；分析报告和 Excel 可显示来源链接。
每项证据保存 Evidence_ID、Company_ID、Contact_ID、field/claim、value、fact_type（Source Fact/Verified Fact/Inference/Conflict/Unknown）、source_type、exact URL或原文件行号、source_date、retrieved_at、identity_signals、confidence、limitations。
官方来源是较强来源，但不是自动 HIGH：必须闭合主体、内容实际支持结论，并评估时效。两个转载同一目录不是两个独立来源。网页摘要仅定位，正文可访问时以正文为证。
冲突记录原值、新值、证据 ID、resolved/unresolved/do_not_merge 和纠正原因；拒绝错配网址记 rejected URL/reason，禁止复用其联系方式。
联系方式分别存 ownership_confidence、role_suitability、deliverability_status、verification_task_id。公开联系人不等于订阅同意，Marketing Permission 默认 Unknown。
A 评级、大字段修正、合并、排除和恢复候选均需证据条目。负面结论需要有效证据；搜索无结果写“本次已查来源未发现可验证记录”，不写“不存在”。
运行清单保存源哈希、冻结版本、研究覆盖、阻断、候选邮箱哈希、任务及报告哈希、最终集合对账和检查结果。每个冻结 ID 都有研究状态或排除证据；审计路径不含密钥。
