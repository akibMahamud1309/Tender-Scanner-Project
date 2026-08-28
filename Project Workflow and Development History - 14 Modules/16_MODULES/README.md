# 16 --- MODULE INDEX

## Module 01 --- Source Registry

Owns the approved list of tender/notice sources and source-specific
configuration.

## Module 02 --- Source Scanner

Connects to configured sources and collects tender/notice listings and
metadata.

## Module 03 --- Database

Provides the PostgreSQL persistence layer and data-access model for the
application.

## Module 04 --- Deduplication & Change Detection

Determines whether a collected opportunity is new, duplicate, or
materially changed.

## Module 05 --- IT/Software Relevance Filter

Filters collected opportunities to identify software, IT, digital,
technology, and related tenders.

## Module 06 --- Document Collector

Finds, downloads, validates, and tracks tender documents associated with
relevant opportunities.

## Module 07 --- Document Processor

Extracts text and metadata from machine-readable tender documents and
prepares content for analysis.

## Module 08 --- OCR

Processes scanned/image-only document pages when normal text extraction
is insufficient.

## Module 09 --- AI Classification

Uses AI to classify relevance and produce structured classification
results with traceability.

## Module 10 --- AI Tender Analysis

Extracts detailed tender requirements, eligibility, deadlines,
experience, documents, restrictions, and other structured intelligence.

## Module 11 --- Dashboard

Provides the local user interface for reviewing tenders, documents,
analysis, source health, and decisions.

## Module 12 --- Decision History

Stores bid/no-bid decisions, decline reasons, categories, comments, and
decision history.

## Module 13 --- Scheduler

Controls automated scan jobs, processing jobs, retry timing, and
scheduled maintenance.

## Module 14 --- Notifications

Delivers local/configured notifications about new relevant tenders,
deadlines, failures, and other events.
