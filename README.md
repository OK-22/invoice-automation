# invoice-automation



\# Invoice-to-ERP Automation Bot



RPA bot that validates invoices against purchase orders and routes exceptions for review. Built with UiPath and Python on synthetic data.



\## Define

Accounts payable staff manually open each invoice, retype the invoice number, PO number, and total into the ERP, and check them against the purchase order. This is slow and error-prone, and mismatches (wrong totals, unknown or missing POs, duplicate invoices) are often caught late.



Goal: automatically validate invoices against PO data, post the clean ones, and route exceptions to a human for review.



Scope: 200 synthetic invoices (PDF) checked against a 150-row PO master file. About 15% of invoices contain a deliberate error, and an answer key records which ones, so the bot's catch rate can be measured.



\## Measure

(Add your manual baseline here after you time yourself.)

