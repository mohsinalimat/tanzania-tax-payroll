# Tanzania Tax & Payroll Compliance ERPNext App

Complete tax and payroll compliance solution for Tanzania businesses, fully integrated with ERPNext.

## Overview

This app provides comprehensive tax and payroll compliance for businesses operating in Tanzania, including:

- **VAT Management** (18% standard rate)
- **PAYE Income Tax** (5-tier progressive system)
- **NSSF & PSSF** (Social Security contributions)
- **SDL** (Skills Development Levy - 3.5%)
- **WCF** (Workers Compensation Fund - 0.5%)
- **HESLB** (Student Loan deductions - 15%)
- **Withholding Tax** tracking
- **Automated Payroll Processing**
- **TRA Compliance** (Tanzania Revenue Authority)

---

## Features

### Tax Compliance Module

#### ✅ VAT (Value Added Tax)
- 18% standard rate tax templates
- Zero-rated and exempt item templates
- Input VAT and Output VAT tracking
- Ready for EFDMS integration (Electronic Fiscal Device Management System)
- Monthly VAT return preparation

#### ✅ PAYE (Pay As You Earn) Income Tax
- 5-tier progressive tax system:
  - 0% on income up to TZS 270,000
  - 8% on TZS 270,001 - 520,000
  - 20% on TZS 520,001 - 760,000
  - 25% on TZS 760,001 - 1,000,000
  - 30% on income above TZS 1,000,000
- Secondary employment flat rate (30%)
- Automatic monthly PAYE calculation

#### ✅ Corporate Tax
- CIT (Corporate Income Tax) tracking
- Quarterly provisional tax payments
- Annual return preparation

#### ✅ Withholding Tax
- Dividend withholding (5-10% based on ownership)
- Service fee withholding (5% resident, 15% non-resident)
- Automated tracking and reporting

### Payroll Compliance Module

#### ✅ NSSF (National Social Security Fund)
- Employee contribution: 10%
- Employer contribution: 10%
- Pre-tax deduction
- Monthly payment tracking (due 30th)

#### ✅ PSSF (Public Service Social Security Fund)
- Employee contribution: 5%
- Employer contribution: 15%
- Pre-tax deduction
- Monthly payment tracking (due 30th)

#### ✅ SDL (Skills Development Levy)
- 3.5% employer-only contribution
- Applicable to companies with 10+ employees
- Monthly payment (due 7th)

#### ✅ WCF (Workers Compensation Fund)
- 0.5% employer-only contribution
- Monthly payment (due 30th)
- Annual return (due March 31; period Mar 1 - Feb 28)

#### ✅ HESLB (Student Loans)
- 15% salary deduction for eligible employees
- Monthly remittance tracking

#### ✅ Salary Components
- Basic Salary
- Allowances (General, Transport, etc.)
- Incentives
- Leave Encashment
- All statutory deductions
- Employee advances and loan recovery

---

## Installation

### Prerequisites
- ERPNext v14, v15, or v16
- HRMS v14, v16, or v16
- Frappe Bench

### Install via Bench

```bash
# Navigate to your bench directory
cd /path/to/your/bench

# Get the app from repository
bench get-app https://github.com/nelsonmpanju/tanzania.git

# Install on your site
bench --site your-site-name install-app tanzania

# Run migrations
bench --site your-site-name migrate

# Restart bench
bench restart
```

### What Gets Installed Automatically

When you install the Tanzania app, the following are created automatically:

#### 1. Tax Accounts (11 accounts)
- Output VAT 18% (Liability)
- Input VAT 18% (Asset)
- VAT Payable (Liability)
- VAT Receivable (Asset)
- PAYE Payable (Liability)
- SDL Payable (Liability)
- NSSF Payable (Liability)
- WCF Payable (Liability)
- Withholding Tax Payable (Liability)
- Withholding Tax Receivable (Asset)
- Tax Expenses (Expense)

#### 2. Payroll Accounts
**Expense Accounts:**
- Salary and Wages Expenses
- Transport Allowance
- Leave Encashment
- NSSF - Employer Contribution
- PSSF - Employer Contribution
- SDL - Employer Contribution
- WCF Expense
- Additional Salary

**Liability Accounts:**
- Salaries Payable (group)
- Payroll Payable
- HELSB Payable Account

**Asset Accounts:**
- Loans and Advances (Assets) (group)
- Employee Advances
- Employee Loan
- Loan Payment
- Employee Deductions

#### 3. Tax Categories
- Standard Rated (18%)
- Zero Rated (0%)
- Exempt
- Out of Scope

#### 4. Tax Templates
**Sales Tax Templates:**
- Tanzania VAT 18% (default)
- Tanzania Zero Rated

**Purchase Tax Templates:**
- Tanzania Purchase VAT 18% (default)
- Tanzania Purchase Zero Rated

