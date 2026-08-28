# Functions

  Function   Purpose   Status    File   Tests
  ---------- --------- --------- ------ -------
  build_classification_prompt   Assemble versioned prompt and evidence   Done    app/ai_classification.py    test_ai_classification.py
  call_ai_classifier   Invoke GPT-5.6 Terra classifier   Done    app/ai_classification.py    test_ai_classification.py
  parse_classification_result   Validate structured output and citations   Done    app/ai_classification.py    test_ai_classification.py
  record_classification   Persist model/prompt/evidence metadata   Done    app/ai_classification.py    test_ai_classification.py
