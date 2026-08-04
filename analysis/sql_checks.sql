-- Reproducible SQLite data-quality checks for the source-style AI portfolio tables.
-- Run with scripts/run_sql_checks.py, which loads CSV files into an in-memory SQLite database.

-- 1. Every control assessment must resolve to a registered initiative.
SELECT COUNT(*) AS orphan_control_assessments
FROM control_assessments c
LEFT JOIN ai_initiative_registry i ON c.initiative_id = i.initiative_id
WHERE i.initiative_id IS NULL;

-- 2. Each registered initiative must have all six required control records.
SELECT initiative_id, COUNT(*) AS control_records
FROM control_assessments
GROUP BY initiative_id
HAVING COUNT(*) <> 6;

-- 3. Open exceptions require a positive age; resolved exceptions must be zero-aged.
SELECT COUNT(*) AS invalid_exception_age_rows
FROM governance_exceptions
WHERE (status = 'Open' AND CAST(age_days AS INTEGER) <= 0)
   OR (status = 'Resolved' AND CAST(age_days AS INTEGER) <> 0);

-- 4. Value records must retain nonnegative planned and realized evidence.
SELECT COUNT(*) AS invalid_value_rows
FROM value_realization
WHERE CAST(planned_value AS REAL) < 0 OR CAST(realized_value AS REAL) < 0;

-- 5. Adoption telemetry must not exceed eligible population or be negative.
SELECT COUNT(*) AS invalid_adoption_rows
FROM adoption_telemetry
WHERE CAST(active_users AS INTEGER) < 0
   OR CAST(eligible_users AS INTEGER) < 0
   OR CAST(active_users AS INTEGER) > CAST(eligible_users AS INTEGER);
