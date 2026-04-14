import re

def extract_invoice_data(text):
    data = {}

    # Product Name (basic assumption)
    product_match = re.search(r"[A-Za-z ]{3,}", text)
    data["product_name"] = product_match.group(0) if product_match else "Unknown"

    # Quantity
    qty_match = re.search(r"\b\d+\b", text)
    data["quantity"] = int(qty_match.group(0)) if qty_match else 0

    # Price
    price_match = re.search(r"\d+\.\d{2}", text)
    data["price"] = float(price_match.group(0)) if price_match else 0.0

    # GST
    gst_match = re.search(r"GST\s*[:\-]?\s*(\d+\.\d+)", text)
    data["gst"] = float(gst_match.group(1)) if gst_match else 0.0

    # Total
    total_match = re.search(r"Total\s*[:\-]?\s*(\d+\.\d+)", text)
    data["total"] = float(total_match.group(1)) if total_match else 0.0

    return data
