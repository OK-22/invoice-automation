import csv, random
from pathlib import Path
from faker import Faker
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

fake = Faker(); random.seed(42)
Path("invoices").mkdir(exist_ok=True)

pos = [{"po_number": f"PO-{10000+i}", "vendor": fake.company(),
        "amount": round(random.uniform(200, 9000), 2)} for i in range(1, 151)]
with open("po_master.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["po_number", "vendor", "amount"])
    w.writeheader(); w.writerows(pos)

key = []
for n in range(1, 201):
    po = random.choice(pos)
    inv_no, po_num, total, error = f"INV-{5000+n}", po["po_number"], po["amount"], ""
    r = random.random()
    if r < 0.05:   total = round(total * random.uniform(1.05, 1.3), 2); error = "amount_mismatch"
    elif r < 0.09: po_num = "PO-99999"; error = "unknown_po"
    elif r < 0.12: po_num = ""; error = "missing_po"
    elif r < 0.15 and n > 1: inv_no = key[-1]["invoice"]; error = "duplicate"
    c = canvas.Canvas(f"invoices/invoice_{n:03}.pdf", pagesize=letter)
    c.drawString(72, 720, f"Invoice No: {inv_no}")
    c.drawString(72, 700, f"Vendor: {po['vendor']}")
    if po_num: c.drawString(72, 680, f"PO Number: {po_num}")
    c.drawString(72, 660, f"Total: ${total:.2f}")
    c.save()
    key.append({"file": f"invoice_{n:03}.pdf", "invoice": inv_no, "error": error})

with open("answer_key.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "invoice", "error"])
    w.writeheader(); w.writerows(key)