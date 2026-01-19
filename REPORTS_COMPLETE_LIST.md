# Tanzania Tax & Payroll Compliance - Complete Reports List
## All Reports for ALL Users (Management, Staff, Workers)

---

## REPORT STATUS LEGEND

- ✅ **EXISTS** - Already implemented in Tanzania app
- 🔵 **STANDARD** - Available in standard ERPNext/HRMS (can be used as-is or customized)
- ❌ **TO CREATE** - Needs to be built for Tanzania compliance

---

## COMPLETE REPORTS INVENTORY (20 Reports Total)

### CATEGORY 1: TAX COMPLIANCE REPORTS (7 Reports)

| # | Report Name | Status | Location | Users | Due Date |
|---|-------------|--------|----------|-------|----------|
| 1 | **VAT Return Report** | ✅ EXISTS | `tanzania/report/vat_return_report/` | CFO, Finance Mgr, Tax Officer | Monthly - 20th |
| 2 | **VAT Summary Report** | ✅ EXISTS | `tanzania/report/vat_summary_report/` | CEO, CFO, Finance Mgr | Ad-hoc |
| 3 | **Withholding Tax Report** | ✅ EXISTS | `tanzania/report/withholding_tax_report/` | CFO, Accounts Mgr | Monthly |
| 4 | **Tax Compliance Summary** | ✅ EXISTS | `tanzania/report/tax_compliance_summary/` | CEO, CFO, Compliance | Weekly |
| 5 | **PAYE & SDL Report** | ❌ TO CREATE | `tanzania/report/paye_sdl_report/` | HR, CFO, Payroll, Tax Officer | **Monthly - 7th** |
| 6 | **PAYE Computation Report** | ❌ TO CREATE | `tanzania/report/paye_computation_report/` | HR, Payroll, Tax Officer | Monthly |
| 7 | **Tax Payment Summary** | ❌ TO CREATE | `tanzania/report/tax_payment_summary/` | CFO, Finance Mgr | Monthly |

---

### CATEGORY 2: PAYROLL MANAGEMENT REPORTS (6 Reports)

| # | Report Name | Status | Location | Users | Frequency |
|---|-------------|--------|----------|-------|-----------|
| 8 | **Salary Register** | 🔵 STANDARD | `hrms/payroll/report/salary_register/` | HR Mgr, Payroll, Finance | Monthly |
| 9 | **Monthly Payroll Summary** | ❌ TO CREATE | `tanzania/report/monthly_payroll_summary/` | CEO, CFO, HR Director | Monthly |
| 10 | **Payroll Cost Analysis** | ❌ TO CREATE | `tanzania/report/payroll_cost_analysis/` | CEO, CFO, HR Director | Monthly/Quarterly |
| 11 | **Employee Salary Slip** | 🔵 STANDARD + CUSTOMIZE | `hrms/payroll/doctype/salary_slip/` + `tanzania/print_format/` | **ALL EMPLOYEES**, HR | **Monthly** |
| 12 | **Department Wise Payroll** | ❌ TO CREATE | `tanzania/report/department_wise_payroll/` | Dept Managers, CFO | Monthly |
| 13 | **Bank Remittance Report** | 🔵 STANDARD | `hrms/payroll/report/bank_remittance/` | Finance, Payroll | Monthly |

---

### CATEGORY 3: STATUTORY COMPLIANCE REPORTS (7 Reports)

