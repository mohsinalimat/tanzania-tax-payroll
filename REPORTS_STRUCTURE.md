# Tanzania Tax & Payroll Compliance - Reports Structure

This document outlines all reports required for managers, CEOs, CFOs, HR managers, and compliance officers.

---

## Report Categories

### 1. Tax Compliance Reports (TRA Filing)
### 2. Payroll Management Reports
### 3. Statutory Compliance Reports
### 4. Executive Summary Reports
### 5. Financial Analysis Reports
### 6. Audit & Compliance Reports

---

## 1. TAX COMPLIANCE REPORTS (TRA Filing)

### 1.1 VAT Return Report (Monthly - Due 20th)
**Report Name:** `VAT Return Report`
**Folder:** `tanzania/tanzania/report/vat_return_report/`
**Status:** ✅ EXISTS
**Users:** CFO, Finance Manager, Tax Officer
**Purpose:** Monthly VAT return filing to TRA

**Sections:**
- Output VAT (Sales - Standard/Zero/Exempt)
- Input VAT (Purchases - Standard/Zero/Exempt)
- Net VAT Payable/Refundable
- TRA Filing Summary

**Filters:**
- Company
- From Date
- To Date
- Tax Category

---

### 1.2 VAT Summary Report
**Report Name:** `VAT Summary Report`
**Folder:** `tanzania/tanzania/report/vat_summary_report/`
**Status:** ✅ EXISTS
**Users:** CFO, CEO, Finance Manager
**Purpose:** High-level VAT analysis for management decisions

**Columns:**
- Period
- Total Sales (Taxable)
- Output VAT Collected
- Total Purchases (Taxable)
- Input VAT Paid
- Net VAT Position
- Payment Status

---

### 1.3 PAYE & SDL Report (Monthly - Due 7th)
**Report Name:** `PAYE and SDL Report`
**Folder:** `tanzania/tanzania/report/paye_sdl_report/`
**Status:** ❌ TO CREATE
**Users:** HR Manager, CFO, Payroll Officer
**Purpose:** Monthly PAYE and SDL filing to TRA

**Sections:**
- **PAYE Summary:**
  - Total Gross Salary
  - Total NSSF/PSSF Deductions
  - Total Taxable Income
  - PAYE by Tax Bracket (0%, 8%, 20%, 25%, 30%)
  - Total PAYE Collected
- **SDL Summary:**
  - Total Payroll Base (Gross Salary)
  - SDL Rate (3.5%)
  - Total SDL Payable
- **Employee-wise Breakdown:**
  - Employee Name | TIN | Gross | NSSF/PSSF | Taxable | PAYE | SDL

**Filters:**
- Company
- Payroll Period (Month/Year)
- Employment Type (Primary/Secondary/All)
- Department
- Branch

---

### 1.4 Withholding Tax Report
**Report Name:** `Withholding Tax Report`
**Folder:** `tanzania/tanzania/report/withholding_tax_report/`
**Status:** ✅ EXISTS
**Users:** CFO, Accounts Payable Manager
**Purpose:** Track withholding tax on payments to suppliers/contractors

**Columns:**
- Supplier Name
- TIN/VRN
- Invoice Number
- Invoice Date
- Gross Amount
- WHT Rate
- WHT Amount
- Net Payment
- WHT Type (Service/Rental/Professional)

---

### 1.5 Tax Compliance Summary
**Report Name:** `Tax Compliance Summary`
**Folder:** `tanzania/tanzania/report/tax_compliance_summary/`
**Status:** ✅ EXISTS
**Users:** CEO, CFO, Compliance Officer
**Purpose:** Executive dashboard for all tax obligations

**Sections:**
- VAT Status (Payable/Paid)
- PAYE Status (Payable/Paid)
- SDL Status (Payable/Paid)
- WHT Status (Payable/Paid)
- Upcoming Deadlines
- Compliance Score
- Penalty/Interest (if any)

---

## 2. PAYROLL MANAGEMENT REPORTS

### 2.1 Monthly Payroll Summary Report
**Report Name:** `Monthly Payroll Summary`
**Folder:** `tanzania/tanzania/report/monthly_payroll_summary/`
**Status:** ❌ TO CREATE
**Users:** CEO, CFO, HR Manager
**Purpose:** High-level payroll cost analysis

