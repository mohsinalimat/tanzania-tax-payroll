# Tanzania Reports - TO DO LIST

## PHASE 1: CRITICAL REPORTS (Week 1) - MUST DO FIRST

### 1. PAYE & SDL Report ⚠️ URGENT - TRA Deadline 7th
**Location:** `tanzania/tanzania/report/paye_sdl_report/`
**Purpose:** Monthly PAYE and SDL filing to TRA
**Users:** HR Manager, CFO, Payroll Officer, Tax Officer
**Priority:** P0 - CRITICAL

**Create files:**
- [x] `__init__.py`
- [x] `paye_sdl_report.json`
- [x] `paye_sdl_report.py`
- [x] `paye_sdl_report.js`

**Must include:**
- [x] PAYE by tax bracket (0%, 8%, 20%, 25%, 30%)
- [x] SDL calculation (3.5%)
- [x] Employee-wise breakdown
- [x] Export to PDF for TRA
- [x] Export to Excel

---

### 2. NSSF Contribution Report ⚠️ URGENT - NSSF Deadline 30th
**Location:** `tanzania/tanzania/report/nssf_contribution_report/`
**Purpose:** NSSF Form CON.5 submission
**Users:** HR Manager, Payroll Officer
**Priority:** P0 - CRITICAL

**Create files:**
- [x] `__init__.py`
- [x] `nssf_contribution_report.json`
- [x] `nssf_contribution_report.py`
- [x] `nssf_contribution_report.js`

**Must include:**
- [x] Employee + Employer contributions (10% each)
- [x] Running total
- [x] Only NSSF registered employees
- [x] Export to PDF for NSSF

---

### 3. WCF Contribution Report ⚠️ URGENT - WCF Deadline 30th
**Location:** `tanzania/tanzania/report/wcf_contribution_report/`
**Purpose:** WCF monthly return
**Users:** HR Manager, Compliance Officer
**Priority:** P0 - CRITICAL

**Create files:**
- [x] `__init__.py`
- [x] `wcf_contribution_report.json`
- [x] `wcf_contribution_report.py`
- [x] `wcf_contribution_report.js`

**Must include:**
- [x] All employees (0.5% rate)
- [x] Employer-only contribution
- [x] Export to PDF for WCF

---

### 4. Employee Salary Slip (Custom Print Format) ⚠️ CRITICAL - ALL EMPLOYEES
**Location:** `tanzania/tanzania/print_format/tanzania_salary_slip/`
**Purpose:** Monthly salary statement for ALL employees
**Users:** ALL EMPLOYEES (self-service), HR, Payroll
**Priority:** P0 - CRITICAL

**Create files:**
- [x] `__init__.py`
- [x] `tanzania_salary_slip.html` (Jinja2 + CSS)

**Must include:**
- [x] Company header with TIN/VRN
- [x] Employee details
- [x] Earnings breakdown
- [x] Deductions breakdown
- [x] Net salary
- [x] Employer contributions (informational)
- [x] Year-to-date totals
- [x] Payment details
- [x] Print-friendly format
- [x] PDF download
- [x] Email functionality
- [x] Self-service access (employees see own only)

---

### 5. Monthly Payroll Summary
**Location:** `tanzania/tanzania/report/monthly_payroll_summary/`
**Purpose:** Executive payroll summary
**Users:** CEO, CFO, HR Director
**Priority:** P0 - CRITICAL

**Create files:**
- [x] `__init__.py`
- [x] `monthly_payroll_summary.json`
- [x] `monthly_payroll_summary.py`
- [x] `monthly_payroll_summary.js`

**Must include:**
- [x] Summary metrics (headcount, costs)
- [x] Cost breakdown
- [x] Statutory deductions
- [x] Department breakdown
- [x] Month-over-month comparison
- [x] Charts/graphs

---

## PHASE 2: IMPORTANT REPORTS (Week 2)

### 6. Statutory Payment Tracking
**Location:** `tanzania/tanzania/report/statutory_payment_tracking/`
**Priority:** P1

**Create files:**
- [ ] `__init__.py`
- [ ] `statutory_payment_tracking.json`
- [ ] `statutory_payment_tracking.py`
- [ ] `statutory_payment_tracking.js`

---

### 7. PAYE Computation Report
**Location:** `tanzania/tanzania/report/paye_computation_report/`
**Priority:** P1

---

### 8. Department Wise Payroll
**Location:** `tanzania/tanzania/report/department_wise_payroll/`
**Priority:** P1

---

### 9. HESLB Deduction Report
**Location:** `tanzania/tanzania/report/heslb_deduction_report/`
**Priority:** P1

---

## PHASE 3: STRATEGIC REPORTS (Week 3)

### 10. Payroll Cost Analysis
**Location:** `tanzania/tanzania/report/payroll_cost_analysis/`
**Priority:** P2

---

### 11. Tax Payment Summary
**Location:** `tanzania/tanzania/report/tax_payment_summary/`
**Priority:** P2

---

### 12. PSSF Contribution Report
**Location:** `tanzania/tanzania/report/pssf_contribution_report/`
**Priority:** P3

---

### 13. SDL Compliance Report
**Location:** `tanzania/tanzania/report/sdl_compliance_report/`
**Priority:** P3

---

### 14. WCF Annual Return
**Location:** `tanzania/tanzania/report/wcf_annual_return/`
**Priority:** P3

---

## COMPLETION CHECKLIST

### Week 1 (Critical)
- [x] PAYE & SDL Report
- [x] NSSF Contribution Report
- [x] WCF Contribution Report
- [x] Employee Salary Slip
- [x] Monthly Payroll Summary

### Week 2 (Important)
- [ ] Statutory Payment Tracking
- [ ] PAYE Computation Report
- [ ] Department Wise Payroll
- [ ] HESLB Deduction Report

### Week 3 (Strategic)
- [ ] Payroll Cost Analysis
- [ ] Tax Payment Summary
- [ ] PSSF Contribution Report
- [ ] SDL Compliance Report
- [ ] WCF Annual Return

---

## TESTING CHECKLIST

For each report:
- [ ] Test with sample data
- [ ] Test filters
- [ ] Test export to PDF
- [ ] Test export to Excel
- [ ] Test role permissions
- [ ] Test on mobile (for salary slip)
- [ ] User acceptance testing
- [ ] Documentation created

---

## START HERE

**Begin with:** PAYE & SDL Report (most urgent - due 7th)
**Then:** Employee Salary Slip (most users - ALL employees)
**Then:** NSSF & WCF reports (due 30th)

**Use this order:**
1. PAYE & SDL Report
2. Employee Salary Slip
3. NSSF Report
4. WCF Report
5. Monthly Payroll Summary

This order ensures:
- Government compliance first
- Employee needs second
- Management reporting last
