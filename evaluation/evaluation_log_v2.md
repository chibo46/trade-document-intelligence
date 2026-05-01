# Evaluation Log — Invoice Extraction Pipeline
### Last updated: April 18, 2026

---

## Summary

| Metric | Value |
|--------|-------|
| Total documents tested | 10 |
| Total fields evaluated | 100 |
| Correct extractions | 100 |
| Overall accuracy | 100% |
| Languages tested | English, Mixed Spanish/English, Spanish date formats |
| Industries tested | Electronics, Apparel, Food & Beverage, Pharmaceutical, Agriculture, Mining, Construction, Consumer Electronics, Wine/Spirits |
| Currencies tested | USD, EUR |
| Routes tested | 10 different trade routes across Latin America, Europe, Asia |
| Prompt version | v1 (no iterations yet) |

---

## Document Results

### Document 001 — INV-2026-00847
- Route: USA → El Salvador
- Industry: Electronics / IT Equipment
- Language: English
- Currency: USD
- Total value: $42,515.00
- Net weight: 170.00 kg
- Score: **10/10 fields correct ✅**

### Document 002 — INV-2026-01134
- Route: Colombia → El Salvador
- Industry: Textiles / Apparel / Footwear
- Language: English
- Currency: USD
- Total value: $24,105.50
- Net weight: 333.50 kg
- Score: **10/10 fields correct ✅**

### Document 003 — FC-2026-00392
- Route: Mexico → Guatemala
- Industry: Food & Beverages
- Language: Mixed Spanish/English (bilingual)
- Currency: USD
- Total value: $45,016.60
- Net weight: 12,930.00 kg
- Score: **10/10 fields correct ✅**
- Note: Claude automatically translated Spanish dates and added HS code descriptions in both languages — value beyond the prompt.

### Document 004 — FARM-2026-00291
- Route: Peru → Spain
- Industry: Pharmaceutical / Medical Supplies
- Language: English
- Currency: EUR
- Total value: EUR €92,345.50
- Net weight: 219.00 kg
- Score: **10/10 fields correct ✅**
- Note: First EUR currency document — handled correctly.

### Document 005 — AGR-2026-00156
- Route: USA → Costa Rica
- Industry: Agricultural Machinery & Equipment
- Language: English
- Currency: USD (FOB)
- Total value: $98,700.00
- Net weight: 6,295.00 kg
- Score: **10/10 fields correct ✅**

### Document 006 — MIN-2026-00088
- Route: Chile → Honduras
- Industry: Mining Equipment
- Language: English
- Currency: USD (CIF)
- Total value: $201,682.50
- Net weight: 7,425.00 kg
- Score: **10/10 fields correct ✅**

### Document 007 — FC-ESP-2026-00445
- Route: Spain → El Salvador
- Industry: Wine & Olive Oil / Spirits
- Language: Mixed Spanish/English (bilingual labels, Spanish date)
- Currency: EUR (CIF)
- Total value: EUR €51,346.50
- Net weight: 3,046.00 kg
- Score: **10/10 fields correct ✅**
- Note: Spanish date "18 de Abril de 2026" correctly identified and translated. Bilingual product descriptions handled perfectly.

### Document 008 — SHZ-2026-08847
- Route: China → Guatemala
- Industry: Electronic Components (microcontrollers, cables, ICs)
- Language: English
- Currency: USD (FOB)
- Total value: $23,530.00
- Net weight: 232.50 kg
- Score: **10/10 fields correct ✅**
- Note: Technical component descriptions with part numbers extracted correctly.

### Document 009 — PAN-CONST-2026-00312
- Route: Panama → Nicaragua
- Industry: Construction Materials (steel, cement, PVC)
- Language: English
- Currency: USD (DAP, road freight)
- Total value: $133,595.75
- Net weight: 480,500.00 kg
- Score: **10/10 fields correct ✅**
- Note: Extreme weight (480,500 kg) extracted correctly. Road freight — different from all other documents.

