
import smtplib
from email.mime.text import MIMEText
import re
import pdfplumber
from datetime import datetime

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Mail sent Successfully")
    
    
    
# def parse_sold_invoice_pdf(pdf_file):
#     result = {
#         'invoice_number': None,
#         'sold_date': None,
#         'customer_name': None,
#         'customer_email': None,   # ← add this
#         'items': []
#     }

#     with pdfplumber.open(pdf_file) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()

#             # ── extract invoice number ─────────────────────────
#             if not result['invoice_number']:
#                 match = re.search(r'Invoice[:\s#]*([A-Z0-9\-]+)', text, re.IGNORECASE)
#                 if match:
#                     result['invoice_number'] = match.group(1).strip()

#             # ── extract date ───────────────────────────────────
#             if not result['sold_date']:
#                 match = re.search(r'Date\s*[:\-]?\s*(\d{2}/\d{2}/\d{2,4})', text, re.IGNORECASE)
#                 if match:
#                     date_str = match.group(1)
#                     try:
#                         if len(date_str.split('/')[-1]) == 2:
#                             result['sold_date'] = datetime.strptime(date_str, '%m/%d/%y').date()
#                         else:
#                             result['sold_date'] = datetime.strptime(date_str, '%m/%d/%Y').date()
#                     except ValueError:
#                         pass

#             # ── extract customer name ──────────────────────────
#             if not result['customer_name']:
#                 match = re.search(r'Sold To[:\s]*\n([^\n]+)', text, re.IGNORECASE)
#                 if match:
#                     result['customer_name'] = match.group(1).strip()

#             # ── extract customer email ─────────────────────────
#             if not result['customer_email']:
#                 match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
#                 if match:
#                     result['customer_email'] = match.group(0).strip()

#             # ── extract line items ─────────────────────────────
#             tables = page.extract_tables()
#             for table in tables:
#                 for row in table:
#                     if not row or len(row) < 4:
#                         continue
#                     first_cell = str(row[0]).strip() if row[0] else ''
#                     if first_cell.lower() in ['qty', 'quantity', '', 'none']:
#                         continue
#                     try:
#                         qty = float(re.sub(r'[^\d.]', '', str(row[0])))
#                         product_code = str(row[1]).strip() if row[1] else None
#                         unit_price_str = str(row[-2]).strip() if row[-2] else '0'
#                         ext_price_str  = str(row[-1]).strip() if row[-1] else '0'

#                         if not product_code or not product_code[0].isdigit():
#                             continue

#                         unit_price = float(re.sub(r'[^\d.]', '', unit_price_str)) if unit_price_str else None
#                         ext_price  = float(re.sub(r'[^\d.]', '', ext_price_str)) if ext_price_str else None

#                         if qty > 0 and product_code:
#                             result['items'].append({
#                                 'product_code': product_code,
#                                 'quantity'    : int(qty),
#                                 'unit_price'  : unit_price,
#                                 'total_price' : ext_price,
#                             })
#                     except (ValueError, IndexError):
#                         continue

#     return result


def parse_sold_invoice_pdf(pdf_file):
    result = {
        'invoice_number': None,
        'sold_date'     : None,
        'customer_name' : None,
        'customer_email': None,
        'items'         : []
    }

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            # ── extract invoice number ─────────────────────────
            # matches: INV-ZO-2026-001 (must start with INV-)
            if not result['invoice_number']:
                match = re.search(r'Invoice No[:\s]*([A-Z0-9\-]+)', text, re.IGNORECASE)
                if match:
                    result['invoice_number'] = match.group(1).strip()
                    print(f"Invoice number: {result['invoice_number']}")

            # ── extract date ───────────────────────────────────
            # matches: Invoice Date: 05 May 2026
            if not result['sold_date']:
                match = re.search(
                    r'Invoice Date[:\s]+(\d{1,2}\s+\w+\s+\d{4})',
                    text, re.IGNORECASE
                )
                if match:
                    try:
                        result['sold_date'] = datetime.strptime(match.group(1).strip(), '%d %B %Y').date()
                        print(f"Sold date: {result['sold_date']}")
                    except ValueError:
                        pass

            # ── extract customer name ──────────────────────────
            # matches: first company name after "BILL TO"
            if not result['customer_name']:
                match = re.search(r'BILL TO\s+SHIP TO\s+([^\n]+)', text, re.IGNORECASE)
                if match:
                    full = match.group(1).strip()
                    
                    # PDF renders: "Mechatronics Technology LLC Mechatronic Technology LLC"
                    # Both are on same line — split by finding where second company starts
                    # Strategy: find "LLC", "Ltd", "Inc", "FZ" etc and cut after first occurrence
                    company_end = re.search(r'(LLC|Ltd|Limited|Inc|FZ|Pvt)\s+\w', full, re.IGNORECASE)
                    if company_end:
                        # cut at end of first company name
                        result['customer_name'] = full[:company_end.end()-2].strip()
                    else:
                        # fallback — split by 2+ spaces
                        parts = re.split(r'\s{2,}', full)
                        result['customer_name'] = parts[0].strip()
                    
                    print(f"Customer name: {result['customer_name']}")

            # ── extract customer email ─────────────────────────
            if not result['customer_email']:
                for email_match in re.finditer(r'[\w\.-]+@[\w\.-]+\.\w+', text):
                    email = email_match.group(0).strip()
                    # skip company/internal emails
                    if 'zoeing' not in email.lower() and 'accounts' not in email.lower():
                        result['customer_email'] = email
                        print(f"Customer email: {result['customer_email']}")
                        break

            # ── extract line items from text ───────────────────
            # pdfplumber merges columns into one cell so parse text directly
            # pattern: number  ZO-XXXXXX  description  qty  unit_price  total
            # e.g: "1 ZO-310153 CNC machine... 2 88.80 177.60"

            lines = text.split('\n')
            for line in lines:
                # match lines starting with: digit  ZO-code  ...  qty  price  total
                match = re.match(
                    r'^\s*\d+\s+(ZO-[A-Z0-9\-]+)\s+.+?\s+(\d+)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s*$',
                    line
                )
                if match:
                    material_code  = match.group(1).strip()
                    quantity       = int(match.group(2))
                    unit_price_str = match.group(3).replace(',', '')
                    total_str      = match.group(4).replace(',', '')

                    unit_price = float(unit_price_str) if unit_price_str else None
                    total      = float(total_str) if total_str else None

                    # avoid duplicates
                    existing_codes = [i['material_code'] for i in result['items']]
                    if material_code not in existing_codes:
                        result['items'].append({
                            'material_code': material_code,
                            'quantity'     : quantity,
                            'unit_price'   : unit_price,
                            'total_price'  : total,
                        })
                        print(f"Item added: {material_code} qty={quantity} price={unit_price}")

    print("Final parsed result:", result)
    return result