**Sections:**
- **Summary Totals:**
  - Total Gross Salary
  - Total Earnings (Allowances, Incentives)
  - Total Deductions (NSSF, PAYE, HESLB, Loans)
  - Total Employer Costs (NSSF, SDL, WCF)
  - Total Net Salary Paid
  - Total Payroll Cost (Gross + Employer Costs)
- **Department-wise Breakdown**
- **Cost Center Analysis**
- **Month-over-Month Comparison**

**Filters:**
- Company
- Payroll Period
- Department
- Branch
- Employment Type

---

### 2.2 Salary Register (Detailed)
**Report Name:** `Salary Register`
**Folder:** `tanzania/tanzania/report/salary_register/`
**Status:** ❌ TO CREATE
**Users:** HR Manager, Payroll Officer, Finance Manager
**Purpose:** Detailed employee-wise salary breakdown

**Columns:**
- Employee ID | Employee Name | Department | Designation
- Basic Salary
- Allowances (Transport, Housing, etc.)
- Gross Salary
- NSSF/PSSF (Employee)
- Taxable Income
- PAYE
- HESLB
- Loan Deductions
- Other Deductions
- Net Salary
- Employer Costs (NSSF, SDL, WCF)
- Total Cost to Company

**Filters:**
- Company
- Payroll Period
- Department
- Branch
- Employee
- Employment Type

---

### 2.3 Payroll Cost Analysis Report
**Report Name:** `Payroll Cost Analysis`
**Folder:** `tanzania/tanzania/report/payroll_cost_analysis/`
**Status:** ❌ TO CREATE
**Users:** CEO, CFO, HR Director
**Purpose:** Strategic payroll cost management and budgeting

**Analysis:**
- **Cost Breakdown:**
  - Direct Salary Costs (70-75%)
  - Statutory Costs (NSSF, SDL, WCF) (15-20%)
  - Tax Burden (PAYE) (10-15%)
- **Trend Analysis:**
  - Last 12 Months Payroll Trend
  - Average Cost per Employee
  - Turnover Impact on Costs
- **Budget vs Actual:**
  - Budgeted Payroll
  - Actual Payroll
  - Variance (Amount & %)
- **Department-wise Cost Allocation**

**Charts:**
- Pie Chart: Cost Distribution
- Line Chart: 12-Month Trend
- Bar Chart: Department Comparison

---

### 2.4 Employee Salary Slip
**Report Name:** `Employee Salary Slip`
**Folder:** `tanzania/tanzania/report/employee_salary_slip/`
**Status:** ❌ TO CREATE
**Users:** All Employees, HR
**Purpose:** Individual employee salary statement

**Format:**
- Company Header with TIN/VRN
- Employee Details (Name, ID, TIN, Department, Bank Account)
- Salary Period
- **Earnings Section:**
  - Basic Salary
  - Allowances
  - Overtime/Incentives
  - **Gross Salary**
- **Deductions Section:**
  - NSSF/PSSF
  - PAYE Tax
  - HESLB
  - Loans/Advances
  - **Total Deductions**
- **Net Salary Payable**
- **Employer Contributions** (NSSF, SDL, WCF)
- **Payment Details** (Bank, Account, Payment Date)

---

## 3. STATUTORY COMPLIANCE REPORTS

### 3.1 NSSF Contribution Report (Monthly - Due 30th)
**Report Name:** `NSSF Contribution Report`
**Folder:** `tanzania/tanzania/report/nssf_contribution_report/`
**Status:** ❌ TO CREATE
**Users:** HR Manager, Payroll Officer
**Purpose:** NSSF Form CON.5 submission

**Columns:**
- Employee Name
- NSSF Number
- Basic Salary + Allowances
- Employee Contribution (10%)
- Employer Contribution (10%)
- Total Contribution (20%)
- Running Total

**Summary:**
- Total Employees Contributing
- Total Employee Contributions
- Total Employer Contributions
- Grand Total Payable to NSSF
- Payment Reference

