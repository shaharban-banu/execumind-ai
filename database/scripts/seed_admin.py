import os
from dotenv import load_dotenv
from database.database import SessionLocal
from database.models import User

load_dotenv()

ADMIN_USERNAME=os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH=os.getenv("ADMIN_PASSWORD")

def seed_admin():
    if not ADMIN_USERNAME or not ADMIN_PASSWORD_HASH:
        raise RuntimeError(
            "ADMIN_USERNAME or ADMIN_PASSWORD is missing from environment."
        )
    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.username == ADMIN_USERNAME)
            .first()
        )

        if existing_user:
            if existing_user.role != "admin":
                existing_user.role = "admin"
                db.commit()
            print(f"Admin '{ADMIN_USERNAME}' already exists.")
            return

        admin = User(
            username=ADMIN_USERNAME,
            password_hash=ADMIN_PASSWORD_HASH,
            role="admin",
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print(
            f"Admin created successfully: "
            f"{admin.username} (id={admin.id})"
        )
    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()