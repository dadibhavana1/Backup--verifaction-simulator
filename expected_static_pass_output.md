# Expected Static Validation Output - PASS

## Input

Healthy SQLite backup database.

Example:

```text
database/backup/backup_YYYYMMDD_HHMMSS.db
```

## Expected Dashboard Status

```text
STATUS: PASS
```

## Expected Validation Details

```text
Users table count: 100
Transactions table count: 500
Total transactions sum: positive numeric value
```

## Expected AI Narrative Report

```text
The restored backup appears healthy. The users and transactions tables contain data, and the transaction amount total is valid. The backup can be considered restorable based on the checks performed.
```

## Expected Generated Output

- Dashboard shows `PASS`.
- No error messages are shown.
- PDF report can be downloaded.
- No GitHub issue is created.

