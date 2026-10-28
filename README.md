# Sales Insights — Python Analytics Project

A beginner-friendly command-line project that turns order data into a business summary. It demonstrates JSON ingestion, validation, financial calculations, aggregation, automated tests, and Markdown reporting. Built with Python's standard library; no packages or API keys required.

## Business questions

- How much revenue was earned, and what was the average order value?
- Which products and regions generated the most revenue?
- How does revenue vary by month?

## Quick start

Install Python 3.10 or newer, extract this folder, and open a terminal inside it.

```bash
python3 analyze.py
python3 -m unittest -v
```

On Windows, use `python` instead of `python3` if needed. Open `reports/summary.md` to see the generated report. A pre-generated example is included so you can view results directly on GitHub.

Custom paths:

```bash
python3 analyze.py --input data/orders.json --output reports/my-report.md
```

## Files

- `analyze.py`: validation, aggregation, and report generation.
- `data/orders.json`: 240 synthetic orders across January–June 2026.
- `reports/summary.md`: output generated from the included data.
- `test_analyze.py`: checks exact monetary totals, grouping, and rejection of invalid data.

## Data format

Each order has a unique `order_id`, an ISO date (`YYYY-MM-DD`), `product`, `region`, positive integer `quantity`, and nonnegative `unit_price` with up to two decimal places. Prices are stored as strings and calculated with Decimal to avoid binary floating-point rounding errors.

```json
{"order_id":"ORD-0001","date":"2026-01-10","product":"Notebook","region":"East","quantity":3,"unit_price":"8.50"}
```

## Metric definitions and limits

Revenue = quantity × unit price. Average order value = revenue ÷ number of orders. Each row represents a complete, single-product order. This simplified dataset does not model discounts, tax, returns, costs, multiple currencies, or multiple items per order. Revenue is not profit. Invalid data stops processing with an error instead of being silently skipped.

All sample data is fictional, generated for learning. Results are descriptive and do not establish causes or predict future sales.

## Make it your own

1. Run the script and explain one result from each table.
2. Add category-level analysis or a date filter.
3. Add tests for the behavior you introduce.
4. Document your changes and what you learned before using the project in interviews.

This starting project was prepared with AI assistance. Customize it and describe your own contributions accurately.

## Upload to GitHub

Extract the ZIP first. Create a repository named `sales-insights-python`, then upload the contents of this folder so `README.md` and `analyze.py` are at the repository root. Commit the files. Upload the extracted files rather than just the ZIP, so visitors can read the code and report.
