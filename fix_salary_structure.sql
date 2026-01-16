-- Tanzania Payroll Fix Script (Without custom_ prefix)
-- This script fixes the salary structure conditions and custom fields
-- Run with: mysql -u _def09664c0663ab2 -pSTk5K0yrpPfW7Lxu _def09664c0663ab2 < apps/tanzania/fix_salary_structure.sql

-- Step 1: Delete old custom fields (with custom_ prefix)
DELETE FROM `tabCustom Field` WHERE dt = 'Employee' AND fieldname IN ('custom_nssf', 'custom_pssf', 'custom_heslb', 'custom_employment_type', 'employment_type');

-- Step 2: Create new fields without custom_ prefix
INSERT IGNORE INTO `tabCustom Field`
(name, dt, fieldname, fieldtype, label, options, description, insert_after, `default`, creation, modified, owner, modified_by)
VALUES
('Employee-tanzania_payroll_section', 'Employee', 'tanzania_payroll_section', 'Section Break', 'Tanzania Payroll Information', NULL, NULL, 'salary_mode', NULL, NOW(), NOW(), 'Administrator', 'Administrator'),
('Employee-nssf', 'Employee', 'nssf', 'Check', 'NSSF Registered', NULL, 'Employee is registered with NSSF (National Social Security Fund)', 'tanzania_payroll_section', '0', NOW(), NOW(), 'Administrator', 'Administrator'),
('Employee-pssf', 'Employee', 'pssf', 'Check', 'PSSF Registered', NULL, 'Employee is registered with PSSF (Public Service Social Security Fund)', 'nssf', '0', NOW(), NOW(), 'Administrator', 'Administrator'),
('Employee-column_break_payroll', 'Employee', 'column_break_payroll', 'Column Break', NULL, NULL, NULL, 'pssf', NULL, NOW(), NOW(), 'Administrator', 'Administrator'),
('Employee-heslb', 'Employee', 'heslb', 'Check', 'HESLB Loan', NULL, 'Employee has HESLB (Higher Education Students Loans Board) loan - 15% deduction', 'column_break_payroll', '0', NOW(), NOW(), 'Administrator', 'Administrator'),
('Employee-employment_type', 'Employee', 'employment_type', 'Select', 'Employment Type', 'Primary\nSecondary', 'Primary or Secondary employment (affects PAYE calculation)', 'heslb', 'Primary', NOW(), NOW(), 'Administrator', 'Administrator');

-- Step 3: Rename columns in Employee table (if old ones exist)
-- Check if custom_nssf column exists and rename data
SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
                   WHERE TABLE_NAME = 'tabEmployee' AND COLUMN_NAME = 'custom_nssf'
                   AND TABLE_SCHEMA = DATABASE());

-- Add new columns if they don't exist
SET @add_nssf = (SELECT IF(COUNT(*) = 0, 'ALTER TABLE `tabEmployee` ADD COLUMN `nssf` INT(1) DEFAULT 0', 'SELECT 1')
                 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'tabEmployee' AND COLUMN_NAME = 'nssf' AND TABLE_SCHEMA = DATABASE());
PREPARE stmt FROM @add_nssf;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @add_pssf = (SELECT IF(COUNT(*) = 0, 'ALTER TABLE `tabEmployee` ADD COLUMN `pssf` INT(1) DEFAULT 0', 'SELECT 1')
                 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'tabEmployee' AND COLUMN_NAME = 'pssf' AND TABLE_SCHEMA = DATABASE());
PREPARE stmt FROM @add_pssf;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @add_heslb = (SELECT IF(COUNT(*) = 0, 'ALTER TABLE `tabEmployee` ADD COLUMN `heslb` INT(1) DEFAULT 0', 'SELECT 1')
                  FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'tabEmployee' AND COLUMN_NAME = 'heslb' AND TABLE_SCHEMA = DATABASE());
