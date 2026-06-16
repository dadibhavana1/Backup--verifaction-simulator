from app.github_integration import file_github_issue


def test_file_github_issue_returns_none_when_credentials_are_missing(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_REPO", raising=False)

    issue_url = file_github_issue("Backup failed", "Validation failed.")

    assert issue_url is None
