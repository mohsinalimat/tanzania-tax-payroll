# Tanzania Tax & Payroll Compliance

ERPNext app for Tanzania tax and payroll automation.

## Features

**Tax**: VAT 18%, Withholding Tax, PAYE brackets
**Payroll**: NSSF 20%, PSSF 20%, SDL 3.5%, WCF 0.5%, HESLB 15%
**Reports**: VAT Return, WHT (ITX.219.03.E), PAYE/SDL, NSSF/WCF, Payroll Cost Analysis

## Installation

```bash
bench get-app tanzania https://github.com/nelsonmpanju/tanzania.git
bench --site your-site install-app tanzania
bench --site your-site migrate
```

## Auto Setup

On install creates:
- Tax accounts (VAT, PAYE, WHT)
- Payroll accounts (NSSF, SDL, WCF, HESLB)
- Statutory suppliers (TRA, NSSF, WCF, HESLB, PSSF)
- Salary components & structure

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