**Filters:**
- Company
- Payroll Period
- Department

---

### 3.2 PSSF Contribution Report (Monthly - Due 30th)
**Report Name:** `PSSF Contribution Report`
**Folder:** `tanzania/tanzania/report/pssf_contribution_report/`
**Status:** ❌ TO CREATE
**Users:** HR Manager, Payroll Officer
**Purpose:** PSSF submission for public sector employees

**Columns:**
- Employee Name
- PSSF Number
- Basic Salary + Allowances
- Employee Contribution (5%)
- Employer Contribution (15%)
- Total Contribution (20%)

**Summary:**
- Total Employee Contributions
- Total Employer Contributions
- Grand Total Payable

---

### 3.3 WCF Contribution Report (Monthly - Due 30th)
**Report Name:** `WCF Contribution Report`
**Folder:** `tanzania/tanzania/report/wcf_contribution_report/`
**Status:** ❌ TO CREATE
**Users:** HR Manager, Compliance Officer
**Purpose:** WCF monthly return submission

**Columns:**
- Employee Name
- Employee ID
- Basic Salary + Allowances
- WCF Rate (0.5%)
- WCF Amount

**Summary:**
- Total Employees
- Total Payroll Base
- Total WCF Payable (0.5%)
- Payment Details

---

### 3.4 WCF Annual Return (Due March 31)
**Report Name:** `WCF Annual Return`
**Folder:** `tanzania/tanzania/report/wcf_annual_return/`
**Status:** ❌ TO CREATE
**Users:** CFO, HR Manager, Compliance Officer
**Purpose:** WCF annual filing (Mar 1 - Feb 28 period)

**Sections:**
- Company Details (TIN, VRN, Registration)
- Period: March 1, YYYY to February 28, YYYY+1
- **Monthly Breakdown** (12 months):
  - Month | Total Payroll | WCF Paid | Payment Date
- **Annual Summary:**
  - Total Payroll for Period
  - Total WCF Contributions
  - Average Monthly Contribution
- **Employee Count Summary:**
  - Beginning Headcount
  - New Hires
  - Terminations
  - Ending Headcount

---

### 3.5 HESLB Deduction Report (Monthly)
**Report Name:** `HESLB Deduction Report`
**Folder:** `tanzania/tanzania/report/heslb_deduction_report/`
**Status:** ❌ TO CREATE
**Users:** HR Manager, Payroll Officer
**Purpose:** HESLB student loan remittance tracking

**Columns:**
- Employee Name
- Employee ID
- HESLB Loan Number
- Basic Salary + Allowances
- HESLB Rate (15%)
- HESLB Deduction Amount

**Summary:**
- Total Employees with HESLB Loans
- Total Amount Deducted
- Total Amount Remitted
- Outstanding Remittances
- Payment Details

---

### 3.6 SDL Compliance Report (Monthly - Due 7th)
**Report Name:** `SDL Compliance Report`
**Folder:** `tanzania/tanzania/report/sdl_compliance_report/`
**Status:** ❌ TO CREATE
**Users:** HR Manager, CFO
**Purpose:** Skills Development Levy tracking (companies with 10+ employees)

**Sections:**
- **Eligibility Check:**
  - Current Employee Count
  - SDL Applicable: Yes/No
- **Calculation:**
  - Total Payroll Base
  - SDL Rate (3.5%)
  - SDL Amount
- **Payment Status:**
  - Amount Due
  - Amount Paid
  - Outstanding Balance
  - Due Date
  - Days Overdue

---

## 4. EXECUTIVE SUMMARY REPORTS

### 4.1 CEO Dashboard Report
**Report Name:** `CEO Dashboard - Tax & Payroll`
**Folder:** `tanzania/tanzania/report/ceo_dashboard/`
**Status:** ❌ TO CREATE
**Users:** CEO, Board of Directors
**Purpose:** Executive overview of all tax and payroll metrics

**KPIs:**
- **Payroll Metrics:**
  - Total Payroll Cost (Current Month)
  - Payroll Cost as % of Revenue
  - Average Salary per Employee
  - Headcount (Current/Change)
