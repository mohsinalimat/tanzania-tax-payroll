# SQL Fixes for Reports

## Issue: Unknown Column 'ss.taxable_earnings'

### Error Message
```
pymysql.err.OperationalError: (1054, "Unknown column 'ss.taxable_earnings' in 'SELECT'")
```

### Root Cause
The Salary Slip table in ERPNext HRMS doesn't have a `taxable_earnings` column. This field doesn't exist in the standard schema.

### Solution
Calculate taxable income in Python code instead of querying it from the database.

**Before (❌ Broken):**
```python
salary_slips = frappe.db.sql(f"""
    SELECT
        ss.name,
        ss.employee,
        ss.employee_name,
        ss.department,
        ss.designation,
        ss.gross_pay,
        ss.taxable_earnings,  ← DOESN'T EXIST
        ss.net_pay,
        ss.posting_date
    FROM `tabSalary Slip` ss
    WHERE ss.docstatus = 1
        {conditions}
    ORDER BY ss.employee, ss.posting_date
""", filters, as_dict=1)
```

**After (✅ Fixed):**
```python
salary_slips = frappe.db.sql(f"""
    SELECT
        ss.name,
        ss.employee,
        ss.employee_name,
        ss.department,
        ss.designation,
        ss.gross_pay,
        ss.net_pay,
        ss.posting_date
    FROM `tabSalary Slip` ss
    WHERE ss.docstatus = 1
        {conditions}
    ORDER BY ss.employee, ss.posting_date
""", filters, as_dict=1)

# Calculate taxable income in Python
for slip in salary_slips:
    nssf_employee = get_component_amount(slip.name, "NSSF")
    taxable_income = flt(slip.gross_pay) - flt(nssf_employee)
```

### Explanation
According to Tanzania tax law:
- **Taxable Income** = Gross Pay - NSSF Employee Contribution
- NSSF employee contribution (10%) is tax-deductible
- Other deductions (PAYE, HESLB, loans) are NOT deducted before calculating taxable income

### Files Changed
- [paye_and_sdl_report.py](tanzania/tanzania/report/paye_and_sdl_report/paye_and_sdl_report.py) - Line 121-135

---

## Common ERPNext HRMS Fields

For reference, here are the standard fields in Salary Slip table:

### Available Fields (Safe to Query):
- `name` - Salary slip ID
- `employee` - Employee ID
- `employee_name` - Employee name
- `company` - Company
- `department` - Department
- `designation` - Designation
- `start_date` - Payroll period start
- `end_date` - Payroll period end
- `posting_date` - Posting date
- `gross_pay` - Total earnings
- `total_deduction` - Total deductions
- `net_pay` - Net salary
- `payment_days` - Working days
- `absent_days` - Absent days
- `bank_name` - Bank name
- `bank_account_no` - Account number
- `mode_of_payment` - Payment method
- `docstatus` - Document status (0=Draft, 1=Submitted, 2=Cancelled)

### Fields That DON'T Exist (Don't Query):
- ❌ `taxable_earnings`
- ❌ `taxable_income`
- ❌ `tax_amount`
- ❌ `paye_amount`

These must be calculated from child tables (`tabSalary Detail`).

---

## How to Query Salary Components

Salary components (earnings and deductions) are stored in the child table `tabSalary Detail`.

### Example: Get NSSF Employee Contribution
```python
nssf_amount = frappe.db.get_value(
    "Salary Detail",
    {
        "parent": salary_slip_id,
        "parenttype": "Salary Slip",
        "salary_component": "NSSF"
    },
    "amount"
)
```

### Example: Get All Deductions for a Slip
```python
deductions = frappe.db.sql("""
    SELECT
        salary_component,
        amount
    FROM `tabSalary Detail`
    WHERE parent = %s
        AND parenttype = 'Salary Slip'
        AND parentfield = 'deductions'
""", (salary_slip_id,), as_dict=1)
```

### Example: Get All Earnings for a Slip
```python
earnings = frappe.db.sql("""
    SELECT
        salary_component,
        amount
    FROM `tabSalary Detail`
    WHERE parent = %s
        AND parenttype = 'Salary Slip'
        AND parentfield = 'earnings'
""", (salary_slip_id,), as_dict=1)
```

---

## Best Practices for Report SQL Queries

### 1. Check Field Existence
Before querying a field, verify it exists:
```bash
bench --site your-site.com mariadb -e "DESCRIBE \`tabSalary Slip\`"
```

### 2. Use Only Standard Fields
Stick to fields that exist in the standard ERPNext/HRMS schema unless you've added custom fields.

### 3. Calculate in Python When Needed
If a value needs to be calculated from multiple sources:
- Query the base data only
- Calculate derived values in Python
- More flexible and maintainable

### 4. Test with Empty Data
Always test reports when:
- No salary slips exist
- Filters return no results
- Required fields are null

### 5. Handle Null Values
Always use `flt()` or similar functions to handle NULL values:
```python
from frappe.utils import flt

# Good
taxable_income = flt(slip.gross_pay) - flt(nssf_employee)

# Bad (will crash if NULL)
taxable_income = slip.gross_pay - nssf_employee
```

---

## Verification Steps

After fixing SQL errors:

1. **Clear cache:**
```bash
bench --site your-site.com clear-cache
```

2. **Test the report:**
- Open the report in ERPNext
- Apply filters
- Verify data displays correctly
- Check calculations are accurate

3. **Test edge cases:**
- Run report with no data
- Run with date ranges that return no results
- Test with employees who have no NSSF
- Test with different companies

4. **Verify performance:**
```bash
# Time the query
bench --site your-site.com console
>>> from tanzania.tanzania.report.paye_and_sdl_report import paye_and_sdl_report
>>> import time
>>> start = time.time()
>>> paye_and_sdl_report.execute({'company': 'Test Company', 'from_date': '2024-01-01', 'to_date': '2024-12-31'})
>>> print(f"Execution time: {time.time() - start:.2f} seconds")
```

---

## Status

✅ **Fixed:** PAYE and SDL Report SQL query
✅ **Tested:** Report loads without SQL errors
✅ **Cache:** Cleared

**Next:** Test with actual salary slip data to verify calculations

---

**Date:** 2024-01-14
**Impact:** PAYE and SDL Report now functional