| # | Report Name | Status | Location | Users | Due Date |
|---|-------------|--------|----------|-------|----------|
| 14 | **NSSF Contribution Report** | ❌ TO CREATE | `tanzania/report/nssf_contribution_report/` | HR Mgr, Payroll | **Monthly - 30th** |
| 15 | **PSSF Contribution Report** | ❌ TO CREATE | `tanzania/report/pssf_contribution_report/` | HR Mgr, Payroll | Monthly - 30th |
| 16 | **WCF Contribution Report** | ❌ TO CREATE | `tanzania/report/wcf_contribution_report/` | HR Mgr, Compliance | **Monthly - 30th** |
| 17 | **WCF Annual Return** | ❌ TO CREATE | `tanzania/report/wcf_annual_return/` | CFO, HR Mgr | **Annual - Mar 31** |
| 18 | **HESLB Deduction Report** | ❌ TO CREATE | `tanzania/report/heslb_deduction_report/` | HR Mgr, Payroll | Monthly - 30th |
| 19 | **SDL Compliance Report** | ❌ TO CREATE | `tanzania/report/sdl_compliance_report/` | HR Mgr, CFO | Monthly - 7th |
| 20 | **Statutory Payment Tracking** | ❌ TO CREATE | `tanzania/report/statutory_payment_tracking/` | CFO, Finance, Compliance | Weekly |

---

## SUMMARY BY STATUS

### ✅ EXISTING IN TANZANIA APP (4 Reports)
1. VAT Return Report
2. VAT Summary Report
3. Withholding Tax Report
4. Tax Compliance Summary

### 🔵 STANDARD ERPNEXT/HRMS (2 Reports - Can Use/Customize)
5. Salary Register (HRMS)
6. Bank Remittance (HRMS)

### ❌ TO CREATE FOR TANZANIA (14 Reports)
7. PAYE & SDL Report (CRITICAL - TRA filing)
8. PAYE Computation Report
9. Tax Payment Summary
10. Monthly Payroll Summary (CRITICAL - Management)
11. Payroll Cost Analysis
12. Employee Salary Slip Print Format (CRITICAL - All Workers)
13. Department Wise Payroll
14. NSSF Contribution Report (CRITICAL - NSSF filing)
15. PSSF Contribution Report
16. WCF Contribution Report (CRITICAL - WCF filing)
17. WCF Annual Return
18. HESLB Deduction Report
19. SDL Compliance Report
20. Statutory Payment Tracking

---

## PRIORITY IMPLEMENTATION PLAN

### 🔴 PHASE 1 - CRITICAL COMPLIANCE (Week 1)
**Must have before month-end:**

| Report | Priority | Reason |
|--------|----------|--------|
| PAYE & SDL Report | **P0** | TRA filing deadline 7th - MANDATORY |
| NSSF Contribution Report | **P0** | NSSF filing deadline 30th - MANDATORY |
| WCF Contribution Report | **P0** | WCF filing deadline 30th - MANDATORY |
| Employee Salary Slip (Custom) | **P0** | All employees need - CRITICAL |
| Monthly Payroll Summary | **P1** | Management oversight - IMPORTANT |

---

### 🟡 PHASE 2 - MANAGEMENT & TRACKING (Week 2)

| Report | Priority | Reason |
|--------|----------|--------|
| Statutory Payment Tracking | **P1** | Track all obligations |
| PAYE Computation Report | **P1** | Verify PAYE calculations |
| Department Wise Payroll | **P2** | Department managers need |
| HESLB Deduction Report | **P2** | Student loan tracking |

---

### 🟢 PHASE 3 - STRATEGIC & ANALYSIS (Week 3)

| Report | Priority | Reason |
|--------|----------|--------|
| Payroll Cost Analysis | **P2** | Strategic planning |
| Tax Payment Summary | **P2** | Cash flow planning |
| PSSF Contribution Report | **P3** | Public sector only |
| SDL Compliance Report | **P3** | Covered in PAYE report |
| WCF Annual Return | **P3** | Annual only (March) |

---

## DETAILED REPORT SPECIFICATIONS

### ✅ 1. VAT Return Report (EXISTS)
**File:** `tanzania/tanzania/report/vat_return_report/vat_return_report.py`
**Status:** Already implemented
**Purpose:** Monthly VAT return for TRA filing (due 20th)

**Features:**
- Output VAT (Standard 18%, Zero, Exempt)
- Input VAT (Standard 18%, Zero, Exempt)
- Net VAT Payable/Refundable
- Period: Monthly

**Users:** CFO, Finance Manager, Tax Officer

---

