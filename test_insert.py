from app.database import SessionLocal
from app.models import URL

db = SessionLocal()

try:
    new_url = URL(
        short_code="test123",
        original_url="https://google.com"
    )

    db.add(new_url)

    db.commit()

    print("URL inserted successfully!")

except Exception as e:
    print("Error:")
    print(e)

finally:
    db.close()