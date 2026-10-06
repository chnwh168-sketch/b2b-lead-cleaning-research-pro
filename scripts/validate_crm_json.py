#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

KEYS = [
    "Lead_Name", "Company", "Email", "Secondary_Email", "Phone", "Whatsapp",
    "WeChat", "Country", "Website", "X_Profile", "Facebook_Profile",
    "Instagram_Profile", "LinkedIn_Profile", "YouTube_Channel",
    "Interested_Products", "Interest_Categories", "Negotiation_Stage",
    "Match_Grade", "Lead_Tag", "Customer_Type", "Lead_Source", "Description"
]

NEGOTIATION_STAGE = {
    "-None-", "快速回复询盘", "背景调查", "发送目录册", "发送公司资料",
    "初步沟通客户意向需求", "明确客户需求", "发送报价单", "确定型号数量", "发送 PI"
}

INTEREST_CATEGORIES = {
    "钢筋机械", "路面机械", "混凝土机械", "压实机械", "地坪机械", "小型工程机械",
    "高空作业设备", "仓储设备", "清洁设备", "环卫设备", "电动工程车辆",
    "农业市政设备", "工业通风设备", "其他设备"
}

CUSTOMER_TYPE = {
    "-None-", "设备制造商", "工程设备经销租赁", "批发商", "承包商", "清洁设备经销租赁",
    "仓储设备经销租赁", "零售商", "工程施工承包商", "个体用户", "清洁服务承包商",
    "保洁公司", "工业品供应商", "生产制造企业", "仓储物流企业", "市政公共渠道",
    "其他相关企业", "不相关企业", "未确认", "其他行业进口商", "租赁公司", "其他行业"
}

LEAD_SOURCE = {
    "-None-", "阿里巴巴IDEAL", "阿里巴巴SWANTECH", "中国制造IDEAL", "中国制造GODWIN",
    "阿里巴巴I-RFQ", "阿里巴巴S-RFQ", "海关数据", "谷歌搜索", "转介绍", "微信",
    "网站hnmachines", "网站cngodwin", "网站hnideal", "X (Twitter)", "Facebook", "Instagram",
    "Linkedin", "展会", "AI搜索", "Facebook I推广", "Facebook G推广", "谷歌ADS I推广",
    "阿里巴巴IDEAL-新", "阿里巴巴IDEA新-RFQ", "中国制造IDEAL-LIFT", "来发信导入"
}

LEAD_TAG = {"-None-", "重点跟进", "一般跟进", "周跟进", "月跟进", "无需跟进"}
MATCH_GRADE = {"-None-", "A", "B", "C"}
EMAIL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
URL_RE = re.compile(r"^https?://[^\s]+$")
DESC_PREFIXES = ["事实：", "；推断：", "；未知：", "；客户价值：", "；风险：", "；下一步："]
FORBIDDEN_UNKNOWN = {"N/A", "Unknown", "None", "null", "待确认", "不知道"}
URL_FIELDS = (
    "Website", "X_Profile", "Facebook_Profile", "Instagram_Profile",
    "LinkedIn_Profile", "YouTube_Channel"
)


def load_data(path):
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return json.load(sys.stdin)


def validate_one(obj, label="object"):
    errors = []
    warnings = []
    if not isinstance(obj, dict):
        return [f"{label}: expected JSON object"], warnings

    if list(obj.keys()) != KEYS:
        errors.append(f"{label}: keys/order must exactly match schema")

    for key in KEYS:
        if key not in obj:
            continue
        if key == "Interest_Categories":
            if not isinstance(obj[key], list):
                errors.append(f"{label}.{key}: must be an array")
        elif not isinstance(obj[key], str):
            errors.append(f"{label}.{key}: must be a string")

    if any(key in obj and not isinstance(obj[key], list if key == "Interest_Categories" else str) for key in KEYS):
        return errors, warnings

    for key, value in obj.items():
        if isinstance(value, str) and value in FORBIDDEN_UNKNOWN:
            errors.append(f"{label}.{key}: use empty string or -None- instead of {value!r}")

    if obj.get("Negotiation_Stage") not in NEGOTIATION_STAGE:
        errors.append(f"{label}.Negotiation_Stage: invalid enum")
    if obj.get("Match_Grade") not in MATCH_GRADE:
        errors.append(f"{label}.Match_Grade: invalid enum")
    if obj.get("Lead_Tag") not in LEAD_TAG:
        errors.append(f"{label}.Lead_Tag: invalid enum")
    if obj.get("Customer_Type") not in CUSTOMER_TYPE:
        errors.append(f"{label}.Customer_Type: invalid enum")
    if obj.get("Lead_Source") not in LEAD_SOURCE:
        errors.append(f"{label}.Lead_Source: invalid enum")

    cats = obj.get("Interest_Categories", [])
    if isinstance(cats, list):
        bad = [x for x in cats if not isinstance(x, str) or x not in INTEREST_CATEGORIES]
        if bad:
            errors.append(f"{label}.Interest_Categories: invalid values {bad}")

    for field in ("Email", "Secondary_Email"):
        value = obj.get(field, "")
        if value and not EMAIL_RE.fullmatch(value):
            errors.append(f"{label}.{field}: must be one plain email address")
        if value and ("mailto:" in value.lower() or "[" in value or "](" in value):
            errors.append(f"{label}.{field}: must not contain Markdown or mailto")

    for field in URL_FIELDS:
        value = obj.get(field, "")
        if value and not URL_RE.fullmatch(value):
            errors.append(f"{label}.{field}: must be a plain http(s) URL")
        if value and ("utm_" in value.lower() or "[" in value or "](" in value):
            errors.append(f"{label}.{field}: contains tracking or Markdown")

    desc = obj.get("Description", "")
    if desc:
        positions = []
        for marker in DESC_PREFIXES:
            pos = desc.find(marker)
            if pos == -1:
                errors.append(f"{label}.Description: missing marker {marker}")
            positions.append(pos)
        if all(p >= 0 for p in positions) and positions != sorted(positions):
            errors.append(f"{label}.Description: markers are not in required order")
        if "utm_" in desc.lower() or "](" in desc or "http://" in desc or "https://" in desc:
            errors.append(f"{label}.Description: must not contain source/tracking URLs or Markdown")
        if len(desc) > 500:
            warnings.append(f"{label}.Description: {len(desc)} chars; target is about 400 Chinese chars")

    lead_name = obj.get("Lead_Name", "")
    company = obj.get("Company", "")
    if not lead_name and company:
        warnings.append(f"{label}.Lead_Name: company exists but lead name is blank; use verified person or natural brand + Team when appropriate")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate Zoho lead JSON against the B2B lead research CRM contract.")
    parser.add_argument("path", nargs="?", help="JSON file path; reads stdin when omitted")
    args = parser.parse_args()

    try:
        data = load_data(args.path)
    except Exception as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 2

    objects = data if isinstance(data, list) else [data]
    errors = []
    warnings = []
    for idx, obj in enumerate(objects, start=1):
        obj_errors, obj_warnings = validate_one(obj, f"lead[{idx}]")
        errors.extend(obj_errors)
        warnings.extend(obj_warnings)

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"OK: {len(objects)} lead(s) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
