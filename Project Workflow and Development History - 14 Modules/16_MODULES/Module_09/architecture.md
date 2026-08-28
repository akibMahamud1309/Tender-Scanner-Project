# Architecture

## Components

-   Prompt/version manager
-   AI classification client
-   Evidence linker
-   Confidence thresholding

## Data flow

``` text
Uncertain record + extracted text -> AI classification call -> Structured result (label, confidence, evidence) -> Persist -> Forward RELEVANT records to AI Tender Analysis
```

## Interfaces

-   Reads: uncertain records and extracted text from Modules 05/07/08.
-   Writes: classification results to Module 03.
-   Forwards: RELEVANT results to Module 10 (AI Tender Analysis).

## Security considerations

-   Tender/document text sent to the AI model is treated as untrusted; classification results are structured data, not executable instructions.
-   Prompt injection attempts embedded in source documents must not be able to alter system behavior beyond the classification task itself.

## Dependencies

-   Module 05 for uncertain records.
-   Module 07/08 for document text.
-   Configured AI provider.
-   Module 03 for persistence.
