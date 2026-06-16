import glob
import os
import sqlite3

from app import mock_backup


def count_rows(db_path, table_name):
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]
    finally:
        conn.close()


def test_init_source_db_creates_expected_tables_and_rows(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    mock_backup.init_source_db()

    assert os.path.exists(mock_backup.SOURCE_DB)
    assert count_rows(mock_backup.SOURCE_DB, "users") == 100
    assert count_rows(mock_backup.SOURCE_DB, "transactions") == 500


def test_create_backup_without_corruption_copies_source_database(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(mock_backup.random, "random", lambda: 0.9)

    mock_backup.create_backup()

    backups = glob.glob(os.path.join(mock_backup.BACKUPS_DIR, "*.db"))
    assert len(backups) == 1
    assert count_rows(backups[0], "users") == 100
    assert count_rows(backups[0], "transactions") == 500


def test_corrupt_backup_can_create_negative_transaction_amounts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mock_backup.init_source_db()

    mock_backup.corrupt_backup(mock_backup.SOURCE_DB, rand_val=0.50)

    conn = sqlite3.connect(mock_backup.SOURCE_DB)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE amount < 0")
        negative_amounts = cursor.fetchone()[0]
    finally:
        conn.close()

    assert negative_amounts > 0


def test_cleanup_old_backups_keeps_latest_files_and_removes_sandbox(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs(mock_backup.BACKUPS_DIR, exist_ok=True)
    os.makedirs("database/sandbox", exist_ok=True)

    for index in range(5):
        path = os.path.join(mock_backup.BACKUPS_DIR, f"backup_{index}.db")
        with open(path, "w", encoding="utf-8") as file:
            file.write("backup")
        os.utime(path, (index, index))

    sandbox_path = "database/sandbox/sandbox_database.db"
    with open(sandbox_path, "w", encoding="utf-8") as file:
        file.write("sandbox")

    mock_backup.cleanup_old_backups(keep=2)

    remaining = sorted(os.path.basename(path) for path in glob.glob(os.path.join(mock_backup.BACKUPS_DIR, "*.db")))
    assert remaining == ["backup_3.db", "backup_4.db"]
    assert not os.path.exists(sandbox_path)
