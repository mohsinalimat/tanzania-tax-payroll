# Tanzania Tax & Payroll - Priority Reports Implementation

## PRIORITY REPORTS TO IMPLEMENT (13 Reports)

These are the MUST-HAVE reports that managers, CFOs, and HR need for day-to-day operations and compliance.

---

## CATEGORY 1: TAX COMPLIANCE REPORTS (5 Reports)

### ✅ 1. VAT Return Report (EXISTS)
**Status:** Already implemented
**Due:** Monthly by 20th
**Users:** CFO, Tax Officer

### ✅ 2. VAT Summary Report (EXISTS)
**Status:** Already implemented
**Users:** CEO, CFO

### ✅ 3. Withholding Tax Report (EXISTS)
**Status:** Already implemented
**Users:** CFO, Accounts Manager

### ❌ 4. PAYE & SDL Report (PRIORITY 1)
**Report Name:** `PAYE and SDL Report`
**Folder:** `tanzania/tanzania/report/paye_sdl_report/`
**Due:** Monthly by 7th
**Users:** HR Manager, CFO, Payroll Officer

**Purpose:** Combined PAYE and SDL filing report for TRA

**Sections:**
1. **PAYE Summary:**
   - Total Employees
   - Total Gross Salary
   - Total NSSF/PSSF Deductions
   - Total Taxable Income
   - PAYE by Bracket:
     - Bracket 1 (0%): Income, Employees, Tax = 0
     - Bracket 2 (8%): Income, Employees, Tax
     - Bracket 3 (20%): Income, Employees, Tax
     - Bracket 4 (25%): Income, Employees, Tax
     - Bracket 5 (30%): Income, Employees, Tax
   - Total PAYE Collected

2. **SDL Summary:**
   - Total Employees (must be ≥10 for SDL)
   - Total Payroll Base
   - SDL Rate (3.5%)
   - Total SDL Payable

3. **Employee Details Table:**
   - Employee ID | Name | TIN
   - Gross Salary
   - NSSF/PSSF Deduction
   - Taxable Income
   - PAYE Amount
   - SDL Amount

**Filters:**
- Company (required)
- Payroll Period (Month/Year) (required)
- Department (optional)
- Employment Type (Primary/Secondary/All)

**Export:** PDF for TRA submission, Excel for records

---

### ❌ 5. Tax Compliance Summary Dashboard (PRIORITY 2)
**Report Name:** `Tax Compliance Summary`
**Folder:** `tanzania/tanzania/report/tax_compliance_summary/`
**Users:** CEO, CFO, Compliance Officer

**Purpose:** One-page dashboard showing all tax obligations status

**Metrics Cards:**
1. **VAT Status:**
   - Current Month VAT Payable/Refundable
   - Payment Status
   - Due Date
   - Days Until Due

2. **PAYE Status:**
   - Current Month PAYE Collected
   - Payment Status
   - Due Date (7th)
   - Days Until Due

3. **SDL Status:**
   - Current Month SDL Amount
   - Payment Status
   - Due Date (7th)
   - Eligible (Yes/No based on employee count)

4. **Statutory Contributions:**
   - NSSF Total Due
   - PSSF Total Due (if applicable)
   - WCF Total Due
   - HESLB Total Due
   - Due Date (30th)

5. **Compliance Status:**
   - All Obligations Paid: Yes/No
   - Overdue Obligations Count
   - Total Amount Overdue
   - Compliance Score (%)

**Table: Upcoming Deadlines (Next 30 Days):**
- Obligation | Amount | Due Date | Status | Days Remaining

**Filters:**
- Company
- Period (Current Month/Custom Range)

---

## CATEGORY 2: PAYROLL MANAGEMENT REPORTS (4 Reports)

### ❌ 6. Monthly Payroll Summary (PRIORITY 1)
**Report Name:** `Monthly Payroll Summary`
**Folder:** `tanzania/tanzania/report/monthly_payroll_summary/`
**Users:** CEO, CFO, HR Manager

**Purpose:** Executive summary of monthly payroll costs