PREPARE stmt FROM @add_heslb;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @add_emp_type = (SELECT IF(COUNT(*) = 0, 'ALTER TABLE `tabEmployee` ADD COLUMN `employment_type` VARCHAR(140) DEFAULT "Primary"', 'SELECT 1')
                     FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'tabEmployee' AND COLUMN_NAME = 'employment_type' AND TABLE_SCHEMA = DATABASE());
PREPARE stmt FROM @add_emp_type;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Copy data from old columns to new columns (if old columns exist)
UPDATE `tabEmployee` SET nssf = COALESCE(custom_nssf, 0) WHERE custom_nssf IS NOT NULL;
UPDATE `tabEmployee` SET pssf = COALESCE(custom_pssf, 0) WHERE custom_pssf IS NOT NULL;
UPDATE `tabEmployee` SET heslb = COALESCE(custom_heslb, 0) WHERE custom_heslb IS NOT NULL;
UPDATE `tabEmployee` SET employment_type = COALESCE(custom_employment_type, 'Primary') WHERE custom_employment_type IS NOT NULL AND custom_employment_type != '';

-- Set defaults for new fields
UPDATE `tabEmployee` SET nssf = 0 WHERE nssf IS NULL;
UPDATE `tabEmployee` SET pssf = 0 WHERE pssf IS NULL;
UPDATE `tabEmployee` SET heslb = 0 WHERE heslb IS NULL;
UPDATE `tabEmployee` SET employment_type = 'Primary' WHERE employment_type IS NULL OR employment_type = '';

-- Step 4: Delete ALL existing rows from Tanzania Default Salary Structure
DELETE FROM `tabSalary Detail` WHERE parent = 'Tanzania Default Salary Structure';

