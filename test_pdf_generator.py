from app.pdf_generator import generate_pdf


def test_generate_pdf_returns_pdf_bytes():
    pdf_bytes = generate_pdf(
        "Verification Report: backup.db",
        "Status: PASS\n\nDetails:\n[+] Users table count: 100\n\nAI Narrative Report:\nBackup is healthy.",
    )

    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 1000
