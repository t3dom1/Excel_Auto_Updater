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

## 3. Data Flow

| Step | Process | Description |
|------|---------|-------------|
| 1 | **Fetch** | Script sends HTTP GET request to the permanent GitHub raw URL. |
| 2 | **Validate** | Response status is verified. File integrity is checked by size. |
| 3 | **Load** | The binary content is saved to local storage as `Book.xlsx`. |
| 4 | **Extract** | The script reads three worksheets: `Sheet 1`, `Sheet 2`, `Sheet 3`. |
| 5 | **Parse** | From each sheet, data is extracted from rows 8, 12, 16, 20, 24. |
| 6 | **Clean** | Currency symbols (`₽`) and spaces are removed; type conversion is applied. |
| 7 | **Aggregate** | All records are combined into a single dataset with sequential indexing. |
| 8 | **Export** | The final table is saved as `processed_data.xlsx`. |

---

## 4. Repository Structure

| File | Purpose |
|------|---------|
| `Book.xlsx` | Source data (manually updated) |
| `parser.py` | Main ETL script |
| `processed_data.xlsx` | Generated output |
| `README.md` | Documentation |
| `requirements.txt` | Dependencies list |

---

## 5. Installation and Configuration

| Step | Action |
|------|--------|
| 1 | Clone the repository: `git clone https://github.com/[USERNAME]/excel-data.git` |
| 2 | Navigate to project directory: `cd excel-data` |
| 3 | Install dependencies: `pip install -r requirements.txt` |
| 4 | Manual installation: `pip install pandas requests openpyxl` |
| 5 | In `parser.py`, update `FILE_URL` with your GitHub raw link |

---

## 6. Execution

| Command | Description |
|---------|-------------|
| `python parser.py` | Run the main script |

**Expected console output:**

| Output | Description |
|--------|-------------|
| `Source: https://raw.githubusercontent.com/...` | Displays the source URL |
| `[10:30:15] Downloading...` | Indicates download start |
| `Downloaded: 34594 bytes` | Shows file size |
| `Sheets found: ['Sheet 1', 'Sheet 2', 'Sheet 3']` | Lists detected worksheets |
| `CONSOLIDATED TABLE` | Displays the aggregated data |
| `Saved: processed_data.xlsx` | Confirms successful export |
| `Records processed: 15` | Reports total record count |

---

## 7. Source Data Specification

| Parameter | Value |
|-----------|-------|
| File Format | .xlsx (Excel Workbook) |
| Worksheets | Sheet 1, Sheet 2, Sheet 3 |
| Header Row | Row 5 (merged cells in columns A, D, G) |
| Data Rows | 8, 12, 16, 20, 24 |
| Columns | A: Full Name, D: Amount, G: Headcount |
| Amount Format | `45 000 ₽` (cleaned automatically) |

---

## 8. Data Update Workflow

| Step | Action |
|------|--------|
| 1 | Upload the new `Book.xlsx` file to the repository root |
| 2 | Add to staging: `git add Book.xlsx` |
| 3 | Commit changes: `git commit -m "Data update"` |
| 4 | Push to remote: `git push` |
| 5 | Run `parser.py` – the system fetches and processes the latest version |

---

## 9. Technical Requirements

| Component | Minimum Version |
|-----------|-----------------|
| Python | 3.8+ |
| pandas | 1.3.0+ |
| requests | 2.25.0+ |
| openpyxl | 3.0.9+ |

---

## 10. Logging and Error Handling

| Control | Implementation |
|---------|----------------|
| HTTP Status | Response code is verified before proceeding |
| File Existence | Local file check before parsing |
| Exception Capture | Try-except blocks handle parsing errors |
| Record Reporting | Total record count is displayed after processing |

---

## 11. Licensing

This project is distributed under the MIT License.
