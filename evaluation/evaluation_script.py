!pip install anthropic pdfplumber --quiet

import pdfplumber
import anthropic
import time
from google.colab import userdata

# Initialize client
client = anthropic.Anthropic(api_key=userdata.get('ANTHROPIC_API_KEY'))

# ── PDF EXTRACTION ────────────────────────────────────────────────────────────
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# ── CHAIN OF THOUGHT EXTRACTOR ────────────────────────────────────────────────
def extract_with_chain_of_thought(text):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system="You are an expert at extracting structured data from trade documents for customs declarations. Always reason carefully before extracting.",
        messages=[{
            "role": "user",
            "content": f"""You will extract customs fields from a commercial invoice.

Before extracting, work through these steps:

Step 1 - Document overview: What type of document is this? What trade route does it cover?
Step 2 - Identify key sections: Where are the party details, line items, weights, and values located?
Step 3 - Resolve ambiguities: Are there multiple values or dates? Which is the correct one for customs?
Step 4 - Extract fields: Now extract each field with confidence.

Invoice text:
{text[:4000]}

Work through all 4 steps, then provide the final extraction:
- Shipper name and address
- Consignee name and address
- Invoice number
- Invoice date
- HS Code(s)
- Description of goods
- Declared value and currency
- Country of origin
- Net weight
- Gross weight

⚠️ AI-assisted extraction — verify all fields before submitting to customs authorities."""
        }]
    )
    return response.content[0].text

# ── GROUND TRUTH ──────────────────────────────────────────────────────────────
ground_truth = {
    "synthetic_invoice_001.pdf": {
        "shipper": "GlobalTech Imports LLC",
        "consignee": "TechSolutions S.A. de C.V.",
        "invoice_number": "INV-2026-00847",
        "invoice_date": "April 18, 2026",
        "hs_codes": ["8471.30.00", "8471.60.10", "8471.60.20", "8528.52.00", "8504.40.10", "8536.69.90"],
        "declared_value": "42515.00",
        "currency": "USD",
        "country_of_origin": "China",
        "net_weight": "170.00",
        "gross_weight": "195.50"
    },
    "synthetic_invoice_002_COL_SLV.pdf": {
        "shipper": "Textiles Andinos S.A.S.",
        "consignee": "Moda Latina S.A. de C.V.",
        "invoice_number": "INV-2026-01134",
        "invoice_date": "April 18, 2026",
        "hs_codes": ["6205.20.00", "6204.62.00", "6110.20.10", "6403.51.00", "6116.10.00"],
        "declared_value": "24105.50",
        "currency": "USD",
        "country_of_origin": "Colombia",
        "net_weight": "333.50",
        "gross_weight": "358.00"
    },
    "synthetic_invoice_003_MEX_GTM.pdf": {
        "shipper": "Alimentos del Pacífico S.A. de C.V.",
        "consignee": "Distribuidora Centroamericana S.A.",
        "invoice_number": "FC-2026-00392",
        "invoice_date": "18 de Abril de 2026",
        "hs_codes": ["2009.11.00", "1901.90.90", "2103.20.00", "1704.90.90", "2202.10.00", "0901.21.00"],
        "declared_value": "45016.60",
        "currency": "USD",
        "country_of_origin": "México",
        "net_weight": "12930.00",
        "gross_weight": "13850.00"
    },
}

# ── LLM-AS-A-JUDGE ────────────────────────────────────────────────────────────
def judge_field(field_name, extracted, expected):
    if not extracted or str(extracted).strip() == "":
        return False, "empty"
    judge_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": f"""Are these two values semantically equivalent for a customs declaration?

Field: {field_name}
Extracted: {extracted}
Expected: {expected}

Answer only YES or NO, then one sentence explaining why."""
        }]
    )
    answer = judge_response.content[0].text.strip()
    is_correct = answer.upper().startswith("YES")
    return is_correct, answer

# ── EVALUATION RUNNER ─────────────────────────────────────────────────────────
def run_evaluation(invoice_files, prompt_version="v2"):
    results = []
    fields = [
        "shipper", "consignee", "invoice_number", "invoice_date",
        "hs_codes", "declared_value", "currency",
        "country_of_origin", "net_weight", "gross_weight"
    ]
    total_fields = 0
    correct_fields = 0

    print(f"\n{'='*60}")
    print(f"EVALUATION REPORT — Prompt {prompt_version}")
    print(f"{'='*60}\n")

    for filename in invoice_files:
        if filename not in ground_truth:
            print(f"⚠️  No ground truth for {filename} — skipping")
            continue

        print(f"📄 {filename}")
        start = time.time()

        try:
            text = extract_text_from_pdf(f"/content/{filename}")
            extracted_text = extract_with_chain_of_thought(text)
        except Exception as e:
            print(f"   ❌ Extraction failed: {e}\n")
            continue

        elapsed = time.time() - start
        gt = ground_truth[filename]
        doc_correct = 0
        doc_total = len(fields)

        for field in fields:
            expected = gt.get(field, "")

            # Special handling for HS codes — check each code individually
            if field == "hs_codes" and isinstance(expected, list):
                codes_found = sum(1 for code in expected if code in extracted_text)
                is_correct = codes_found == len(expected)
                judge_used = "✅" if is_correct else "🤖"
                if not is_correct:
                    is_correct, _ = judge_field(field, extracted_text, str(expected))
            else:
                if isinstance(expected, list):
                    expected = ", ".join(expected)
                is_correct = str(expected).lower() in extracted_text.lower()
                if not is_correct:
                    is_correct, _ = judge_field(field, extracted_text, str(expected))
                    judge_used = "🤖"
                else:
                    judge_used = "✅"

            status = "✅" if is_correct else "❌"
            print(f"   {status} {judge_used} {field}: {'correct' if is_correct else f'WRONG — expected: {expected}'}")

            if is_correct:
                doc_correct += 1
                correct_fields += 1
            total_fields += 1

        doc_accuracy = round(doc_correct / doc_total * 100, 1)
        print(f"   📊 Document accuracy: {doc_correct}/{doc_total} ({doc_accuracy}%)")
        print(f"   ⏱️  Extraction time: {elapsed:.1f}s\n")

        results.append({
            "file": filename,
            "correct": doc_correct,
            "total": doc_total,
            "accuracy": doc_accuracy,
            "time": round(elapsed, 1)
        })

    overall = round(correct_fields / total_fields * 100, 1) if total_fields > 0 else 0
    print(f"{'='*60}")
    print(f"OVERALL: {correct_fields}/{total_fields} fields correct — {overall}% accuracy")
    print(f"{'='*60}\n")
    return results

# ── RUN IT ────────────────────────────────────────────────────────────────────
invoice_files = [
    "synthetic_invoice_001.pdf",
    "synthetic_invoice_002_COL_SLV.pdf",
    "synthetic_invoice_003_MEX_GTM.pdf",
]

results = run_evaluation(invoice_files, prompt_version="v2")
