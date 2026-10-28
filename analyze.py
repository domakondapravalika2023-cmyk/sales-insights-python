"""Analyze one-product orders using only Python's standard library."""
import argparse
import json
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_orders(path):
    rows = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(rows, list) or not rows:
        raise ValueError('Input must be a nonempty JSON list of orders.')
    seen = set()
    for index, row in enumerate(rows, 1):
        try:
            if not isinstance(row, dict):
                raise ValueError('order must be an object')
            for key in ('order_id', 'date', 'product', 'region'):
                if not isinstance(row.get(key), str) or not row[key].strip():
                    raise ValueError(f'{key} must be a nonempty string')
            date.fromisoformat(row['date'])
            if row['order_id'] in seen:
                raise ValueError('duplicate order_id')
            seen.add(row['order_id'])
            if type(row.get('quantity')) is not int or row['quantity'] <= 0:
                raise ValueError('quantity must be a positive integer')
            price = Decimal(str(row['unit_price']))
            if not price.is_finite() or price < 0 or price != price.quantize(Decimal('0.01')):
                raise ValueError('unit_price must be nonnegative with at most 2 decimal places')
            row['revenue'] = price * row['quantity']
        except (KeyError, ValueError, InvalidOperation) as exc:
            raise ValueError(f'Invalid order at row {index}: {exc}') from exc
    return rows


def summarize(rows):
    groups = {key: defaultdict(Decimal) for key in ('month', 'product', 'region')}
    for row in rows:
        for key in groups:
            label = row['date'][:7] if key == 'month' else row[key]
            groups[key][label] += row['revenue']
    total = sum((row['revenue'] for row in rows), Decimal(0))
    return total, groups


def report(rows):
    total, groups = summarize(rows)
    lines = ['# Sales Insights Report', '', 'Synthetic demo data; amounts in USD.', '',
             f'- Orders: {len(rows):,}',
             f'- Units sold: {sum(row["quantity"] for row in rows):,}',
             f'- Revenue: ${total:,.2f}',
             f'- Average order value: ${total / len(rows):,.2f}', '']
    for key, values in groups.items():
        lines += [f'## Revenue by {key}', '', '| Segment | Revenue (USD) |', '| --- | ---: |']
        entries = sorted(values.items()) if key == 'month' else sorted(values.items(), key=lambda pair: (-pair[1], pair[0]))
        for label, amount in entries:
            label = label.replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')
            lines.append(f'| {label} | ${amount:,.2f} |')
        lines.append('')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'data/orders.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'reports/summary.md')
    args = parser.parse_args()
    try:
        result = report(load_orders(args.input))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding='utf-8')
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Error: {exc}\n')
    print(result)
    print(f'\nSaved to {args.output}')


if __name__ == '__main__':
    main()
