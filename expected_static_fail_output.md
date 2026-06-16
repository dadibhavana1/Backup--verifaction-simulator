# Expected Static Validation Output - FAIL

## Input

Corrupted SQLite backup database.

Example corruption:

```sql
DELETE FROM transactions;
```

## Expected Dashboard Status

```text
STATUS: FAIL
```

## Expected Validation Details

```text
Users table count: 100
Transactions table count: 0
Total transactions sum: None
```

## Expected Errors

```text
Transactions table is empty.
Total transactions sum is NULL.
```

## Expected AI Narrative Report

```text
The restored backup is not healthy. The transactions table is empty and the transaction amount total is NULL. This backup should not be used for recovery until the issue is investigated.
```

## Expected Generated Output

- Dashboard shows `FAIL`.
- Error details are displayed.
- PDF report can be downloaded.
- GitHub issue is created if `GITHUB_TOKEN` and `GITHUB_REPO` are configured.

