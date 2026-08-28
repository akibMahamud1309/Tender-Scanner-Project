# Requirements

## Functional requirements

-   Accept decision actions (bid / no-bid) from Module 11 (Dashboard).
-   Require a decline reason and category when a decision is no-bid.
-   Store free-text user comments alongside each decision.
-   Timestamp every decision and preserve the full history if a decision is later revisited.
-   Expose decision history for future reporting or pattern analysis (e.g., common decline reasons).

## Non-functional requirements

-   Decisions are never overwritten; a changed decision creates a new history entry rather than replacing the old one.
-   Decline reason/category values should come from a maintained, consistent list to keep reporting meaningful.

## Inputs

-   Decision actions (bid/no-bid, reason, category, comments) from Module 11.

## Outputs

-   Persisted, timestamped decision history per tender.
-   Decision data available for future reporting.

## Acceptance criteria

-   A no-bid decision without a reason/category is rejected and requires that data.
-   Revisiting a decision preserves the original entry rather than deleting it.
-   All decisions for a tender are retrievable in chronological order.
