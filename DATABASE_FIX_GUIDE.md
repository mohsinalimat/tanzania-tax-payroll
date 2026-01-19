# Database Fix Guide - Report Renaming Issues

## Problem: Module Not Found Error After Renaming Report

When you rename a report's files but the old report name still exists in the database, you'll get errors like:

```
ModuleNotFoundError: No module named 'tanzania.tanzania.report.paye_&_sdl_report'
```

This happens because:
1. The Report document in the database still has the old name
2. ERPNext tries to import the Python module using the old name
3. The old directory/files no longer exist

## Solution

### Method 1: Using Custom Fix Script (Recommended)

1. **Create fix script:**

```python
# File: apps/tanzania/tanzania/fix_reports.py

import frappe

def fix_paye_report():
    """Delete old PAYE & SDL Report and let it be recreated with new name"""
    try:
        if frappe.db.exists("Report", "PAYE & SDL Report"):
            frappe.delete_doc("Report", "PAYE & SDL Report", force=True, ignore_permissions=True)
            frappe.db.commit()
            print("✅ Deleted old 'PAYE & SDL Report'")
        else:
            print("ℹ️  Old 'PAYE & SDL Report' not found")

        if frappe.db.exists("Report", "PAYE and SDL Report"):
            print("✅ New 'PAYE and SDL Report' exists")
        else:
            print("⚠️  New 'PAYE and SDL Report' not found - will be created on next sync")

    except Exception as e:
        print(f"❌ Error: {e}")
        frappe.db.rollback()
```

2. **Run the fix:**

```bash
bench --site your-site.com execute tanzania.fix_reports.fix_paye_report
```

3. **Clear cache:**

```bash
bench --site your-site.com clear-cache
```

### Method 2: Using Direct Database Update

If you prefer SQL:

```bash
bench --site your-site.com mariadb
```

Then in MariaDB:

```sql
-- Check if old report exists
SELECT name FROM `tabReport` WHERE name = 'PAYE & SDL Report';

-- Delete old report
DELETE FROM `tabReport` WHERE name = 'PAYE & SDL Report';

-- Verify new report exists
SELECT name, module FROM `tabReport` WHERE name = 'PAYE and SDL Report';
```

### Method 3: Using ERPNext UI

1. Go to: **Desk → Setup → Report**
2. Search for "PAYE & SDL Report"
3. Open it and delete it
4. Reload the page
5. The new "PAYE and SDL Report" should appear

## Verification Steps

After applying the fix:

1. **Clear all caches:**
```bash
bench --site your-site.com clear-cache
bench --site your-site.com clear-website-cache
```

2. **Check if report works:**
   - Go to Reports list in ERPNext
   - Search for "PAYE and SDL Report" (with "and", not "&")
   - Click to open it
   - Try running the report

3. **Verify module path:**
```bash
ls -la apps/tanzania/tanzania/tanzania/report/paye_and_sdl_report/
```

Should show:
```
__init__.py
paye_and_sdl_report.json
paye_and_sdl_report.py
paye_and_sdl_report.js
```

## Prevention: Best Practices

### 1. Report Naming Rules

**DO:**
- Use simple alphanumeric names with spaces
- "PAYE and SDL Report" ✅
- "Monthly Payroll Summary" ✅
- "NSSF Contribution Report" ✅

**DON'T:**
- Use special characters: `& * / \ @ # $ % ^`
- "PAYE & SDL Report" ❌
- "P&L Report" ❌
- "Cost/Benefit Analysis" ❌

### 2. Renaming Existing Reports

If you must rename a report:

**Step 1:** Delete from database first
```bash
bench --site your-site.com execute "frappe.delete_doc('Report', 'Old Report Name', force=True)"
```

**Step 2:** Rename files
```bash
mv old_report/ new_report/
mv new_report/old_report.* new_report/new_report.*
```

**Step 3:** Update JSON
```json
{
  "name": "New Report Name",
  "report_name": "New Report Name"
}
```

**Step 4:** Update JavaScript
```javascript
frappe.query_reports["New Report Name"] = {
  // ...
}
```

**Step 5:** Clear cache and migrate
```bash
bench --site your-site.com clear-cache
bench --site your-site.com migrate
```

## Common Errors and Fixes

### Error 1: Module Not Found
```
ModuleNotFoundError: No module named 'tanzania.tanzania.report.old_name'
```

**Fix:** Delete old Report document from database (see Method 1 above)

### Error 2: Letter Head Not Found
```
Could not find Letter Head: Some Letter Head Name
```

**Fix:** Remove `letter_head` field from JSON or create the Letter Head first

### Error 3: Import Error
```
ImportError: cannot import name 'execute' from 'tanzania.tanzania.report.paye_&_sdl_report'
```

**Fix:** Check that `__init__.py` exists in report directory

### Error 4: Report Not Visible
**Symptoms:** Report doesn't appear in Reports list

**Fix:**
```bash
bench --site your-site.com reload-doc tanzania Report "Report Name"
bench --site your-site.com clear-cache
```

## Applied Fixes for Tanzania App

For this project, the following fixes were applied:

1. ✅ Renamed "PAYE & SDL Report" to "PAYE and SDL Report"
2. ✅ Removed all `letter_head` references from JSON files
3. ✅ Created all missing `__init__.py` files
4. ✅ Deleted old report documents from database
5. ✅ Cleared all caches

### Files Fixed:

```
apps/tanzania/tanzania/tanzania/report/
├── paye_and_sdl_report/              ← RENAMED (was paye_sdl_report)
│   ├── __init__.py                   ← CREATED
│   ├── paye_and_sdl_report.json      ← RENAMED & FIXED
│   ├── paye_and_sdl_report.py        ← RENAMED
│   └── paye_and_sdl_report.js        ← RENAMED & FIXED
├── nssf_contribution_report/
│   ├── __init__.py                   ← CREATED
│   └── nssf_contribution_report.json ← FIXED (removed letter_head)
├── wcf_contribution_report/
│   ├── __init__.py                   ← CREATED
│   └── wcf_contribution_report.json  ← FIXED (removed letter_head)
└── monthly_payroll_summary/
    └── __init__.py                   ← CREATED
```

## Testing After Fixes

Run these tests to ensure everything works:

```bash
# Test 1: List all reports
bench --site your-site.com execute "print([r.name for r in frappe.get_all('Report', filters={'module': 'Tanzania'})])"

# Test 2: Try importing the Python module
bench --site your-site.com console
>>> from tanzania.tanzania.report.paye_and_sdl_report import paye_and_sdl_report
>>> paye_and_sdl_report.execute()

# Test 3: Access via UI
# Go to: http://your-site.com/app/query-report/PAYE%20and%20SDL%20Report
```

## Emergency Rollback

If fixes cause issues, you can rollback:

```bash
# 1. Restore old report from backup
bench --site your-site.com --force restore /path/to/backup.sql

# 2. Or recreate manually in UI
# Go to: Desk → Setup → Report → New Report
# Fill in all details manually
```

## Support

If issues persist:
1. Check error logs: `bench --site your-site.com logs`
2. Check browser console for JavaScript errors
3. Verify file permissions: `ls -la apps/tanzania/tanzania/tanzania/report/`
4. Ensure Python can import: `python -c "import tanzania.tanzania.report.paye_and_sdl_report.paye_and_sdl_report"`

---

**Last Updated:** 2024-01-14
**Status:** ✅ All Phase 1 reports fixed and working
