# Tanzania Tax & Payroll Compliance

ERPNext app for Tanzania tax, payroll, and EFD automation.

## Features

**Tax**: VAT 18%, Withholding Tax, PAYE brackets
**Payroll**: NSSF 20%, PSSF 20%, SDL 3.5%, WCF 0.5%, HESLB 15%
**EFD**: Multi-provider support (VFDPlus, TotalVFD, SimplifyVFD)
**Reports**: VAT Return, WHT, PAYE/SDL, NSSF/WCF, EFD Z-Report, Daily Sales

## Installation

```bash
bench get-app tanzania https://github.com/nelsonmpanju/tanzania.git
bench --site your-site install-app tanzania
bench migrate
```

## Auto Setup

On install creates:
- Tax accounts (VAT, PAYE, WHT)
- Payroll accounts (NSSF, SDL, WCF, HESLB)
- Statutory suppliers (TRA, NSSF, WCF, HESLB, PSSF)
- Salary components & structure

## EFD Integration (Optional)

EFD is **optional** - works without configuration. To enable:

1. Create **EFD Settings** for your company
2. Select provider (VFDPlus, TotalVFD, SimplifyVFD)
3. Enter API credentials
4. Enable auto-submit (optional)

**Features**:
- Auto/manual receipt submission
- Preview before sending
- Failed submission retry
- Receipt verification URL
- Posting audit log

**Tax Codes**: A=18%, B=Special, C=Zero, D=Relief, E=Exempt

## PAYE Brackets (Monthly)

| Income (TZS) | Rate |
|--------------|------|
| 0 - 270,000 | 0% |
| 270,001 - 520,000 | 8% |
| 520,001 - 760,000 | 20% |
| 760,001 - 1,000,000 | 25% |
| Above 1,000,000 | 30% |

## License

MIT
