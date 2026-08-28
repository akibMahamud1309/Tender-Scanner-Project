# 03 --- SYSTEM ARCHITECTURE

Approved Sources → Source Registry → Source Scanner → Normalization →
Deduplication/Change Detection → PostgreSQL → IT/Software Filter →
Document Collector → Document Processor → OCR when needed → AI
Classification → AI Tender Analysis → Dashboard → Decision History.
Scheduler and Notifications operate across the pipeline.

Technology direction: local Windows PC, Python/FastAPI, PostgreSQL,
JSONB, optional pgvector, Playwright where needed, local OCR, local
document storage.
