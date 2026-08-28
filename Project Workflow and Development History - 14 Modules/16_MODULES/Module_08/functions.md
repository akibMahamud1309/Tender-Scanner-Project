# Functions

  Function   Purpose   Status    File   Tests
  ---------- --------- --------- ------ -------
  detect_scanned_pages   Identify pages needing OCR   Done    app/ocr.py    test_ocr.py
  run_ocr   Send a document to GPT-5.6 Terra   Done    app/ocr.py    test_ocr.py
  normalize_ocr_output   Convert OCR output to standard text format   Done    app/ocr.py    test_ocr.py
  record_ocr_result   Persist OCR text with engine/version metadata   Done    app/ocr.py    test_ocr.py
