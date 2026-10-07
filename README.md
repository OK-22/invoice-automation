# Invoice-to-ERP Automation Bot

> Validates 200 invoices against purchase orders in 4 seconds and catches all 26 injected errors with 0 false positives (synthetic data).

An RPA bot built in UiPath Studio that reads invoice PDFs, checks them against a purchase order master file, and routes problem invoices to an exceptions queue with a stated reason. Python is used to generate the test data and score the bot's results.

## Define

Accounts payable staff typically open each invoice, retype the invoice number, PO number, and total into the ERP, and check them against the purchase order. This is slow and error-prone, and mismatches (wrong totals, unknown or missing POs, duplicate invoices) are often caught late.

Goal: automatically validate invoices against PO data, post the clean ones, and send exceptions to a human for review.

Scope: 200 synthetic invoices (PDF) checked against a 150-row PO master file. 26 invoices (13%) contain a deliberate error, and an answer key records which ones, so the bot's catch rate can be measured exactly.

## Measure

The bot's performance is measured against a known answer key:

- Time to process all 200 invoices
- Errors caught correctly, by type
- False positives (clean invoices wrongly flagged)

## Analyze

Four error types were injected into the data:

| Error type | Count |
|---|---|
| Missing PO number | 5 |
| Unknown PO (not in master file) | 9 |
| Amount mismatch | 8 |
| Duplicate invoice number | 4 |
| **Total** | **26** |

## Improve

The workflow in `uipath/Main.xaml` does the following for each invoice:

1. Reads the PDF text and extracts the invoice number, PO number, and total using regular expressions.
2. Looks up the PO in `po_master.csv` and compares the invoice total with the PO amount (tolerance of one cent).
3. Keeps a running list of invoice numbers already seen, to catch duplicates.
4. Writes clean invoices to `output/posted.csv`, and everything else to `output/exceptions.csv` with a reason code (`missing_po`, `unknown_po`, `amount_mismatch`, `duplicate`).

## Control

- Every invoice gets exactly one outcome: posted, or exception with a reason.
- `compare.py` scores the exceptions file against `answer_key.csv` and reports caught errors, misses, and false positives.
- The rules are deterministic, so results are repeatable on every run.

## Results

| Metric | Result |
|---|---|
| Invoices processed | 200 |
| Total run time | 4 seconds (about 0.02 seconds per invoice) |
| Errors caught correctly | 26 of 26 |
| Missed errors | 0 |
| False positives | 0 |

## Repository contents

- `generate_data.py`: creates the 200 invoice PDFs, `po_master.csv`, and `answer_key.csv` (fixed random seed, so the data is reproducible)
- `uipath/`: the UiPath Studio project
- `output/`: `posted.csv` and `exceptions.csv` from the latest run
- `compare.py`: scores the bot's exceptions against the answer key

## How to run it

1. Install the Python libraries: `pip install faker reportlab`
2. Generate the data: `python generate_data.py`
3. Open the `uipath` folder in UiPath Studio (Community Edition is free) and run `Main.xaml`
4. Score the results: `python compare.py`

Note: file paths in `Main.xaml` are hardcoded to the author's machine. Update the paths for `po_master.csv`, `invoices`, and `output` before running.

## Limitations and next steps

- The data is synthetic and the rules are deterministic, so a perfect score is expected here. The value is in showing the full workflow: extraction, validation, exception routing, and measurement.
- Real invoices would need OCR for scanned documents, handling of varied layouts, and human review of edge cases.
- Next steps: replace the CSV files with a real ERP or database connection, and add a manual-review step for exceptions.