### Document 010 — SEO-2026-HN-00934
- Route: South Korea → Honduras
- Industry: Consumer Electronics (TVs, phones, laptops)
- Language: English
- Currency: USD (CIF)
- Total value: $124,227.13
- Net weight: 1,537.50 kg
- Score: **10/10 fields correct ✅**
- Note: Mixed product types across 5 different electronics categories.

---

## Field Accuracy Breakdown — All 10 Documents

| Field | 001 | 002 | 003 | 004 | 005 | 006 | 007 | 008 | 009 | 010 |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| Shipper | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Consignee | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Invoice number | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Invoice date | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ Spanish | ✅ | ✅ | ✅ |
| HS Codes | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Description | ✅ | ✅ | ✅ bilingual | ✅ | ✅ | ✅ | ✅ bilingual | ✅ technical | ✅ | ✅ |
| Declared value | ✅ USD | ✅ USD | ✅ USD | ✅ EUR | ✅ USD | ✅ USD | ✅ EUR | ✅ USD | ✅ USD | ✅ USD |
| Country of origin | ✅ per line | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Net weight | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 480,500 kg | ✅ |
| Gross weight | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Total: 100/100 fields correct — 100% accuracy**

---

## Key Observations

1. **EUR currency handled correctly** — Documents 004 and 007 used EUR. Extractor correctly identified and reported the currency without confusion.

2. **Bilingual documents work well** — Documents 003 and 007 had mixed Spanish/English content. Claude handled both languages seamlessly and even translated Spanish dates automatically.

3. **Extreme values no problem** — Document 009 had 480,500 kg net weight (container shipment). Extracted correctly despite being 100x larger than other documents.

4. **Technical descriptions extracted** — Document 008 had part numbers, component specifications, and technical codes. All extracted accurately.

5. **Claude adds value beyond the prompt** — On multiple documents, Claude included bonus information (Incoterm, port details, payment terms) not explicitly requested. Useful for customs declarations.

6. **Human-in-the-loop warning present** — All extractions included the verification warning. Legal protection working as designed.

---

## Prompt Version History

| Version | Change | Accuracy |
|---------|--------|----------|
| v1 (current) | Initial prompt — fields listed, JSON output requested | 100% on 10 docs |
| v2 | Planned: Add few-shot examples | TBD |
| v3 | Planned: Add confidence indicators per field | TBD |

## Automated Evaluation Script

| Metric | Value |
|--------|-------|
| Script type | Automated — runs all docs in one command |
| Judge | LLM-as-a-Judge (Claude Haiku) for semantic accuracy |
| HS code handling | Individual code matching |
| Format handling | Ignores currency symbols and comma formatting |
| Average extraction time | ~20 seconds per document |

## Final Results — Prompt v2 with Automated Evaluation

| Document | Fields Correct | Accuracy |
|----------|---------------|----------|
| synthetic_invoice_001.pdf | 10/10 | 100% |
| synthetic_invoice_002_COL_SLV.pdf | 10/10 | 100% |
| synthetic_invoice_003_MEX_GTM.pdf | 10/10 | 100% |
| **OVERALL** | **30/30** | **100%** |
---

## Dataset Progress

- **Current:** 10 / 50 documents labeled
- **Next:** Expand to 30 documents — add varied formats:
  - Scanned PDFs (phone photos)
  - Documents with handwritten annotations
  - Poor quality scans
  - Documents with tables in different layouts
- **Goal:** Find the accuracy floor — where does the extractor start failing?

---

## Next Steps

1. Deploy Gradio app to Hugging Face Spaces (permanent URL)
2. Test 3 prompt versions — measure before/after accuracy
3. Add LLM-as-a-Judge evaluation (Claude Haiku as critic model)
4. Build automated evaluation script
5. Test on messy/scanned invoices to find accuracy floor
6. Add 20 more documents to reach 30/50

---

*Evaluation log version: 2*
*Last updated: April 18, 2026*
*Next update: after Hugging Face deployment and prompt iteration*