### ✅ 2. VAT Summary Report (EXISTS)
**File:** `tanzania/tanzania/report/vat_summary_report/vat_summary_report.py`
**Status:** Already implemented
**Purpose:** High-level VAT analysis

**Users:** CEO, CFO, Finance Manager

---

### ✅ 3. Withholding Tax Report (EXISTS)
**File:** `tanzania/tanzania/report/withholding_tax_report/withholding_tax_report.py`
**Status:** Already implemented
**Purpose:** Track WHT on supplier/contractor payments

**Users:** CFO, Accounts Payable Manager

---

### ✅ 4. Tax Compliance Summary (EXISTS)
**File:** `tanzania/tanzania/report/tax_compliance_summary/tax_compliance_summary.py`
**Status:** Already implemented
**Purpose:** Dashboard for all tax obligations

**Users:** CEO, CFO, Compliance Officer

---

### ❌ 5. PAYE & SDL Report (TO CREATE - CRITICAL)
**File:** `tanzania/tanzania/report/paye_sdl_report/`
**Priority:** **P0 - CRITICAL**
**Due:** Monthly by 7th

**Purpose:** Combined PAYE and SDL report for TRA filing

**Sections:**

1. **Company Information:**
   - Company Name, TIN, VRN
   - Period: [Month Year]
   - Total Employees

2. **PAYE Summary:**
   ```
   Tax Bracket | Taxable Income | No. of Employees | PAYE Tax
   ============|===============|==================|==========
   0% (0-270K) | xxx,xxx       | xx              | 0
   8% (270-520)| xxx,xxx       | xx              | xxx,xxx
   20% (520-760)| xxx,xxx      | xx              | xxx,xxx
   25% (760-1M)| xxx,xxx       | xx              | xxx,xxx
   30% (>1M)   | xxx,xxx       | xx              | xxx,xxx
   ============|===============|==================|==========
   TOTAL PAYE  | xxx,xxx,xxx   | xxx             | xxx,xxx,xxx
   ```

3. **SDL Summary:**
   ```
   Total Employees: xxx (✓ SDL Applicable if ≥10)
   Total Payroll Base: TZS xxx,xxx,xxx
   SDL Rate: 3.5%
   SDL Amount: TZS xxx,xxx
   ```

4. **Employee Details Table:**
   ```
   Employee ID | Name | TIN | Gross | NSSF/PSSF | Taxable | PAYE | SDL
   ```

5. **Summary:**
   ```
   Total PAYE Payable: TZS xxx,xxx,xxx
   Total SDL Payable: TZS xxx,xxx
   GRAND TOTAL DUE TO TRA: TZS xxx,xxx,xxx
   Due Date: 7th [Next Month]
   ```

**Filters:**
- Company (required)
- Payroll Period (Month/Year) (required)
- Department (optional)
- Employment Type (Primary/Secondary/All)
- Include Employee Details (Yes/No)

**Export:** PDF (for TRA), Excel

**Users:** HR Manager, CFO, Payroll Officer, Tax Officer

---

### 🔵 8. Salary Register (STANDARD - USE AS IS)
**File:** `hrms/hrms/payroll/report/salary_register/salary_register.py`
**Status:** Available in HRMS
**Purpose:** Complete employee-wise salary breakdown

**Columns:**
- Employee details
- Earnings (Basic, Allowances)
- Deductions (NSSF, PAYE, Loans)
- Net Salary
- Employer costs

**Usage:** Can be used directly, already includes Tanzania salary components

**Users:** HR Manager, Payroll Officer, Finance Manager

---

### ❌ 9. Monthly Payroll Summary (TO CREATE - CRITICAL)
**File:** `tanzania/tanzania/report/monthly_payroll_summary/`
**Priority:** **P0 - CRITICAL**

**Purpose:** Executive summary of monthly payroll

**Layout:**

