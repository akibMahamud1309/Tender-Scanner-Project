# Architecture

## Components

-   Event listener
-   Deduplication tracker
-   Delivery channel adapter
-   Status recorder

## Data flow

``` text
Pipeline event (new relevant tender / deadline / failure) -> Dedup check -> Deliver via channel -> Record delivery status
```

## Interfaces

-   Reads: events from Modules 05/09/10/13.
-   Writes: notification status to Module 03.
-   Delivers: to configured local notification channel.

## Security considerations

-   Notification content is derived from already-validated internal data, not raw untrusted source text, to avoid delivering unsanitized content.

## Dependencies

-   Modules 05/09/10 for tender/deadline events.
-   Module 13 for failure events.
-   Module 03 for status persistence.
