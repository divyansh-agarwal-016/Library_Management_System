from pathlib import Path

from app.config import DEFAULT_DB_PATH
from seed import seed


def reset_database():
    db_file = Path(DEFAULT_DB_PATH)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    if db_file.exists():
        db_file.unlink()
        print(f"Removed existing database: {db_file}")
    else:
        print(f"No existing database found at: {db_file}")

    seed()
    print("Database reset complete.")


if __name__ == "__main__":
    reset_database()
