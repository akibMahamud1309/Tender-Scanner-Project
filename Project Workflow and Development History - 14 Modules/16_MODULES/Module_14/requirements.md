# Requirements

## Functional requirements

-   Listen for events: new RELEVANT tender, approaching deadline (configurable lead time), and source/job failures surfaced by the Scheduler.
-   Deliver notifications via the configured local/notification channel(s).
-   Track which events have already triggered a notification to avoid repeat/duplicate alerts for the same event.
-   Record notification delivery status (sent, failed) for troubleshooting.

## Non-functional requirements

-   Notification delivery failures must not block or affect the rest of the pipeline.
-   Deduplication window/logic must be clearly defined so users can trust that 'no notification' means 'already notified', not 'lost'.

## Inputs

-   New RELEVANT tender events from Module 05/09.
-   Deadline data from Module 10.
-   Job/source failure events from Module 13.

## Outputs

-   Delivered notifications via configured channel(s).
-   Notification delivery status records.

## Acceptance criteria

-   A new relevant tender triggers exactly one notification, not one per pipeline stage it passes through.
-   A tender approaching its configured deadline lead time triggers a deadline notification.
-   A source failure important enough to configure triggers a failure notification.
-   Notification delivery status is recorded and inspectable.
