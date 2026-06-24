# Excel Data Sync
**Version:** 1.0.0 | **Status:** Production | **License:** MIT

---

## 1. Purpose

The **Excel Data Sync** project provides a lightweight ETL pipeline for automated retrieval, parsing, and aggregation of structured Excel data stored in a remote Git repository.

The system eliminates manual file handling by providing a single access point for analytics processing.

---

## 2. Core Functionality

| Component | Description |
|-----------|-------------|
| **File Download** | Retrieves the source file via a permanent raw URL from GitHub |
| **Structure Parsing** | Handles merged cells and non‑standard worksheet layouts |
| **Multi‑sheet Aggregation** | Combines data from three sheets into a unified dataset |
| **Data Cleaning** | Removes currency symbols, whitespace, and normalises data types |
| **Record Indexing** | Applies automatic sequential numbering to all entries |
| **Result Export** | Outputs a well‑structured Excel workbook |

---

## 3. System Architecture
┌─────────────────────┐
│ GitHub Repository │
│ (Book.xlsx) │
└──────────┬──────────┘
│ HTTP GET (raw)
▼
┌─────────────────────┐
│ download_file() │
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│ parse_excel() │
│ - Sheet 1 │
│ - Sheet 2 │
│ - Sheet 3 │
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│ Consolidated Table │
│ ID, Name, Amount, │
│ Headcount │
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│ processed_data │
│ .xlsx │
└─────────────────────┘
