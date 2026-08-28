# Requirements

## Functional requirements

-   Accept UNCERTAIN records from Module 05 and normalized document text from Module 07/08.
-   Send tender text/evidence to the configured AI model with a versioned prompt/configuration.
-   Return a structured classification: RELEVANT / NOT_RELEVANT with a confidence score.
-   Record the model name/version and prompt/configuration version used for each classification.
-   Retain references to the specific evidence (document, page, extracted snippet) that supported the classification.

## Non-functional requirements

-   Classifications must be reproducible given the same model/prompt version and input.
-   Must not fabricate evidence references; every classification cites real, retrievable source text.
-   Should degrade gracefully (flag for manual review) if the AI provider is unavailable, rather than blocking the whole pipeline.

## Inputs

-   UNCERTAIN records from Module 05.
-   Extracted/normalized document text from Module 07/08.

## Outputs

-   Structured relevance classification with confidence score.
-   Model/prompt version metadata per classification.
-   Evidence references supporting each classification.

## Acceptance criteria

-   An UNCERTAIN record receives a final RELEVANT/NOT_RELEVANT classification with a confidence score.
-   Every classification records which model/prompt version produced it.
-   Low-confidence classifications are flagged for manual review rather than accepted silently.