- **Tax Compliance:**
  - VAT Position (Payable/Refundable)
  - PAYE Collected
  - All Taxes Paid vs Due
  - Compliance Status (Green/Yellow/Red)
- **Statutory Obligations:**
  - NSSF Contributions Status
  - SDL Status
  - WCF Status
  - Upcoming Deadlines
- **Trend Analysis:**
  - 12-Month Payroll Trend
  - Tax Burden Trend
  - Headcount Trend

**Charts:**
- Payroll Cost Trend (Line)
- Tax Compliance Status (Donut)
- Department Headcount (Bar)
- Cost per Employee Trend (Line)

---

### 4.2 CFO Financial Dashboard
**Report Name:** `CFO Tax & Payroll Dashboard`
**Folder:** `tanzania/tanzania/report/cfo_dashboard/`
**Status:** ❌ TO CREATE
**Users:** CFO, Finance Director
**Purpose:** Financial oversight of tax and payroll liabilities

**Sections:**
- **Cash Flow Impact:**
  - Upcoming Tax Payments (7 days)
  - Upcoming Payroll (Next Pay Date)
  - Upcoming Statutory Payments (30 days)
  - Total Cash Requirement
- **Liability Management:**
  - PAYE Payable Balance
  - VAT Payable Balance
  - NSSF Payable Balance
  - SDL Payable Balance
  - WCF Payable Balance
  - HESLB Payable Balance
  - Total Statutory Liabilities
- **Expense Analysis:**
  - Payroll Expense (Current Month)
  - Payroll Expense (YTD)
  - Budget Variance
  - Forecast vs Actual
- **Compliance Risk:**
  - Overdue Payments (Amount & Days)
  - Penalty Risk
  - Interest Accrued

---

### 4.3 HR Director Dashboard
**Report Name:** `HR Director Dashboard`
**Folder:** `tanzania/tanzania/report/hr_director_dashboard/`
**Status:** ❌ TO CREATE
**Users:** HR Director, HR Manager
**Purpose:** People analytics and statutory compliance oversight

**Metrics:**
- **Workforce Analytics:**
  - Total Headcount (Breakdown by Type)
  - Department Distribution
  - Employment Type Mix (Primary/Secondary)
  - NSSF vs PSSF Split
- **Compensation Analytics:**
  - Average Salary by Department
  - Salary Range Analysis (Min, Avg, Max)
  - Salary Increase Trend
  - Benefits Cost per Employee
- **Statutory Compliance:**
  - NSSF Registration Status (%)
  - PSSF Registration Status (%)
  - HESLB Loan Deductions Active
  - TIN Assignment Status
- **Payroll Processing Status:**
  - Current Month Status
  - Pending Approvals
  - Errors/Issues
  - Payment Completion

---

### 4.4 Monthly Tax & Payroll Summary (Board Report)
**Report Name:** `Monthly Board Report - Tax & Payroll`
**Folder:** `tanzania/tanzania/report/monthly_board_report/`
**Status:** ❌ TO CREATE
**Users:** Board of Directors, CEO, CFO
**Purpose:** Monthly board meeting presentation

**Format:**
- **Executive Summary** (1 page)
- **Payroll Summary:**
  - Total Cost
  - Headcount Changes
  - Key Metrics
- **Tax Summary:**
  - VAT Position
  - PAYE Collected
  - Compliance Status
- **Risks & Issues:**
  - Overdue Obligations
  - Compliance Gaps
  - Cost Overruns
- **Recommendations:**
  - Action Items
  - Strategic Decisions Required

---

## 5. FINANCIAL ANALYSIS REPORTS

### 5.1 Payroll Variance Analysis
**Report Name:** `Payroll Variance Analysis`
**Folder:** `tanzania/tanzania/report/payroll_variance_analysis/`
**Status:** ❌ TO CREATE
**Users:** CFO, Finance Manager, HR Manager
**Purpose:** Budget vs actual payroll analysis

**Columns:**
- Cost Component
- Budget (Month)
- Actual (Month)
- Variance (Amount)
- Variance (%)
- YTD Budget
- YTD Actual
- YTD Variance

**Components:**
- Basic Salary
- Allowances
- Overtime
- Incentives
- NSSF (Employer)
- PSSF (Employer)
- SDL
- WCF
- **Total Payroll Cost**