**Summary Section:**
- **Headcount:** Total Employees (Active)
- **Gross Payroll:** Total Basic + Allowances
- **Total Earnings:** All earning components
- **Total Deductions:** NSSF + PAYE + HESLB + Loans + Other
- **Net Salary Paid:** Amount transferred to employees
- **Employer Costs:**
  - NSSF/PSSF Employer Contribution
  - SDL
  - WCF
  - Total Employer Costs
- **TOTAL PAYROLL COST:** Gross + Employer Costs

**Department Breakdown Table:**
- Department | Headcount | Gross Salary | Employer Costs | Total Cost | % of Total

**Cost Components Breakdown:**
- Basic Salary: Amount (% of Total)
- Allowances: Amount (% of Total)
- NSSF Employee: Amount
- PAYE: Amount
- HESLB: Amount
- Net Paid: Amount
- Employer Statutory: Amount (% of Total)

**Month Comparison:**
- Previous Month | Current Month | Change (Amount) | Change (%)

**Filters:**
- Company (required)
- Payroll Period (required)
- Department (optional)
- Compare with Previous Month (checkbox)

---

### ❌ 7. Salary Register (Detailed) (PRIORITY 1)
**Report Name:** `Salary Register`
**Folder:** `tanzania/tanzania/report/salary_register/`
**Users:** HR Manager, Payroll Officer, Finance Manager

**Purpose:** Complete employee-wise salary breakdown for payroll verification

**Columns:**
1. Employee ID
2. Employee Name
3. Department
4. Designation
5. Basic Salary
6. Allowances (breakdown if needed)
7. **Gross Salary**
8. NSSF/PSSF (Employee 10%/5%)
9. **Taxable Income**
10. PAYE Tax
11. HESLB (15% if applicable)
12. Loan Deductions
13. Other Deductions
14. **Total Deductions**
15. **Net Salary**
16. Employer NSSF/PSSF
17. Employer SDL (3.5%)
18. Employer WCF (0.5%)
19. **Total Employer Cost**
20. **Cost to Company (CTC)**

**Summary Row:**
- Totals for all numeric columns

**Filters:**
- Company (required)
- Payroll Period (required)
- Department (optional)
- Branch (optional)
- Employee (optional - for single employee slip)
- Employment Type (Primary/Secondary/All)

**Export:** Excel, PDF, CSV

---

### ❌ 8. Payroll Cost Analysis (PRIORITY 2)
**Report Name:** `Payroll Cost Analysis`
**Folder:** `tanzania/tanzania/report/payroll_cost_analysis/`
**Users:** CEO, CFO, HR Director

**Purpose:** Strategic payroll cost management

**Cost Distribution (Pie Chart + Table):**
- Direct Salary (Basic + Allowances): Amount | %
- Employee Deductions (NSSF, PAYE): Amount | %
- Employer Statutory (NSSF, SDL, WCF): Amount | %
- Net to Employees: Amount | %

**Trend Analysis (Last 12 Months - Line Chart):**
- Month | Gross Payroll | Employer Costs | Total Cost | Headcount | Cost per Employee

**Budget vs Actual (if budget exists):**
- Budget Amount
- Actual Amount
- Variance (Amount)
- Variance (%)
- Status (Over/Under Budget)

**Department Cost Distribution (Bar Chart):**
- Department | Total Cost | % of Total | Headcount | Cost per Employee

**Key Metrics:**
- Average Salary per Employee
- Average Statutory Cost per Employee
- Payroll Cost as % of Revenue (if revenue data available)
- Month-over-Month Change (%)

**Filters:**
- Company (required)
- Payroll Period (required)
- Show Trend (Last 6/12 months)
- Include Budget Comparison (checkbox)

---

### ❌ 9. Employee Salary Slip (PRIORITY 1)
**Report Name:** `Employee Salary Slip`
**Folder:** `tanzania/tanzania/report/employee_salary_slip/`
**Users:** All Employees (Own), HR, Payroll

**Purpose:** Individual monthly salary statement

