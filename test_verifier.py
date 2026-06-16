import os
import sqlite3

from app import mock_backup, verifier


def create_empty_transactions_backup(tmp_path):
    mock_backup.init_source_db()
    backup_path = tmp_path / "broken_backup.db"
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    mock_backup.corrupt_backup(mock_backup.SOURCE_DB, rand_val=0.20)
    os.replace(mock_backup.SOURCE_DB, backup_path)
    return backup_path


def test_restore_backup_copies_selected_backup_to_sandbox(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mock_backup.init_source_db()

    verifier.restore_backup(mock_backup.SOURCE_DB)

    assert os.path.exists(verifier.SANDBOX_DB)


def test_run_validation_queries_passes_for_healthy_database(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mock_backup.init_source_db()
    verifier.restore_backup(mock_backup.SOURCE_DB)

    results = verifier.run_validation_queries()

    assert results["status"] == "PASS"
    assert results["errors"] == []
    assert "Users table count: 100" in results["details"]
    assert "Transactions table count: 500" in results["details"]


def test_run_validation_queries_fails_when_transactions_are_empty(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    backup_path = create_empty_transactions_backup(tmp_path)
    verifier.restore_backup(backup_path)

    results = verifier.run_validation_queries()

    assert results["status"] == "FAIL"
    assert "Transactions table is empty." in results["errors"]
    assert "Total transactions sum is NULL." in results["errors"]


def test_run_validation_queries_fails_when_sandbox_database_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    results = verifier.run_validation_queries()

    assert results["status"] == "FAIL"
    assert results["errors"] == ["Sandbox database file is missing after restoration."]


def test_generate_report_returns_mock_text_when_gemini_key_is_missing(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    report = verifier.generate_report(
        "backup.db",
        {"status": "PASS", "details": ["Users table count: 100"], "errors": []},
    )

    assert report == "Gemini API key not configured. Mock report: Validation completed."


def test_verify_backup_files_issue_when_static_validation_fails(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    backup_path = create_empty_transactions_backup(tmp_path)

    monkeypatch.setattr(verifier, "generate_report", lambda backup_filename, results: "Backup failed.")
    monkeypatch.setattr(verifier, "file_github_issue", lambda title, body: "https://github.com/example/repo/issues/1")

    results = verifier.verify_backup(backup_path)

    assert results["status"] == "FAIL"
    assert results["report"] == "Backup failed."
    assert results["issue_url"] == "https://github.com/example/repo/issues/1"


def test_run_ai_dynamic_validation_returns_error_when_api_key_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    mock_backup.init_source_db()

    conn = sqlite3.connect(mock_backup.SOURCE_DB)
    conn.close()

    result = verifier.run_ai_dynamic_validation(mock_backup.SOURCE_DB)

    assert result == {"error": "API Key missing or invalid"}