**Item Tax Templates:**
- Tanzania VAT 18%
- Tanzania Zero Rated
- Tanzania Exempt
- Tanzania Purchase VAT 18%
- Tanzania Purchase Zero Rated

#### 5. Salary Components (23 components)
All salary components are created with correct accounting mappings for earnings and deductions.

#### 6. Default Salary Structure
"Tanzania Default Salary Structure" with all PAYE tiers, NSSF/PSSF formulas, and statutory deductions.

#### 7. Custom Fields
**Employee:**
- NSSF Registered (checkbox)
- PSSF Registered (checkbox)
- HESLB Loan (checkbox)
- Employment Type (Primary/Secondary)

**Company, Customer, Supplier:**
- TIN (Tax Identification Number)
- VRN (VAT Registration Number)
- Tax Office

**Sales Invoice, Purchase Invoice:**
- Auto-fetched TIN/VRN fields

---

## Quick Start Guide

### Step 1: Configure Company Information

1. Go to **Company** master
2. Fill in Tanzania tax information:
   - TIN (Tax Identification Number)
   - VRN (VAT Registration Number)
   - Tax Office

### Step 2: Setup Customers and Suppliers

1. Add TIN and VRN to existing customers/suppliers
2. Assign appropriate tax categories:
   - Standard Rated (most common)
   - Zero Rated (exports, certain essentials)
   - Exempt (financial services, education)

### Step 3: Configure Items

1. Assign tax templates to items:
   - **Standard items:** Tanzania VAT 18%
   - **Zero-rated items:** Tanzania Zero Rated
   - **Exempt items:** Tanzania Exempt

### Step 4: Setup Employees for Payroll

1. Go to **Employee** master
2. Fill in Tanzania payroll information:
   - ✅ Check **NSSF Registered** (for NSSF contributors)
   - ✅ Check **PSSF Registered** (for public service employees)
   - ✅ Check **HESLB Loan** (if employee has student loan)
   - Select **Employment Type:**
     - **Primary:** Regular employment (5-tier PAYE)
     - **Secondary:** Second job (30% flat PAYE)

### Step 5: Assign Salary Structure

1. Go to **Salary Structure Assignment**
2. Select employee
3. Choose **"Tanzania Default Salary Structure"**
4. Set **Base Salary** (monthly gross)
5. Add any **Allowances** (optional)
6. Submit

### Step 6: Process Monthly Payroll

1. Go to **Payroll Entry**
2. Select **Payroll Period** (month)
3. Select **Posting Date**
4. Click **Get Employees**
5. System automatically calculates:
   - NSSF/PSSF (employee + employer)
   - PAYE (based on 5-tier system)
   - SDL (if ≥10 employees)
   - WCF (0.5%)
   - HESLB (if applicable)
6. Review calculations
7. **Create Salary Slips**
8. **Submit** payroll
9. **Make Bank Entry** for salary payments

### Step 7: Monthly Compliance

#### By 7th of Following Month:
- Pay and file **PAYE** to TRA
- Pay and file **SDL** to TRA (if applicable)

#### By 20th of Following Month:
- Pay and file **VAT** to TRA

#### By 30th of Following Month:
- Pay **NSSF** contributions
- Submit NSSF Form CON.5
- Pay **WCF** contributions
- Submit WCF monthly return
- Pay **HESLB** deductions

---

## Tax Calculation Examples

### Example 1: PAYE Calculation (Primary Employment)

**Employee Salary:**
- Base Salary: TZS 1,500,000
- Allowance: TZS 300,000
- **Gross Salary: TZS 1,800,000**

**Step 1: NSSF Deduction (10%)**
- NSSF = 1,800,000 × 10% = TZS 180,000

**Step 2: Taxable Income**
- Taxable Income = 1,800,000 - 180,000 = TZS 1,620,000

**Step 3: PAYE Tax (5-tier)**
- First 270,000: 0% = 0
- Next 250,000 (270K-520K): 8% = 20,000
- Next 240,000 (520K-760K): 20% = 48,000
- Next 240,000 (760K-1M): 25% = 60,000
- Remaining 620,000 (>1M): 30% = 186,000
- **Total PAYE = TZS 314,000**

**Step 4: Net Salary**
- Net = 1,800,000 - 180,000 (NSSF) - 314,000 (PAYE)
- **Net Salary = TZS 1,306,000**

**Employer Costs:**
- NSSF Employer: TZS 180,000 (10%)
- SDL: TZS 63,000 (3.5%)
- WCF: TZS 9,000 (0.5%)
- **Total Employer Cost = TZS 2,052,000**

### Example 2: Secondary Employment

**Employee Salary:** TZS 800,000

**PAYE Calculation:**
- NSSF: 800,000 × 10% = TZS 80,000
- Taxable: 800,000 - 80,000 = TZS 720,000
- **PAYE: 720,000 × 30% = TZS 216,000** (flat rate)

---

## Reports