**Format (Print/PDF):**

```
═══════════════════════════════════════════════════════════
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
Employee TIN:       [TIN]         Bank Account:   [Account]
Pay Period:         [From - To]   Payment Date:   [Date]
───────────────────────────────────────────────────────────

EARNINGS                                          Amount (TZS)
───────────────────────────────────────────────────────────
Basic Salary                                      [Amount]
Allowances                                        [Amount]
Transport Allowance                               [Amount]
Other Earnings                                    [Amount]
                                                 ──────────
GROSS SALARY                                      [Amount]
═══════════════════════════════════════════════════════════

DEDUCTIONS                                        Amount (TZS)
───────────────────────────────────────────────────────────
NSSF/PSSF (10%/5%)                               [Amount]
PAYE Tax                                         [Amount]
HESLB (15%)                                      [Amount]
Loan Deduction                                   [Amount]
Other Deductions                                 [Amount]
                                                 ──────────
TOTAL DEDUCTIONS                                 [Amount]
───────────────────────────────────────────────────────────

NET SALARY PAYABLE                               [Amount]
═══════════════════════════════════════════════════════════

EMPLOYER CONTRIBUTIONS (Not Paid to Employee)
───────────────────────────────────────────────────────────
NSSF/PSSF Employer (10%/15%)                     [Amount]
Skills Development Levy (3.5%)                   [Amount]
Workers Compensation Fund (0.5%)                 [Amount]
                                                 ──────────
TOTAL EMPLOYER COST                              [Amount]
═══════════════════════════════════════════════════════════

TOTAL COST TO COMPANY (CTC)                      [Amount]
═══════════════════════════════════════════════════════════

PAYMENT DETAILS
Bank: [Bank Name]
Account Number: [Account]
Payment Method: Bank Transfer
Payment Date: [Date]

This is a system-generated salary slip.
Generated on: [DateTime]
───────────────────────────────────────────────────────────
```

**Filters:**
- Company (required)
- Employee (required)
- Payroll Period (required)

**Features:**
- Email to employee
- Download PDF
- Print ready format
- Show/Hide employer costs (option)

---

## CATEGORY 3: STATUTORY COMPLIANCE REPORTS (4 Reports)

### ❌ 10. NSSF Contribution Report (PRIORITY 1)
**Report Name:** `NSSF Contribution Report`
**Folder:** `tanzania/tanzania/report/nssf_contribution_report/`
**Due:** Monthly by 30th
**Users:** HR Manager, Payroll Officer

**Purpose:** NSSF Form CON.5 preparation and submission

**Header:**
- Company Name | TIN | VRN
- NSSF Employer Number
- Period: [Month Year]
- Report Date: [Date]

**Employee Contribution Table:**
| # | Employee Name | NSSF Number | Basic+Allowances | Employee (10%) | Employer (10%) | Total | Running Total |
|---|---------------|-------------|------------------|----------------|----------------|-------|---------------|
| 1 | ...           | ...         | ...              | ...            | ...            | ...   | ...           |

**Summary:**
- Total Employees Contributing: [Count]
- Total Contributory Salary: TZS [Amount]
- Total Employee Contributions (10%): TZS [Amount]
- Total Employer Contributions (10%): TZS [Amount]
- **GRAND TOTAL PAYABLE TO NSSF: TZS [Amount]**

**Payment Details:**
- Due Date: 30th [Month Year]
- Payment Reference: [Reference]
- Bank Details: [NSSF Bank Account]

**Filters:**
- Company (required)
- Payroll Period (required)
- Department (optional)

**Export:** PDF (for NSSF), Excel

---

### ❌ 11. WCF Contribution Report (PRIORITY 1)
**Report Name:** `WCF Contribution Report`
**Folder:** `tanzania/tanzania/report/wcf_contribution_report/`
**Due:** Monthly by 30th
**Users:** HR Manager, Compliance Officer

**Purpose:** WCF monthly return submission

**Header:**
- Company Name | TIN | VRN
- WCF Registration Number
- Period: [Month Year]
- Report Date: [Date]

