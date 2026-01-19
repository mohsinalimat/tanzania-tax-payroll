<p align="center">
  <img src="https://img.shields.io/badge/ERPNext-15.x-blue" alt="ERPNext Version">
  <img src="https://img.shields.io/badge/Frappe-15.x-blue" alt="Frappe Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Country-Tanzania-gold" alt="Country">
</p>

# 🇹🇿 Tanzania Tax & Payroll Compliance

A comprehensive ERPNext application for Tanzanian businesses to automate tax calculations, payroll processing, and statutory compliance with TRA (Tanzania Revenue Authority) and social security regulations.

---

## ✨ Key Features

### Tax Compliance
| Feature | Description |
|---------|-------------|
| **VAT Management** | 18% VAT calculations with Input/Output tracking |
| **Withholding Tax** | Automatic WHT deductions (2%, 5%, 10%, 15%) |
| **PAYE Calculation** | Progressive tax brackets as per Tanzania Income Tax Act |
| **Tax Templates** | Pre-configured templates for all transaction types |

### Payroll Compliance
| Contribution | Rate | Description |
|--------------|------|-------------|
| **NSSF** | 10% + 10% | Employee + Employer contributions |
| **PSSF** | 5% + 15% | Public sector pension scheme |
| **SDL** | 3.5% | Skills Development Levy (employer) |
| **WCF** | 0.5% | Workers Compensation Fund (employer) |
| **HESLB** | 15% | Student loan repayment (if applicable) |

### Reports
- **VAT Return Report** - Ready for TRA filing
- **Withholding Tax Report** (ITX.219.03.E format)
- **PAYE & SDL Report** - Monthly payroll taxes
- **NSSF/WCF Contribution Reports**
- **Payroll Cost Analysis** - Department-wise cost breakdown
- **Statutory Payment Tracking** - Due vs Paid monitoring
- **Executive Dashboards** - CEO/CFO summary views

---

## 🚀 Installation

### Prerequisites
- ERPNext 15.x
- Frappe HRMS 15.x

### Install via Bench
```bash
# Get the app
bench get-app tanzania https://github.com/your-org/tanzania.git

# Install on your site
bench --site your-site.local install-app tanzania

# Run migrations
bench --site your-site.local migrate

# Restart
bench restart
```

### Automatic Setup
Upon installation, the app automatically creates:
- ✅ Tax accounts (VAT, PAYE, WHT payables)
- ✅ Payroll accounts (NSSF, SDL, WCF, HESLB)
- ✅ Statutory suppliers (TRA, NSSF, WCF, HESLB)
- ✅ Salary components with correct formulas
- ✅ Default salary structure
- ✅ Tax templates for Sales/Purchase

---

## 📋 Quick Start Guide

### 1. Company Setup
After installation, verify your company has:
- **TIN** (Tax Identification Number)
- **VRN** (VAT Registration Number) - if VAT registered

### 2. Employee Configuration
For each employee, set:
- **NSSF/PSSF Registration** - Check the applicable fund
- **Employment Type** - Primary or Secondary employer
- **HESLB** - If employee has student loan

### 3. Run Payroll
1. Go to **HR > Payroll Entry**
2. Select period and employees
3. Create Salary Slips
4. Submit - Journal Entry auto-created with statutory parties

### 4. Generate Reports
Navigate to **Tanzania** module for all compliance reports.

---

## 📊 Compliance Deadlines

| Obligation | Due Date | Penalty |
|------------|----------|---------|
| PAYE & SDL | 7th of following month | 5% + 2% monthly |
| VAT Return | 20th of following month | TZS 100,000 min |
| NSSF/PSSF | 30th of following month | 5% penalty |
| WHT | 7th of following month | Varies |
| WCF | Quarterly | As per WCF Act |

---

## 🏗️ Technical Architecture

```
tanzania/
├── install.py              # Auto-setup on installation
├── payroll_setup.py        # Salary components & structures
├── payroll_hooks.py        # Journal Entry party assignment
├── custom_fields.py        # TIN, VRN, NSSF fields
└── tanzania/
    └── report/             # All compliance reports
        ├── vat_return_report/
        ├── paye_sdl_report/
        ├── nssf_contribution_report/
        ├── itx_219_03_e_withholding_tax/
        ├── payroll_cost_analysis/
        ├── statutory_payment_tracking/
        └── ceo_dashboard/
```

---

## 🔧 Configuration

### Salary Component Formulas
| Component | Formula | Type |
|-----------|---------|------|
| Basic | `base` | Earning |
| NSSF (Employee) | `(base+IA_1)*0.1` | Deduction |
| NSSF (Employer) | `(base+IA_1)*0.1` | Statistical |
| PAYE | Progressive brackets | Deduction |
| SDL | `(base+IA_1)*0.035` | Statistical |
| WCF | `(base+IA_1)*0.005` | Statistical |

### PAYE Tax Brackets (Monthly)
| Income Range (TZS) | Rate |
|-------------------|------|
| 0 - 270,000 | 0% |
| 270,001 - 520,000 | 8% |
| 520,001 - 760,000 | 20% |
| 760,001 - 1,000,000 | 25% |
| Above 1,000,000 | 30% |

---

## 📞 Support

For issues and feature requests, please contact:
- **Email**: support@your-company.com
- **Documentation**: [Link to docs]

---

## 📄 License

MIT License - See LICENSE file for details.

---

<p align="center">
  <strong>Built for Tanzanian Businesses 🇹🇿</strong><br>
  Simplifying Compliance, Empowering Growth
</p>