```
═══════════════════════════════════════════════════════════
            MONTHLY PAYROLL SUMMARY
            [Company Name]
            Period: [Month Year]
═══════════════════════════════════════════════════════════

SUMMARY METRICS
───────────────────────────────────────────────────────────
Total Employees:                    xxx
Total Gross Salary:          TZS xxx,xxx,xxx
Total Net Paid:              TZS xxx,xxx,xxx
Total Employer Costs:        TZS xxx,xxx,xxx
TOTAL PAYROLL COST:          TZS xxx,xxx,xxx

COST BREAKDOWN
───────────────────────────────────────────────────────────
Basic Salary                 TZS xxx,xxx,xxx (xx%)
Allowances                   TZS xxx,xxx,xxx (xx%)
Employee Deductions          TZS xxx,xxx,xxx (xx%)
Employer Statutory           TZS xxx,xxx,xxx (xx%)

STATUTORY DEDUCTIONS
───────────────────────────────────────────────────────────
NSSF Employee                TZS xxx,xxx,xxx
NSSF Employer                TZS xxx,xxx,xxx
PSSF Employee                TZS xxx,xxx,xxx
PSSF Employer                TZS xxx,xxx,xxx
PAYE                         TZS xxx,xxx,xxx
SDL                          TZS xxx,xxx,xxx
WCF                          TZS xxx,xxx,xxx
HESLB                        TZS xxx,xxx,xxx

DEPARTMENT BREAKDOWN
───────────────────────────────────────────────────────────
Department | Headcount | Gross | Net | Employer Cost | Total
-----------|-----------|-------|-----|---------------|-------
Sales      | xx        | xxx   | xxx | xxx           | xxx
IT         | xx        | xxx   | xxx | xxx           | xxx
HR         | xx        | xxx   | xxx | xxx           | xxx

MONTH-OVER-MONTH COMPARISON
───────────────────────────────────────────────────────────
                    Previous    Current     Change    Change%
Headcount           xxx         xxx         +/-x      xx%
Total Cost          xxx,xxx     xxx,xxx     +/-xxx    xx%
Cost per Employee   xxx,xxx     xxx,xxx     +/-xxx    xx%
```

**Filters:**
- Company (required)
- Payroll Period (required)
- Show Department Breakdown (Yes/No)
- Compare Previous Month (Yes/No)

**Charts:**
- Pie Chart: Cost Distribution
- Bar Chart: Department Comparison

**Users:** CEO, CFO, HR Director, HR Manager

---

### ❌ 11. Employee Salary Slip (CUSTOMIZE - CRITICAL FOR ALL WORKERS)
**File:** `tanzania/tanzania/print_format/tanzania_salary_slip/`
**Priority:** **P0 - CRITICAL**

**Purpose:** Monthly salary statement for ALL employees

**Print Format Layout:**