### Tax Reports
- VAT Return Report (monthly)
- PAYE/SDL Report (monthly - due 7th)
- Withholding Tax Report

### Payroll Reports
- Monthly Payroll Summary
- NSSF Contribution Report (due 30th)
- WCF Contribution Report (due 30th)
- HESLB Deduction Report
- Leave Balance Report
- Salary Register

---

## Compliance Deadlines

| Date | Obligation | Department | Frequency |
|------|-----------|------------|-----------|
| **7th** | PAYE + SDL payment & filing | TRA | Monthly |
| **20th** | VAT payment & filing | TRA | Monthly |
| **30th** | NSSF payment (Form CON.5) | NSSF | Monthly |
| **30th** | WCF payment + return | WCF | Monthly |
| **31st March** | Q1 CIT provisional (25%) | TRA | Quarterly |
| **30th June** | Q2 CIT + Final return | TRA | Quarterly |
| **30th September** | Q3 CIT provisional (25%) | TRA | Quarterly |
| **31st December** | Q4 CIT provisional (25%) | TRA | Quarterly |
| **31st March** | WCF Annual Return | WCF | Annually (Mar 1 - Feb 28) |

---

## Customization

### Adding Custom Salary Components

1. Go to **Salary Component**
2. Click **New**
3. Set component details:
   - Name, abbreviation, type (Earning/Deduction)
   - Formula (if applicable)
   - Tax applicability
4. Link to appropriate account
5. Add to salary structure

### Modifying PAYE Brackets

If TRA updates tax brackets:

1. Go to **Salary Structure**
2. Edit "Tanzania Default Salary Structure"
3. Update PAYE deduction formulas
4. Update conditions
5. Save

---

## Troubleshooting

### Issue: Accounts not created after installation

**Solution:**
```bash
# Run migrate again
bench --site your-site-name migrate

# Or run setup manually from console
bench --site your-site-name console
>>> from tanzania.install import setup_tanzania_taxes, setup_tanzania_payroll_system
>>> setup_tanzania_taxes()
>>> setup_tanzania_payroll_system()
```

### Issue: PAYE calculation incorrect

**Check:**
1. Employee has NSSF/PSSF checked
2. Employment Type is set correctly (Primary/Secondary)
3. Salary structure is assigned
4. Formulas in salary structure match current tax law

### Issue: Salary component account missing

**Solution:**
1. Go to **Salary Component**
2. Open the component
3. Check "Accounts" table
4. Add missing company and account mapping
5. Save

---

## Integration (Future Enhancements)

### Planned Integrations:

1. **TRA iTax Portal**
   - Automated PAYE/SDL return filing
   - Automated CIT return filing
   - OAuth 2.0 authentication

2. **EFDMS (Electronic Fiscal Device)**
   - Invoice validation
   - QR code generation
   - Real-time VAT tracking

3. **NSSF Portal**
   - Form CON.5 auto-submission
   - Contribution verification
   - Maternity benefit eligibility check

4. **WCF Portal**
   - Monthly return submission
   - Annual return submission
   - Coverage certificate tracking

5. **Banking Gateway**
   - Salary payment batch files
   - Tax payment integration
   - Automated reconciliation

---

## Support & Contact

### Tanzania Revenue Authority (TRA)
- Website: https://www.tra.go.tz
- iTax Portal: https://itax.tra.go.tz
- Support: +255 111 113 333

### NSSF
- Website: https://www.nssf.go.tz
- Support: +255 22 219 2000

### WCF
- Website: https://www.wcf.go.tz
- Support: +255 22 241 5000

---

## Contributing

This app uses `pre-commit` for code formatting and linting.

### Setup Development Environment

```bash
cd apps/tanzania
pre-commit install
```

Pre-commit is configured to use:
- ruff (Python linting)
- eslint (JavaScript linting)
- prettier (Code formatting)
- pyupgrade (Python syntax upgrading)

### Running Tests

```bash
# Run all tests
bench --site your-site-name run-tests --app tanzania

# Run specific test
bench --site your-site-name run-tests --app tanzania --module tanzania.tests.test_paye
```

---

## CI/CD

GitHub Actions workflows:
- **CI:** Runs unit tests on every push to `develop`
- **Linters:** Runs Frappe Semgrep Rules and pip-audit on PRs

---

## Changelog

### Version 1.0.0 (January 2026)
- Initial release
- Complete tax compliance (VAT, PAYE, CIT, WHT)
- Complete payroll compliance (NSSF, PSSF, SDL, WCF, HESLB)
- Automated account creation on installation
- Default salary structure with Tanzania tax rules
- Custom fields for tax and payroll compliance

---

## License

MIT License

Copyright (c) 2026 Nelson Mpanju

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Acknowledgments

- ERPNext team for the excellent framework
- Tanzania Revenue Authority for tax guidelines
- NSSF and WCF for contribution guidelines
- Tanzania business community for requirements and feedback

---

**Made with ❤️ for Tanzania businesses**
