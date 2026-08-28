# Requirements

## Functional requirements

-   Accept normalized listing records from Module 02 (Source Scanner) as input.
-   Compute a stable match key per record (source ID + reference number, falling back to normalized URL + title hash when no reference number exists).
-   Look up existing records by match key against the Database (Module 03).
-   Classify each incoming record as NEW, UNCHANGED, or CHANGED.
-   For CHANGED records, produce a field-level diff (deadline, scope, documents, status) rather than overwriting silently.
-   Write a change event/history row for every CHANGED record instead of destroying the prior version.

## Non-functional requirements

-   Matching must be deterministic and reproducible for the same input.
-   Must not silently drop a record it cannot confidently match; ambiguous cases go to manual review rather than being auto-merged.
-   Should scale to the volume produced by a full scan cycle across all approved sources without becoming the pipeline bottleneck.

## Inputs

-   Normalized listing records from Module 02 (Source Scanner).
-   Existing records/history from Module 03 (Database).

## Outputs

-   Classification result per record: NEW / UNCHANGED / CHANGED.
-   Field-level change diff for CHANGED records.
-   History-preserving change events persisted via Module 03.

## Acceptance criteria

-   A record seen for the first time is classified NEW.
-   An identical record on a repeat scan is classified UNCHANGED and does not create a duplicate row.
-   A record with an altered deadline or scope is classified CHANGED, with the old value retained in history and the new value current.
-   No two records that share a stable match key ever exist as separate rows.
