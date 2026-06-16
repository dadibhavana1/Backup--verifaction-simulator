# Expected AI Dynamic Validation Output

## Input

SQLite backup database selected from the Streamlit dashboard.

Example:

```text
database/backup/backup_YYYYMMDD_HHMMSS.db
```

## Expected AI-Generated Checks

Gemini AI reads the database schema and may generate SQL checks like:

```sql
SELECT * FROM transactions WHERE amount < 0;
```

```sql
SELECT username, email, COUNT(*)
FROM users
GROUP BY username, email
HAVING COUNT(*) > 1;
```

```sql
SELECT *
FROM transactions
WHERE user_id NOT IN (SELECT id FROM users);
```

## Expected PASS Case

```text
Test: Check for negative transaction amounts
Status: PASS
Result: No anomalies found.
```

## Expected FAIL Case

```text
Test: Check for negative transaction amounts
Status: FAIL
Result: Found anomalous rows.
```

## Expected Generated Output

- Dashboard displays each AI-generated test.
- SQL query is shown for each test.
- Each test shows pass or fail status.
- AI narrative report explains the database health.
- PDF report can be downloaded.
- GitHub issue is created if anomalies are found and GitHub is configured.