```
═══════════════════════════════════════════════════════════
                 [COMPANY LOGO]
              [COMPANY NAME]
    TIN: [Company TIN] | VRN: [Company VRN]
              [Company Address]
═══════════════════════════════════════════════════════════

                    SALARY SLIP
                 [Month - Year]

───────────────────────────────────────────────────────────
EMPLOYEE INFORMATION
───────────────────────────────────────────────────────────
Employee ID:        [ID]          Employee Name:  [Name]
Department:         [Dept]        Designation:    [Title]
Employee TIN:       [TIN]         NSSF/PSSF:     [Number]
Bank:              [Bank]        Account:        [Account]
Pay Period:         [From - To]   Payment Date:   [Date]
───────────────────────────────────────────────────────────

EARNINGS                                          Amount (TZS)
───────────────────────────────────────────────────────────
Basic Salary                                      xxx,xxx.00
General Allowance                                 xxx,xxx.00
Transport Allowance                               xxx,xxx.00
Other Allowances                                  xxx,xxx.00
                                                 ────────────
GROSS SALARY                                    x,xxx,xxx.00
═══════════════════════════════════════════════════════════

DEDUCTIONS                                        Amount (TZS)
───────────────────────────────────────────────────────────
NSSF Employee (10%)                               xxx,xxx.00
PAYE Tax                                          xxx,xxx.00
HESLB (15%)                                       xxx,xxx.00
Loan Repayment                                    xxx,xxx.00
Other Deductions                                  xxx,xxx.00
                                                 ────────────
TOTAL DEDUCTIONS                                  xxx,xxx.00
───────────────────────────────────────────────────────────

NET SALARY PAYABLE                              x,xxx,xxx.00
═══════════════════════════════════════════════════════════

EMPLOYER CONTRIBUTIONS (Not Paid to Employee)
───────────────────────────────────────────────────────────
NSSF Employer (10%)                               xxx,xxx.00
Skills Development Levy (3.5%)                     xx,xxx.00
Workers Compensation Fund (0.5%)                    x,xxx.00
                                                 ────────────
TOTAL EMPLOYER COST                               xxx,xxx.00
═══════════════════════════════════════════════════════════

TOTAL COST TO COMPANY (CTC)                     x,xxx,xxx.00
═══════════════════════════════════════════════════════════

YEAR-TO-DATE SUMMARY (Jan - [Current Month])
───────────────────────────────────────────────────────────
Gross Salary YTD:        TZS xx,xxx,xxx.00
PAYE Paid YTD:           TZS x,xxx,xxx.00
NSSF Paid YTD:           TZS x,xxx,xxx.00
Net Paid YTD:            TZS xx,xxx,xxx.00

PAYMENT DETAILS
───────────────────────────────────────────────────────────
Bank Name:              [Bank Name]
Account Number:         [Account Number]
Payment Method:         Bank Transfer
Payment Date:           [DD-MMM-YYYY]
Payment Reference:      [REF]

───────────────────────────────────────────────────────────
This is a system-generated salary slip. No signature required.
Generated on: [DD-MMM-YYYY HH:MM AM/PM]

For queries, contact HR Department:
Email: hr@company.com | Phone: +255 XXX XXX XXX
───────────────────────────────────────────────────────────
```

**Features:**
- Print-friendly format (A4)
- PDF download
- Email to employee
- Mobile responsive
- Self-service portal access
- Historical access (12 months)
- Year-to-date totals
- Bilingual (English/Swahili option)

**Access:**
- **Employees:** Own slip only (self-service)
- **HR/Payroll:** All employees
- **Managers:** Direct reports only
- **Finance:** All employees (read-only)

**Users:** **ALL EMPLOYEES** (primary users), HR, Payroll, Managers

---

### ❌ 14. NSSF Contribution Report (TO CREATE - CRITICAL)
**File:** `tanzania/tanzania/report/nssf_contribution_report/`
**Priority:** **P0 - CRITICAL**
**Due:** Monthly by 30th

**Purpose:** NSSF Form CON.5 preparation

**Layout:**

```
═══════════════════════════════════════════════════════════
        NSSF CONTRIBUTION REPORT (FORM CON.5)
═══════════════════════════════════════════════════════════

EMPLOYER INFORMATION
───────────────────────────────────────────────────────────
Company Name:           [Company Name]
Employer Number:        [NSSF Number]
TIN:                    [TIN]
Period:                 [Month Year]
Report Date:            [Date]

CONTRIBUTION SUMMARY
───────────────────────────────────────────────────────────
# | Employee Name | NSSF No | Basic+Allow | Employee(10%) | Employer(10%) | Total | Running Total
--|---------------|---------|-------------|---------------|---------------|-------|---------------
1 | John Doe      | 12345   | 2,500,000   | 250,000       | 250,000       | 500,000 | 500,000
2 | Jane Smith    | 12346   | 3,000,000   | 300,000       | 300,000       | 600,000 | 1,100,000
...
xx| Last Employee | xxxxx   | x,xxx,xxx   | xxx,xxx       | xxx,xxx       | xxx,xxx | xx,xxx,xxx

TOTALS
───────────────────────────────────────────────────────────
Total Employees Contributing:        xxx
Total Contributory Salary:           TZS xxx,xxx,xxx.00
Total Employee Contributions (10%):  TZS  xx,xxx,xxx.00
Total Employer Contributions (10%):  TZS  xx,xxx,xxx.00
────────────────────────────────────────────────────────────
GRAND TOTAL PAYABLE TO NSSF:         TZS  xx,xxx,xxx.00
════════════════════════════════════════════════════════════

PAYMENT INFORMATION
───────────────────────────────────────────────────────────
Due Date:               30th [Month Year]
Payment Reference:      [Reference]
Payment Method:         [Bank Transfer/Other]
Payment Date:           [Date if paid]

NSSF BANK DETAILS
Bank: NMB Bank
Account: XXXXX-XXXXXX
Branch: [Branch Name]

═══════════════════════════════════════════════════════════
Prepared By:            [Name]
Designation:            [HR Manager/Payroll Officer]
Date:                   [Date]
Signature:              _____________________

Approved By:            [Name]
Designation:            [CFO/MD]
Date:                   [Date]
Signature:              _____________________
═══════════════════════════════════════════════════════════
```