---

### 5.2 Department Payroll Analysis
**Report Name:** `Department Payroll Analysis`
**Folder:** `tanzania/tanzania/report/department_payroll_analysis/`
**Status:** ❌ TO CREATE
**Users:** CEO, CFO, Department Heads
**Purpose:** Departmental cost allocation and analysis

**Columns:**
- Department
- Headcount
- Total Gross Salary
- Average Salary
- Statutory Costs
- Total Cost
- Cost per Employee
- % of Total Payroll

**Charts:**
- Pie Chart: Payroll by Department
- Bar Chart: Average Salary by Department
- Table: Department Ranking

---

### 5.3 Employee Cost Analysis
**Report Name:** `Employee Cost to Company (CTC) Report`
**Folder:** `tanzania/tanzania/report/employee_ctc_report/`
**Status:** ❌ TO CREATE
**Users:** HR Manager, Finance Manager
**Purpose:** True cost of employment per employee

**Breakdown:**
- **Direct Compensation:**
  - Basic Salary
  - Allowances
  - Incentives
  - **Gross Salary**
- **Employer Statutory Costs:**
  - NSSF (10%)
  - SDL (3.5%)
  - WCF (0.5%)
  - **Total Statutory (14%)**
- **Total Cost to Company (CTC)**
- **CTC Breakdown:**
  - Employee Takes Home: XX%
  - Government (PAYE): XX%
  - Social Security: XX%
  - Employer Costs: XX%

---

### 5.4 Tax Burden Analysis Report
**Report Name:** `Tax Burden Analysis`
**Folder:** `tanzania/tanzania/report/tax_burden_analysis/`
**Status:** ❌ TO CREATE
**Users:** CEO, CFO, Tax Advisor
**Purpose:** Overall tax liability analysis

**Sections:**
- **Monthly Tax Summary:**
  - VAT (Net Payable)
  - PAYE
  - SDL
  - Withholding Tax
  - Other Taxes
  - **Total Tax Liability**
- **Tax as % of Revenue:**
  - Direct Taxes %
  - Indirect Taxes %
  - Total Tax Burden %
- **Trend Analysis:**
  - 12-Month Tax Payment History
  - Tax Efficiency Metrics
- **Benchmarking:**
  - Industry Average Comparison
  - Tax Optimization Opportunities

---

## 6. AUDIT & COMPLIANCE REPORTS

### 6.1 Payroll Audit Trail Report
**Report Name:** `Payroll Audit Trail`
**Folder:** `tanzania/tanzania/report/payroll_audit_trail/`
**Status:** ❌ TO CREATE
**Users:** Internal Auditor, Compliance Officer
**Purpose:** Track all payroll changes and approvals

**Columns:**
- Transaction Date
- Payroll Period
- Employee
- Change Type (New Hire, Salary Change, Termination, etc.)
- Old Value
- New Value
- Changed By
- Approved By
- Approval Date
- Reason/Notes

---

### 6.2 Statutory Payment Tracking Report
**Report Name:** `Statutory Payment Tracking`
**Folder:** `tanzania/tanzania/report/statutory_payment_tracking/`
**Status:** ❌ TO CREATE
**Users:** CFO, Finance Manager, Compliance Officer
**Purpose:** Track all statutory payments and deadlines

**Columns:**
- Obligation Type (PAYE, SDL, NSSF, WCF, VAT)
- Period
- Due Date
- Amount Due
- Payment Date
- Amount Paid
- Payment Reference
- Days Late
- Penalty (if any)
- Status (Paid/Overdue/Upcoming)

**Summary:**
- Total Paid on Time
- Total Late Payments
- Total Penalties Incurred
- Compliance Rate %

---

### 6.3 Employee Statutory Deductions Register
**Report Name:** `Employee Statutory Deductions Register`
**Folder:** `tanzania/tanzania/report/employee_statutory_deductions_register/`
**Status:** ❌ TO CREATE
**Users:** Auditor, HR Manager
**Purpose:** Complete record of all statutory deductions

