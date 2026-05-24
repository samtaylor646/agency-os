import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from server import database, models, auth
from sqlalchemy.orm import Session

db = database.SessionLocal()
models.Base.metadata.create_all(bind=database.engine)

user = db.query(models.User).filter(models.User.email == "admin@agencyos.com").first()
if not user:
    hashed_password = auth.get_password_hash("password123")
    user = models.User(email="admin@agencyos.com", hashed_password=hashed_password)
    db.add(user)
    db.commit()
    print("User seeded")
else:
    print("User already exists")
db.close()
