# Tanzania Tax & Payroll - Setup Guide

This guide walks you through the complete setup process to get Tanzania Tax & Payroll working correctly for your business.

## Table of Contents

1. [Initial Setup](#1-initial-setup)
2. [Company Configuration](#2-company-configuration)
3. [Tax Setup](#3-tax-setup)
4. [EFD Integration](#4-efd-integration)
5. [Customer & Supplier Setup](#5-customer--supplier-setup)
6. [Item Configuration](#6-item-configuration)
7. [Payroll Setup](#7-payroll-setup)
8. [Running Payroll](#8-running-payroll)
9. [Generating Reports](#9-generating-reports)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Initial Setup

### 1.1 Install the App

```bash
bench get-app tanzania https://github.com/nelsonmpanju/tanzania.git
bench --site your-site install-app tanzania
bench migrate
bench build --app tanzania
bench restart
```

### 1.2 What Gets Created Automatically

After installation, the following are created automatically:

| Category | Items Created |
|----------|--------------|
| **Tax Accounts** | Output VAT 18%, Input VAT, PAYE Payable, SDL Payable, WCF Payable, HESLB Payable, PSSF Payable |
| **Payroll Accounts** | Salary Expenses, NSSF Employer, SDL Employer, WCF Expense, PSSF Employer |
| **Salary Components** | 25 components including Basic, NSSF, PSSF, PAYE, SDL, WCF, HESLB |
| **Tax Categories** | Standard Rate, Zero Rated, Exempt |

---

## 2. Company Configuration

### 2.1 Add Tanzania Tax Information

1. Go to **Setup > Company > [Your Company]**
2. Scroll to **Tanzania Tax Information** section
3. Fill in:
   - **TIN**: Your Tax Identification Number (e.g., 123-456-789)
   - **VRN**: VAT Registration Number (e.g., 40-123456-A)
   - **Tax Office**: Your TRA tax office location

> **Important**: TIN and VRN are required for EFD integration and will appear on all invoices.

---

## 3. Tax Setup

### 3.1 Understanding Tax Categories

Tanzania uses different VAT categories:

| Category | VAT Rate | Use Case |
|----------|----------|----------|
| **Standard Rate** | 18% | Most goods and services |
| **Zero Rated** | 0% | Exports, basic food items |
| **Exempt** | N/A | Education, health services |
| **Special Relief** | Variable | Government projects |

### 3.2 Configure Item Tax Templates

Item Tax Templates define which tax code applies to items for EFD receipts.

1. Go to **Tanzania > Tax Setup > Item Tax Template**
2. Create or edit templates:

**Example: Standard VAT Template**
```
Title: Tanzania VAT 18%
EFD Tax Code: A-Standard 18%
Tax Rates:
  - Tax Type: Output VAT 18% - [Company]
  - Tax Rate: 18%
```

**Example: Zero Rated Template**
```
Title: Tanzania Zero Rated
EFD Tax Code: C-Zero Rated
Tax Rates:
  - Tax Type: Output VAT 18% - [Company]
  - Tax Rate: 0%
```

**Example: Exempt Template**
```
Title: Tanzania Exempt
EFD Tax Code: E-Exempt
Tax Rates: (leave empty)
```

### 3.3 Configure Tax Rules (Automatic Tax Assignment)

Tax Rules automatically apply taxes based on customer/supplier type, item group, etc.

1. Go to **Tanzania > Tax Setup > Tax Rule**
2. Create rules for automatic tax application:

**Example: Standard Sales Tax Rule**
```
Tax Type: Sales
Tax Template: Tanzania Sales VAT 18%
Priority: 1
Filters: (leave empty for default)
```

**Example: Export Sales (Zero Rated)**
```
Tax Type: Sales
Tax Template: Tanzania Zero Rated
Priority: 2
Filters:
  - Tax Category: Zero Rated
```

### 3.4 Configure Sales Taxes and Charges Template

1. Go to **Tanzania > Tax Setup > Sales Taxes and Charges Template**
2. Create template:

```
Title: Tanzania VAT 18%
Company: [Your Company]
Is Default: Yes

Taxes:
  - Type: On Net Total
  - Account Head: Output VAT 18% - [Company]
  - Rate: 18%
  - Description: VAT 18%
```

### 3.5 Configure Purchase Taxes and Charges Template

1. Go to **Tanzania > Tax Setup > Purchase Taxes and Charges Template**
2. Create template:

```
Title: Tanzania Input VAT
Company: [Your Company]
Is Default: Yes

Taxes:
  - Type: On Net Total
  - Account Head: Input VAT - [Company]
  - Rate: 18%
  - Description: Input VAT 18%
```

### 3.6 Withholding Tax (WHT) Setup

Tanzania requires businesses to withhold tax on certain payments to suppliers. The app uses ERPNext's native **Tax Withholding Category** feature.

#### WHT Categories Created Automatically

| Category Name | WHT Rate | Use Case |
|--------------|----------|----------|
| Tanzania WHT 2% - Services | 2% | Service payments |
| Tanzania WHT 5% - Rent | 5% | Rent/Lease payments |
| Tanzania WHT 10% - Professional | 10% | Professional/Technical fees |
| Tanzania WHT 15% - Non-Resident | 15% | Payments to non-residents |

#### Setting Up WHT for a Supplier

1. Go to **Buying > Supplier > [Supplier Name]**
2. In the **Tax** section, set **Tax Withholding Category**
   - Example: Select "Tanzania WHT 2% - Services" for service suppliers
3. Save the supplier

#### Using WHT on Purchase Invoices

1. Create a new **Purchase Invoice**
2. Select a supplier with Tax Withholding Category set
3. Check **Apply Tax Withholding Amount** checkbox
4. Add your items and taxes as usual
5. The system will **automatically deduct WHT** from the invoice total
6. Submit the invoice

**Example Calculation:**
```
Net Total:           1,000,000 TZS
+ VAT 18%:             180,000 TZS
- WHT 2%:              -20,000 TZS (auto-calculated)
= Grand Total:       1,160,000 TZS
```

#### WHT Reporting

To view all WHT transactions:
1. Go to **Tanzania > Tax Report > ITX 219.03.E Withholding Tax**
2. Select your company and date range
3. The report shows all Purchase Invoices with WHT applied

> **Note**: The WHT report only shows data when suppliers have Tax Withholding Category assigned and Purchase Invoices are created with "Apply Tax Withholding Amount" checked.

---

## 4. EFD Integration

### 4.1 Get EFD Credentials

Contact one of the supported EFD providers to get your API credentials:

| Provider | Website | Notes |
|----------|---------|-------|
| **VFDPlus** | vfdplus.tz | Most popular |
| **TotalVFD** | totalvfd.tz | Alternative |
| **SimplifyVFD** | simplifyvfd.tz | Simplified option |

You will receive:
- API Key / Token
- Device Serial Number (optional - can be fetched)
- Sandbox credentials for testing

### 4.2 Configure EFD Settings

1. Go to **Tanzania > EFD Integration > EFD Settings**
2. Click **+ Add EFD Settings**
3. Fill in:

```
Company: [Your Company]
EFD Provider: VFDPlus (or your provider)
Environment: Sandbox (for testing) / Production (for live)

API Credentials:
  - API Key: [Your API Key from provider]
  - API Secret: [If required by provider]

Settings:
  - Enabled: Yes
  - Auto Submit on Invoice: Yes (recommended)
  - Max Retry Attempts: 3
```

4. Click **Fetch Device Info** to retrieve TIN/VRN from TRA
5. Save

### 4.3 Configure Mode of Payment for EFD

Each payment mode needs an EFD payment type:

1. Go to **Accounting > Mode of Payment**
2. Edit each payment mode and set **EFD Payment Type**:

| Mode of Payment | EFD Payment Type |
|----------------|------------------|
| Cash | CASH |
| Bank Transfer | EMONEY |
| Cheque | CHEQUE |
| Credit Card | CCARD |
| Credit (On Account) | INVOICE |

### 4.4 Test EFD Connection

1. Go to **EFD Settings** for your company
2. Click **Test Connection**
3. If successful, you'll see "Connection successful"

### 4.5 Submit Invoice to EFD

**Automatic Submission:**
- If "Auto Submit on Invoice" is enabled, invoices are submitted automatically when you submit a Sales Invoice

**Manual Submission:**
1. Open a submitted Sales Invoice
2. Click **Submit to EFD** button
3. Review the preview dialog
4. Click **Submit** to send to TRA

### 4.6 Check EFD Status

- **EFD Status** field on Sales Invoice shows: Not Sent, Pending, Success, Failed
- Click on **EFD Posting Log** link to see detailed submission history
- Use **EFD Verification URL** to verify receipt on TRA portal

---

## 5. Customer & Supplier Setup

### 5.1 Configure Customer Tax Information

1. Go to **Selling > Customer > [Customer Name]**
2. Scroll to **Tanzania Tax Information** section
3. Fill in:

```
TIN: Customer's Tax Identification Number
VRN: Customer's VAT Registration Number (if registered)
EFD ID Type: Select appropriate ID type
  - 1-TIN (for businesses)
  - 5-NID (for individuals with NIDA)
  - 6-Other (for foreign customers)
Tax Category: Link to appropriate tax category
```

### 5.2 Configure Supplier Tax Information

1. Go to **Buying > Supplier > [Supplier Name]**
2. Scroll to **Tanzania Tax Information** section
3. Fill in:

```
TIN: Supplier's Tax Identification Number
VRN: Supplier's VAT Registration Number
Tax Category: Link to appropriate tax category
```

### 5.3 Apply Tax Category at Group Level

To apply tax rules to all customers/suppliers in a group:

1. Go to **Selling > Customer Group** or **Buying > Supplier Group**
2. Create groups like "Export Customers", "Local Businesses"
3. In Tax Rules, filter by Customer Group or Supplier Group

---

## 6. Item Configuration

### 6.1 Assign Tax Template to Items

1. Go to **Stock > Item > [Item Name]**
2. In **Tax** section, add Item Tax:

```
Item Tax Template: Tanzania VAT 18%
Valid From: (leave empty for always)
```

### 6.2 Apply Tax at Item Group Level

For bulk assignment:

1. Go to **Stock > Item Group > [Group Name]**
2. Add Item Tax Template in the group
3. All items in this group will inherit the tax template

### 6.3 Tax Priority

Tax is determined in this order:
1. Item-level tax template (highest priority)
2. Item Group-level tax template
3. Tax Rule based on customer/supplier
4. Default tax template on transaction

---

## 7. Payroll Setup

### 7.1 Configure Employee Statutory Details

For each employee, configure their statutory information:

1. Go to **HR > Employee > [Employee Name]**
2. Scroll to **Statutory Details** section
3. Fill in:

```
Pension Fund: NSSF or PSSF
  - NSSF: National Social Security Fund (most common)
  - PSSF: Private Sector Pension Fund (some private companies)

TIN: Employee's Tax Identification Number
HESLB: HESLB Loan Number (if applicable, for loan repayment)
Pension Fund Number: NSSF/PSSF membership number
WCF Number: Workers Compensation Fund number
NIDA: National ID number

Employment Type: Primary or Secondary
  - Primary: Normal PAYE calculation
  - Secondary: 30% flat rate (for employees with multiple jobs)
```

### 7.2 Understanding Statutory Deductions

| Component | Employee | Employer | Condition |
|-----------|----------|----------|-----------|
| **NSSF** | 10% | 10% | Pension Fund = NSSF |
| **PSSF** | 5% | 15% | Pension Fund = PSSF |
| **SDL** | - | 3.5% | All employees |
| **WCF** | - | 0.5% | All employees |
| **HESLB** | 15% | - | HESLB field is filled |
| **PAYE** | Variable | - | Based on tax brackets |

### 7.3 PAYE Tax Brackets

PAYE is calculated based on monthly taxable income:

| Monthly Income (TZS) | Tax Rate | Cumulative Tax |
|---------------------|----------|----------------|
| 0 - 270,000 | 0% | 0 |
| 270,001 - 520,000 | 8% | Up to 20,000 |
| 520,001 - 760,000 | 20% | Up to 68,000 |
| 760,001 - 1,000,000 | 25% | Up to 128,000 |
| Above 1,000,000 | 30% | 128,000 + 30% of excess |

> **Note**: PAYE is calculated on gross income MINUS NSSF/PSSF employee contribution.

### 7.4 Create Salary Structure

1. Go to **Tanzania > Payroll Setup > Salary Structure**
2. Create new structure:

```
Name: Tanzania Standard Salary
Company: [Your Company]
Is Active: Yes
Payroll Frequency: Monthly

Earnings:
  - Basic (Amount Based)
  - Allowance (Amount Based)
  - Transport Allowance (Amount Based)

Deductions:
  - NSSF (Formula Based) - Auto-calculated
  - PSSF (Formula Based) - Auto-calculated
  - PAYE- (Tax) (Formula Based) - Auto-calculated
  - HESLB (Formula Based) - Auto-calculated
  - SDL (Formula Based) - Auto-calculated
  - WCF (Formula Based) - Auto-calculated
```

### 7.5 Assign Salary Structure to Employees

1. Go to **Tanzania > Payroll Setup > Salary Structure Assignment**
2. Click **+ Add Salary Structure Assignment**
3. Fill in:

```
Employee: [Select Employee]
Salary Structure: Tanzania Standard Salary
From Date: Start date
Company: [Your Company]

Base: Monthly basic salary amount
Variable: Any variable pay
```

### 7.6 Bulk Salary Structure Assignment

For multiple employees:

1. Go to **Tanzania > Payroll Setup > Bulk Salary Structure Assignment**
2. Select filters (Department, Branch, etc.)
3. Select employees
4. Assign structure to all at once

---

## 8. Running Payroll

### 8.1 Create Payroll Entry

1. Go to **Tanzania > Payroll Setup > Payroll Entry**
2. Click **+ Add Payroll Entry**
3. Fill in:

```
Company: [Your Company]
Posting Date: Pay date
Payroll Frequency: Monthly
Start Date: First day of pay period
End Date: Last day of pay period

Payroll Payable Account: Payroll Payable - [Company]
Cost Center: [If applicable]
```

4. Click **Get Employees** to fetch employees with salary structure
5. Review the list
6. Click **Create Salary Slips**

### 8.2 Review Salary Slips

1. Click **View Salary Slips** on Payroll Entry
2. Open each slip to verify:
   - Earnings are correct
   - NSSF/PSSF calculated correctly
   - PAYE calculated correctly
   - HESLB deducted (if applicable)

### 8.3 Submit Salary Slips

1. On Payroll Entry, click **Submit Salary Slips**
2. All salary slips will be submitted

### 8.4 Create Payment Entry (Bank Entry)

1. On Payroll Entry, click **Make Bank Entry**
2. This creates Journal Entry for:
   - Net salary payment to employees
   - Statutory liability accounts (PAYE, NSSF, SDL, WCF, HESLB)

---

## 9. Generating Reports

### 9.1 Tax Reports

| Report | Path | Purpose |
|--------|------|---------|
| **VAT eFiling Return** | Tanzania > Tax Report | Monthly VAT return for TRA |
| **Input VAT Return** | Tanzania > Tax Report | Input VAT claims |
| **VAT Output Reconciliation** | Tanzania > Tax Report | Match EFD with invoices |
| **Withholding Tax (ITX 219.03.E)** | Tanzania > Tax Report | WHT submission |

### 9.2 Payroll Reports

| Report | Path | Purpose |
|--------|------|---------|
| **PAYE and SDL Report** | Tanzania > Payroll Report | Monthly PAYE/SDL for TRA |
| **NSSF Contribution Report** | Tanzania > Payroll Report | NSSF submission |
| **WCF Contribution Report** | Tanzania > Payroll Report | WCF submission |
| **HESLB Return** | Tanzania > Payroll Report | HESLB submission |
| **Monthly Payroll Summary** | Tanzania > Payroll Report | Internal payroll summary |
| **Payroll Cost Analysis** | Tanzania > Payroll Report | Cost breakdown |

### 9.3 EFD Reports

| Report | Path | Purpose |
|--------|------|---------|
| **EFD Summary** | Tanzania > EFD Integration | EFD submission overview |
| **EFD Daily Sales** | Tanzania > EFD Integration | Daily sales by EFD |
| **EFD Z-Report** | Tanzania > EFD Integration | End of day fiscal report |

---

## 10. Troubleshooting

### 10.1 EFD Issues

**Issue: EFD submission fails**
- Check EFD Settings credentials
- Verify internet connection
- Check EFD Posting Log for error message
- Contact your EFD provider

**Issue: Receipt not appearing on TRA portal**
- Wait a few minutes for TRA sync
- Use the verification URL from the invoice
- Check if you're in Sandbox vs Production mode

**Issue: Wrong tax code on receipt**
- Check Item Tax Template has correct EFD Tax Code
- Verify Item has the correct tax template assigned

### 10.2 Payroll Issues

**Issue: NSSF not calculating**
- Verify employee has Pension Fund = "NSSF" in Statutory Details
- Check salary structure has NSSF component with condition

**Issue: PAYE calculating incorrectly**
- Verify Employment Type (Primary vs Secondary)
- Check NSSF is deducted before PAYE calculation
- Review PAYE formula in salary component

**Issue: HESLB not deducting**
- Employee must have HESLB number filled in Statutory Details
- Check salary structure has HESLB component

### 10.3 Tax Issues

**Issue: VAT not applying to invoice**
- Check Item has Item Tax Template assigned
- Verify Tax Rule is configured
- Check customer has correct Tax Category

**Issue: Wrong tax amount**
- Verify Item Tax Template has correct rate
- Check if there are conflicting tax rules

---

## Quick Reference Card

### Tax Rates
- **VAT**: 18%
- **Withholding Tax**: 2-15% (varies by type)

### Statutory Rates
- **NSSF**: 10% + 10% (employee + employer)
- **PSSF**: 5% + 15% (employee + employer)
- **SDL**: 3.5% (employer only)
- **WCF**: 0.5% (employer only)
- **HESLB**: 15% (employee only, if applicable)

### EFD Tax Codes
- **A**: Standard 18%
- **B**: Special Rate
- **C**: Zero Rated
- **D**: Special Relief
- **E**: Exempt

### EFD Payment Types
- **CASH**: Cash payment
- **CHEQUE**: Cheque payment
- **CCARD**: Credit/Debit card
- **EMONEY**: Mobile money, bank transfer
- **INVOICE**: Credit sale

---

## Need Help?

- **GitHub Issues**: [Report a bug](https://github.com/nelsonmpanju/tanzania/issues)
- **Email**: nelsonnorbert87@gmail.com

---

<div align="center">
	<p>Made with love for Tanzanian Businesses</p>
	<p>By <a href="https://github.com/nelsonmpanju">Nelson Mpanju</a></p>
</div>