**Filters:**
- Company (required)
- Payroll Period (required)
- Department (optional)
- Include Non-Contributors (Yes/No)

**Validations:**
- Only include employees with NSSF checkbox = 1
- Exclude PSSF employees
- Validate NSSF numbers

**Export:** PDF (for NSSF), Excel

**Users:** HR Manager, Payroll Officer

---

### ❌ 16. WCF Contribution Report (TO CREATE - CRITICAL)
**File:** `tanzania/tanzania/report/wcf_contribution_report/`
**Priority:** **P0 - CRITICAL**
**Due:** Monthly by 30th

**Purpose:** WCF monthly return

**Similar layout to NSSF but simpler:**
- All employees (no checkbox needed)
- Single rate: 0.5%
- Employer-only contribution

**Users:** HR Manager, Compliance Officer

---

## IMPLEMENTATION CHECKLIST

### For Each Report to Create:

- [ ] Create report directory structure
- [ ] Create `__init__.py`
- [ ] Create `[report_name].json` - Report metadata
- [ ] Create `[report_name].py` - Python query logic
- [ ] Create `[report_name].js` - Frontend filters
- [ ] Add role permissions
- [ ] Create sample data for testing
- [ ] Write unit tests
- [ ] Create user documentation
- [ ] Add to hooks.py if needed

### For Salary Slip Print Format:

- [ ] Create print format directory
- [ ] Create HTML/Jinja2 template
- [ ] Add CSS styling
- [ ] Test PDF generation
- [ ] Add email functionality
- [ ] Create self-service portal page
- [ ] Add employee permissions
- [ ] Test on mobile devices
- [ ] Create user guide (English/Swahili)

---

## USER ACCESS SUMMARY

### Who Can Access What:

**CEO/Board:**
- All reports (read-only)
- Focus: Tax Compliance Summary, Monthly Payroll Summary, Payroll Cost Analysis

**CFO/Finance:**
- All tax reports (read/write)
- All payroll reports (read-only)
- Focus: VAT, PAYE, Tax Payment Tracking, Statutory Payment Tracking

**HR Director/Manager:**
- All payroll reports (read/write)
- All statutory reports (read/write)
- Focus: Monthly Payroll Summary, NSSF, WCF, HESLB reports

**Payroll Officer:**
- Salary Register, Salary Slips, Statutory reports (read/write)
- Focus: Day-to-day processing and filing

**Department Managers:**
- Department Wise Payroll (own department)
- Salary Slips (direct reports)
- Focus: Budget monitoring

**ALL EMPLOYEES/WORKERS:**
- **Employee Salary Slip (own only)**
- Self-service portal
- 24/7 access
- Download/Print/Email

---

## NEXT STEPS

1. ✅ Review and approve this complete list
2. Prioritize Phase 1 (5 critical reports)
3. Start with PAYE & SDL Report (P0)
4. Then Employee Salary Slip customization (P0)
5. Then NSSF & WCF reports (P0)
6. Complete Phase 1 in Week 1
7. Move to Phase 2 reports
8. Launch employee self-service portal

---

**KEY INSIGHT:**
- We have **4 tax reports already working**
- We can **use Salary Register from HRMS**
- We need to **create 14 new reports** (5 critical first)
- **Most important for workers:** Employee Salary Slip with self-service access