**Columns:**
- Employee ID | Employee Name | TIN
- Period
- Gross Salary
- NSSF/PSSF Deducted
- PAYE Deducted
- HESLB Deducted
- Total Deductions
- Remittance Status (Paid/Pending)
- Remittance Date
- Payment Reference

---

### 6.4 Tax Compliance Certificate Report
**Report Name:** `Tax Compliance Certificate Status`
**Folder:** `tanzania/tanzania/report/tax_compliance_certificate/`
**Status:** ❌ TO CREATE
**Users:** CFO, Compliance Officer
**Purpose:** Monitor TCC (Tax Compliance Certificate) eligibility

**Sections:**
- **Company Details:**
  - TIN
  - VRN
  - Current TCC Status
  - TCC Expiry Date
- **Compliance Status:**
  - All Taxes Filed (Yes/No)
  - All Taxes Paid (Yes/No)
  - Outstanding Liabilities
  - Last 12 Months Filing Status
- **TCC Eligibility:**
  - Eligible for TCC: Yes/No
  - Blocking Issues (if any)
  - Action Required

---

## SUMMARY: Complete Reports List

### ✅ Existing Reports (3)
1. VAT Return Report
2. VAT Summary Report
3. Withholding Tax Report

### ❌ Reports to Create (27)

#### Tax Reports (2)
4. PAYE and SDL Report
5. Tax Compliance Summary

#### Payroll Reports (4)
6. Monthly Payroll Summary
7. Salary Register
8. Payroll Cost Analysis
9. Employee Salary Slip

#### Statutory Compliance Reports (6)
10. NSSF Contribution Report
11. PSSF Contribution Report
12. WCF Contribution Report
13. WCF Annual Return
14. HESLB Deduction Report
15. SDL Compliance Report

#### Executive Reports (4)
16. CEO Dashboard
17. CFO Dashboard
18. HR Director Dashboard
19. Monthly Board Report

#### Financial Analysis Reports (4)
20. Payroll Variance Analysis
21. Department Payroll Analysis
22. Employee CTC Report
23. Tax Burden Analysis

#### Audit & Compliance Reports (4)
24. Payroll Audit Trail
25. Statutory Payment Tracking
26. Employee Statutory Deductions Register
27. Tax Compliance Certificate Status

---

## Report Access Matrix

| Report Category | CEO | CFO | Finance Mgr | HR Director | HR Mgr | Payroll Officer | Tax Officer | Auditor | Employee |
|----------------|-----|-----|-------------|-------------|--------|----------------|------------|---------|----------|
| VAT Reports | ✓ | ✓ | ✓ | - | - | - | ✓ | ✓ | - |
| PAYE/SDL | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| Payroll Summary | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | ✓ | - |
| Salary Register | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | ✓ | - |
| Employee Slip | - | - | - | ✓ | ✓ | ✓ | - | - | ✓ (Own) |
| NSSF/PSSF/WCF | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | ✓ | - |
| Executive Dash | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - |
| Financial Analysis | ✓ | ✓ | ✓ | ✓ | - | - | - | ✓ | - |
| Audit Reports | ✓ | ✓ | ✓ | - | - | - | - | ✓ | - |

---

## Report Frequencies

### Daily
- None (all reports are on-demand)

### Weekly
- Payroll Processing Status
- Upcoming Statutory Deadlines

### Monthly (Must Run)
1. VAT Return Report (by 20th)
2. PAYE & SDL Report (by 7th)
3. NSSF Contribution Report (by 30th)
4. WCF Contribution Report (by 30th)
5. HESLB Deduction Report (by 30th)
6. Monthly Payroll Summary
7. Monthly Board Report

### Quarterly
- Payroll Variance Analysis
- Department Payroll Analysis
- Tax Burden Analysis

### Annual
- WCF Annual Return (by March 31)
- Employee CTC Report
- Full Year Tax Compliance Summary

---

## Next Steps

1. Prioritize report creation based on compliance deadlines
2. Create report templates for each category
3. Implement data queries and calculations
4. Design report layouts and formatting
5. Add export functionality (PDF, Excel, CSV)
6. Implement role-based access control
7. Add scheduling for automated report generation
8. Create user documentation for each report
