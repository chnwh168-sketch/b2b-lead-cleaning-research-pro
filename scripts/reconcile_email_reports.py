#!/usr/bin/env python3
"""Reconcile same-task reports locally; does not call a paid API."""
import argparse
import csv
import json
from pathlib import Path


def read(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        headers = {str(k).strip().lower(): k for k in (reader.fieldnames or [])}
        if 'email' not in headers:
            raise ValueError(f'{path}: missing email header')
        rows = list(reader)
    emails = [str(row.get(headers['email']) or '').strip().lower() for row in rows]
    if any(not v for v in emails) or len(emails) != len(set(emails)):
        raise ValueError(f'{path}: blank or duplicate emails')
    return set(emails), rows, headers


def reconcile(candidates, full, good, status_column='result', quality_column='quality'):
    c, _, _ = read(candidates)
    f, rows, headers = read(full)
    g, _, _ = read(good)
    errors = []
    if c != f:
        errors.append('candidate/full mismatch: missing='+str(sorted(c-f))+' extra='+str(sorted(f-c)))
    if status_column not in headers and quality_column not in headers:
        raise ValueError('Full Report needs explicit result/quality columns; pass actual provider column names')
    expected = set()
    for row in rows:
        status = str(row.get(headers.get(status_column)) or '').strip().lower()
        quality = str(row.get(headers.get(quality_column)) or '').strip().lower()
        if status in {'catch_all', 'catch-all', 'unknown', 'invalid', 'bad', 'disposable'} or quality in {'bad', 'unknown', 'disposable'}:
            continue
        if status == 'ok' or quality == 'good':
            expected.add(str(row[headers['email']]).strip().lower())
    if g != expected:
        errors.append('Good-only/full status mismatch')
    return {'passed': not errors, 'candidate_count': len(c), 'full_count': len(f), 'good_count': len(g), 'errors': errors}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidates', required=True)
    p.add_argument('--full', required=True)
    p.add_argument('--good', required=True)
    p.add_argument('--status-column', default='result')
    p.add_argument('--quality-column', default='quality')
    a = p.parse_args()
    try:
        report = reconcile(a.candidates, a.full, a.good, a.status_column.lower(), a.quality_column.lower())
    except (ValueError, OSError) as e:
        report = {'passed': False, 'errors': [str(e)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['passed'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
