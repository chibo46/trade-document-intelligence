# Evaluation Log — Invoice Extraction Pipeline

## Summary
| Metric | Value |
|--------|-------|
| Total documents tested | 3 |
| Total fields evaluated | 30 |
| Correct extractions | 30 |
| Overall accuracy | 100% |
| Languages tested | English, Mixed Spanish/English |

## Document Results

### Document 001 — INV-2026-00847
- Route: USA → El Salvador
- Industry: Electronics / IT equipment
- Language: English
- Score: 10/10 fields correct ✅

### Document 002 — INV-2026-01134
- Route: Colombia → El Salvador
- Industry: Textiles / Apparel / Footwear
- Language: English
- Score: 10/10 fields correct ✅

### Document 003 — FC-2026-00392
- Route: Mexico → Guatemala
- Industry: Food & Beverages
- Language: Mixed Spanish/English (bilingual)
- Score: 10/10 fields correct ✅
- Note: Claude automatically translated dates and added HS 
  code descriptions in both languages — value beyond the prompt.

## Field Accuracy Breakdown
| Field | Doc 001 | Doc 002 | Doc 003 |
|-------|---------|---------|---------|
| Shipper | ✅ | ✅ | ✅ |
| Consignee | ✅ | ✅ | ✅ |
| Invoice number | ✅ | ✅ | ✅ |
| Invoice date | ✅ | ✅ | ✅ |
| HS Codes | ✅ | ✅ | ✅ |
| Description of goods | ✅ | ✅ | ✅ |
| Declared value | ✅ | ✅ | ✅ |
| Country of origin | ✅ | ✅ | ✅ |
| Net weight | ✅ | ✅ | ✅ |
| Gross weight | ✅ | ✅ | ✅ |

## Dataset Progress
- Current: 3 / 50 documents labeled
- Next: Add 7 more invoices (different formats, scanned docs)