**Employee Contribution Table:**
| # | Employee ID | Employee Name | Gross Salary | WCF Rate | WCF Amount |
|---|-------------|---------------|--------------|----------|------------|
| 1 | ...         | ...           | ...          | 0.5%     | ...        |

**Summary:**
- Total Employees: [Count]
- Total Payroll Base: TZS [Amount]
- WCF Rate: 0.5%
- **TOTAL WCF PAYABLE: TZS [Amount]**

**Payment Details:**
- Due Date: 30th [Month Year]
- Payment Reference: [Reference]

**Filters:**
- Company (required)
- Payroll Period (required)
- Department (optional)

**Export:** PDF, Excel

---

### ❌ 12. HESLB Deduction Report (PRIORITY 2)
**Report Name:** `HESLB Deduction Report`
**Folder:** `tanzania/tanzania/report/heslb_deduction_report/`
**Due:** Monthly by 30th
**Users:** HR Manager, Payroll Officer

**Purpose:** Student loan remittance tracking

**Header:**
- Company Name | TIN
- Period: [Month Year]

**Employee Deduction Table:**
| # | Employee ID | Employee Name | HESLB Loan No | Gross Salary | Rate | Deduction Amount |
|---|-------------|---------------|---------------|--------------|------|------------------|
| 1 | ...         | ...           | ...           | ...          | 15%  | ...              |

**Summary:**
- Total Employees with HESLB Loans: [Count]
- Total Salary Base: TZS [Amount]
- **TOTAL HESLB DEDUCTIONS: TZS [Amount]**

**Remittance Status:**
- Amount Deducted: TZS [Amount]
- Amount Remitted: TZS [Amount]
- Outstanding: TZS [Amount]
- Payment Date: [Date]
- Payment Reference: [Reference]

**Filters:**
- Company (required)
- Payroll Period (required)
- Remittance Status (All/Pending/Paid)

**Export:** PDF, Excel

---

### ❌ 13. Statutory Payment Tracking (PRIORITY 2)
**Report Name:** `Statutory Payment Tracking`
**Folder:** `tanzania/tanzania/report/statutory_payment_tracking/`
**Users:** CFO, Finance Manager, Compliance Officer

**Purpose:** Track all statutory payment obligations and compliance

**Payment Tracking Table:**
| Obligation | Period | Due Date | Amount Due | Payment Date | Amount Paid | Payment Ref | Days Late | Penalty | Status |
|------------|--------|----------|------------|--------------|-------------|-------------|-----------|---------|--------|
| PAYE       | Jan-24 | 07-Feb   | 5,000,000  | 05-Feb       | 5,000,000   | PAY001      | 0         | 0       | Paid   |
| SDL        | Jan-24 | 07-Feb   | 1,750,000  | 05-Feb       | 1,750,000   | PAY001      | 0         | 0       | Paid   |
| VAT        | Jan-24 | 20-Feb   | 3,200,000  | -            | 0           | -           | 5         | ?       | Overdue|
| NSSF       | Jan-24 | 30-Feb   | 4,500,000  | -            | 0           | -           | -         | -       | Pending|
| WCF        | Jan-24 | 30-Feb   | 225,000    | -            | 0           | -           | -         | -       | Pending|
| HESLB      | Jan-24 | 30-Feb   | 450,000    | -            | 0           | -           | -         | -       | Pending|

**Summary Cards:**
- **Paid on Time:** [Count] | TZS [Amount] | [%]
- **Overdue:** [Count] | TZS [Amount] | [%]
- **Pending (Not Due):** [Count] | TZS [Amount] | [%]
- **Total Penalties:** TZS [Amount]
- **Compliance Rate:** [%]

**Status Legend:**
- 🟢 Paid (On Time)
- 🟡 Pending (Not Yet Due)
- 🔴 Overdue (Payment Required)

**Filters:**
- Company (required)
- Period (From Date - To Date)
- Obligation Type (All/PAYE/SDL/VAT/NSSF/WCF/HESLB)
- Status (All/Paid/Overdue/Pending)

