"""Create all configured Tender Scanner database tables."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.database import Base, engine
from app import models  # noqa: F401 - importing registers models with Base.metadata


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database tables created or already present.")


if __name__ == "__main__":
    main()
