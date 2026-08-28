# Workflow

## Normal workflow

1.  Load a RELEVANT tender's document text.
2.  Run structured field extraction.
3.  Consolidate fields across multiple documents.
4.  Persist with evidence references.

## Failure/retry workflow

-   A tender with no extractable documents is flagged for manual review rather than producing an empty analysis silently.
-   Conflicting values for the same field across documents are flagged rather than one silently overwriting the other.

## Manual-review workflow

Tenders with conflicting or low-confidence extracted fields are surfaced for manual review before a bid/no-bid decision.