**Export:** PDF, Excel

---

## IMPLEMENTATION PRIORITY SEQUENCE

### Phase 1 (Week 1) - CRITICAL COMPLIANCE REPORTS
**Must complete before month-end:**
1. PAYE & SDL Report (Due 7th)
2. Monthly Payroll Summary
3. Salary Register
4. Employee Salary Slip

### Phase 2 (Week 2) - STATUTORY REPORTS
**Must complete before 30th:**
5. NSSF Contribution Report
6. WCF Contribution Report
7. Tax Compliance Summary Dashboard

### Phase 3 (Week 3) - MANAGEMENT REPORTS
**For strategic decision-making:**
8. Payroll Cost Analysis
9. HESLB Deduction Report
10. Statutory Payment Tracking

---

## EXCLUDED REPORTS (Can Wait)

### Postponed to Phase 4 (Future):
- CEO Dashboard (Report #4 category)
- CFO Dashboard (Report #4 category)
- HR Director Dashboard (Report #4 category)
- Monthly Board Report (Report #4 category)
- Payroll Variance Analysis (Report #5 category)
- Department Payroll Analysis (Report #5 category)
- Employee CTC Report (Report #5 category)
- Tax Burden Analysis (Report #5 category)
- Payroll Audit Trail (Report #6 category)
- Employee Statutory Deductions Register (Report #6 category)
- Tax Compliance Certificate Status (Report #6 category)
- PSSF Contribution Report (if needed)
- SDL Compliance Report (covered in PAYE & SDL Report)
- WCF Annual Return (can be created from monthly reports)

**Reason for Postponement:** These are analytical/audit reports that can be derived from the primary reports or are needed less frequently.

---

## TECHNICAL SPECIFICATIONS

### Report File Structure
Each report needs:
```
tanzania/tanzania/report/[report_name]/
├── __init__.py
├── [report_name].py        # Python logic
├── [report_name].js         # Frontend filters
└── [report_name].json       # Report metadata
```

### Common Filters (All Reports)
- Company (Link to Company) - **Required**
- Payroll Period or Date Range - **Required**
- Department (Link to Department) - Optional
- Employee (Link to Employee) - Optional

### Export Formats Required
- PDF (for official submissions)
- Excel (for data manipulation)
- CSV (for data imports)

### Performance Considerations
- Use SQL queries for data retrieval (not ORM for large datasets)
- Add pagination for reports with >1000 rows
- Cache report data for 1 hour (especially dashboards)
- Add loading indicators for slow queries

### Access Control - Complete User Access Matrix

| Report Name | CEO | CFO | Finance Mgr | HR Director | HR Mgr | Payroll Officer | Tax Officer | Dept Manager | Supervisor | Employee/Worker |
|-------------|-----|-----|-------------|-------------|--------|----------------|-------------|--------------|------------|-----------------|
| **TAX REPORTS** |
| VAT Return Report | R | R | RW | - | - | - | RW | - | - | - |
| VAT Summary Report | R | R | RW | - | - | - | RW | - | - | - |
| Withholding Tax Report | R | R | RW | - | - | - | RW | - | - | - |
| PAYE & SDL Report | R | R | RW | R | RW | RW | RW | - | - | - |
| Tax Compliance Summary | R | R | R | - | - | - | R | - | - | - |
| **PAYROLL REPORTS** |
| Monthly Payroll Summary | R | R | R | R | RW | R | - | R (Own Dept) | R (Own Team) | - |
| Salary Register | R | R | R | R | RW | RW | - | R (Own Dept) | - | - |
| Payroll Cost Analysis | R | R | R | R | R | - | - | R (Own Dept) | - | - |
| Employee Salary Slip | R | R | R | R | RW | RW | - | R (Own Dept) | R (Own Team) | **R (Own Only)** |
| **STATUTORY REPORTS** |
| NSSF Contribution Report | R | R | R | R | RW | RW | - | - | - | - |
| WCF Contribution Report | R | R | R | R | RW | RW | - | - | - | - |
| HESLB Deduction Report | R | R | R | R | RW | RW | - | - | - | - |
| Statutory Payment Tracking | R | R | RW | R | R | - | R | - | - | - |

**Legend:**
- **R** = Read Only (Can view report)
- **RW** = Read/Write (Can view and generate report)
- **-** = No Access
- **(Own Only)** = Can only view their own record
- **(Own Dept)** = Can only view their department's data
- **(Own Team)** = Can only view their team's data

**Role Descriptions:**
- **CEO:** Full visibility across all reports for strategic oversight
- **CFO:** Full visibility, can export/print for board meetings
- **Finance Manager:** Manages tax compliance and financial reports
- **HR Director:** Strategic HR oversight, read-only access
- **HR Manager:** Full payroll management and statutory compliance
- **Payroll Officer:** Day-to-day payroll processing and reporting
- **Tax Officer:** Tax filing and compliance specialist
- **Department Manager:** Can view payroll costs for their department only
- **Supervisor:** Can view salary slips for direct reports only
- **Employee/Worker:** Self-service access to own salary slip

---

## EMPLOYEE/WORKER SELF-SERVICE PORTAL

### What Employees/Workers Can Access

**Primary Report: Employee Salary Slip (Self-Service)**

Every employee/worker gets:
1. **Monthly Salary Slip Access**
   - View current month salary slip
   - View historical slips (past 12 months)
   - Download PDF for personal records
   - Print salary slip
   - Email to personal email

2. **Salary Slip Contents:**
   - Personal earnings breakdown
   - All deductions explained
   - Net salary calculation
   - Employer contributions (informational)
   - Payment details (bank, date)
   - Year-to-date (YTD) totals

3. **Self-Service Features:**
   - No need to request from HR
   - Available 24/7 online
   - Mobile-friendly view
   - Secure access (own records only)
   - Multi-language support (English/Swahili)

4. **Privacy & Security:**
   - Employees can ONLY see their own salary slips
   - Cannot see other employees' salaries
   - Secure login required
   - Audit trail of all accesses
   - Download history tracked

### Employee Portal Access Flow

```
Employee Login → ESS Portal → Payroll → Salary Slips
                              ↓
                    Select Month (dropdown)
                              ↓
                    View/Download/Print/Email
```

### Implementation Notes for Employee Access

**Technical Requirements:**
- Add Employee Portal module
- Restrict query to `employee = frappe.session.user`
- Add download counter
- Email functionality
- Mobile responsive design

**User Training:**
- Simple 5-minute video tutorial
- FAQ document
- HR helpdesk for support
- Posters with QR code to salary slip portal

**Benefits for Workers:**
- **Transparency:** See exactly how salary is calculated
- **Convenience:** No need to wait for HR to print
- **Planning:** Can download for loan applications, visa, etc.
- **Record Keeping:** Keep historical records
- **Verification:** Verify bank payment matches slip

**Benefits for HR:**
- Reduce HR workload (no manual slip printing)
- Reduce paper usage
- Reduce employee queries
- Automatic distribution
- Better employee satisfaction

---

## SUCCESS METRICS

### Compliance Success:
- ✅ All statutory reports filed on time (100% compliance)
- ✅ Zero penalties for late filing
- ✅ All employee queries resolved using salary slips

### Management Success:
- ✅ CEO gets monthly payroll summary in 5 minutes
- ✅ CFO tracks all tax obligations in one dashboard
- ✅ HR verifies payroll accuracy before payment

### User Adoption:
- ✅ 90% of users can generate reports without training
- ✅ Reports load in <5 seconds
- ✅ Export to PDF/Excel works flawlessly

---

## NEXT STEPS

1. ✅ Review and approve priority report list
2. Start implementation with Phase 1 (PAYE & SDL Report first)
3. Create report templates and layouts
4. Implement data queries and calculations
5. Add export functionality
6. Test with sample data
7. User acceptance testing
8. Deploy to production
9. Train users
10. Monitor usage and gather feedback
