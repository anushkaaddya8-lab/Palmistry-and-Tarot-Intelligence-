from app.database import SessionLocal
from app.model.tarot_card import TarotCard


db = SessionLocal()

try:
    card = TarotCard(
        name="The Fool",
        arcana="Major Arcana",
        suit=None,
        upright_meaning="New beginnings, adventure, freedom, and unlimited potential.",
        reversed_meaning="Recklessness, poor decisions, naivety, and lack of direction.",
        keywords="Beginnings, adventure, freedom, innocence",
        image_url=None
    )

    db.add(card)
    db.commit()

    print("The Fool card inserted successfully!")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()