-- Step 5: Insert correct earnings with proper conditions (without custom_ prefix)
INSERT INTO `tabSalary Detail` (name, owner, creation, modified, modified_by, docstatus, idx, parent, parenttype, parentfield, salary_component, abbr, formula, amount_based_on_formula, depends_on_payment_days, do_not_include_in_total, `condition`)
VALUES
-- Earnings
(CONCAT('SSDE-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 1, 'Tanzania Default Salary Structure', 'Salary Structure', 'earnings', 'Basic', 'B', 'base', 1, 1, 0, ''),
(CONCAT('SSDE-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 2, 'Tanzania Default Salary Structure', 'Salary Structure', 'earnings', 'Allowance', 'IA_1', '', 0, 0, 0, ''),
(CONCAT('SSDE-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 3, 'Tanzania Default Salary Structure', 'Salary Structure', 'earnings', 'Transport Allowance', 'TrAll', '', 0, 1, 0, ''),
(CONCAT('SSDE-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 4, 'Tanzania Default Salary Structure', 'Salary Structure', 'earnings', 'NSSF Expense', 'NSSFe', '(base+IA_1)*0.1', 1, 0, 1, 'nssf == 1'),
(CONCAT('SSDE-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 5, 'Tanzania Default Salary Structure', 'Salary Structure', 'earnings', 'PSSF Expense', 'PSSFe', '(base+IA_1)*0.15', 1, 0, 1, 'pssf == 1'),
(CONCAT('SSDE-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 6, 'Tanzania Default Salary Structure', 'Salary Structure', 'earnings', 'SDL Expense', 'SDLe', '(base+IA_1)*0.035', 1, 0, 1, ''),
(CONCAT('SSDE-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 7, 'Tanzania Default Salary Structure', 'Salary Structure', 'earnings', 'WCF Expense', 'WCFe', '(base+IA_1)*0.005', 1, 0, 1, '');

-- Step 6: Insert correct deductions with proper conditions (without custom_ prefix)
INSERT INTO `tabSalary Detail` (name, owner, creation, modified, modified_by, docstatus, idx, parent, parenttype, parentfield, salary_component, abbr, formula, amount_based_on_formula, depends_on_payment_days, do_not_include_in_total, `condition`)
VALUES
-- NSSF Employee and Employer
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 1, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'NSSF', 'NSSFemp', '(base+IA_1)*0.1', 1, 0, 0, 'nssf == 1'),
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 2, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'NSSF Employer', 'NSSFempl', '(base+IA_1)*0.1', 1, 0, 1, 'nssf == 1'),
-- PSSF Employee and Employer
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 3, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'PSSF', 'PSSFemp', '(base+IA_1)*0.05', 1, 0, 0, 'pssf == 1'),
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 4, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'PSSF Employer', 'PSSFempl', '(base+IA_1)*0.15', 1, 0, 1, 'pssf == 1'),
-- WCF and SDL
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 5, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'WCF', 'WCF', '(base+IA_1)*0.005', 1, 0, 1, ''),
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 6, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'SDL', 'SDL', '(base+IA_1)*0.035', 1, 0, 1, ''),
-- PAYE Tiers (Primary Employment)
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 7, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'PAYE- (Tax)', 'PAYE', '(((base+IA_1) - NSSFemp) - 270000) * 0.08', 1, 1, 0, '(((base+IA_1) - NSSFemp) >= 270000) and (((base+IA_1) - NSSFemp) < 520000) and (employment_type == "Primary" or employment_type == "")'),
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 8, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'PAYE- (Tax)', 'PAYE', '((((base+IA_1) - NSSFemp) - 520000) * 0.2) + 20000', 1, 1, 0, '(((base+IA_1) - NSSFemp) >= 520000) and (((base+IA_1) - NSSFemp) < 760000) and (employment_type == "Primary" or employment_type == "")'),
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 9, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'PAYE- (Tax)', 'PAYE', '((((base+IA_1) - NSSFemp) - 760000) * 0.25) + 68000', 1, 1, 0, '(((base+IA_1) - NSSFemp) >= 760000) and (((base+IA_1) - NSSFemp) < 1000000) and (employment_type == "Primary" or employment_type == "")'),
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 10, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'PAYE- (Tax)', 'PAYE', '((((base+IA_1) - NSSFemp) - 1000000) * 0.3) + 128000', 1, 1, 0, '(((base+IA_1) - NSSFemp) >= 1000000) and (employment_type == "Primary" or employment_type == "")'),
-- PAYE Secondary Employment (30% flat)
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 11, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'PAYE- (Tax)', 'PAYE', '((base+IA_1) - NSSFemp) * 0.3', 1, 1, 0, 'employment_type == "Secondary"'),
-- HESLB
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 12, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'HESLB', 'HESLB', '(base+IA_1) * 0.15', 1, 0, 0, 'heslb == 1'),
-- Other Deductions
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 13, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'Salary Advance', 'SLADV', '', 0, 1, 1, ''),
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 14, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'Loan', 'Ln', '', 0, 1, 0, ''),
(CONCAT('SSDD-', UUID_SHORT()), 'Administrator', NOW(), NOW(), 'Administrator', 0, 15, 'Tanzania Default Salary Structure', 'Salary Structure', 'deductions', 'Employee Deduction', 'ED', '', 0, 1, 0, '');

-- Step 7: Verify the fix
SELECT 'Verification Results:' as '';
SELECT '----------------------' as '';
SELECT CONCAT('Custom Fields on Employee: ', COUNT(*)) as result FROM `tabCustom Field` WHERE dt = 'Employee' AND fieldname IN ('nssf', 'pssf', 'heslb', 'employment_type', 'tanzania_payroll_section', 'column_break_payroll');
SELECT CONCAT('Earnings in Salary Structure: ', COUNT(*)) as result FROM `tabSalary Detail` WHERE parent = 'Tanzania Default Salary Structure' AND parentfield = 'earnings';
SELECT CONCAT('Deductions in Salary Structure: ', COUNT(*)) as result FROM `tabSalary Detail` WHERE parent = 'Tanzania Default Salary Structure' AND parentfield = 'deductions';

SELECT 'Done! Field names are now: nssf, pssf, heslb, employment_type (without custom_ prefix)' as '';
