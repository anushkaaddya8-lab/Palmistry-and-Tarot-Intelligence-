from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from io import BytesIO

from app.database import get_db
from app.auth.dependencies import get_current_user

from app.model.tarot_reading import TarotReading
from app.model.tarot_card import TarotCard


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/tarot/{reading_id}")
def generate_tarot_report(

    reading_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    result = (

        db.query(TarotReading, TarotCard)

        .join(

            TarotCard,

            TarotReading.card_id == TarotCard.id

        )

        .filter(

            TarotReading.id == reading_id,

            TarotReading.user_id == current_user.id

        )

        .first()

    )


    if not result:

        raise HTTPException(

            status_code=404,

            detail="Reading not found"

        )


    reading, card = result


    # Select correct meaning
    if reading.orientation == "Reversed":

        meaning = card.reversed_meaning

    else:

        meaning = card.upright_meaning


    pdf_buffer = BytesIO()


    document = SimpleDocTemplate(

        pdf_buffer,

        pagesize=A4,

        rightMargin=50,

        leftMargin=50,

        topMargin=50,

        bottomMargin=50

    )


    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(

        "TitleStyle",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontSize=24,

        spaceAfter=20

    )


    heading_style = ParagraphStyle(

        "HeadingStyle",

        parent=styles["Heading2"],

        alignment=TA_CENTER,

        fontSize=16,

        spaceAfter=15

    )


    normal_style = ParagraphStyle(

        "NormalStyle",

        parent=styles["BodyText"],

        fontSize=12,

        leading=18,

        spaceAfter=12

    )


    content = []


    content.append(

        Paragraph(

            "🎴 Tarot Card Reading",

            title_style

        )

    )


    content.append(

        Paragraph(

            "Your personal Tarot interpretation",

            heading_style

        )

    )


    content.append(

        Spacer(1, 20)

    )


    content.append(

        Paragraph(

            f"<b>Card:</b> {card.name}",

            normal_style

        )

    )


    content.append(

        Paragraph(

            f"<b>Arcana:</b> {card.arcana}",

            normal_style

        )

    )


    content.append(

        Paragraph(

            f"<b>Suit:</b> {card.suit}",

            normal_style

        )

    )


    content.append(

        Paragraph(

            f"<b>Orientation:</b> {reading.orientation}",

            normal_style

        )

    )


    content.append(

        Spacer(1, 20)

    )


    content.append(

        Paragraph(

            "<b>Interpretation & Meaning</b>",

            heading_style

        )

    )


    content.append(

        Paragraph(

            meaning,

            normal_style

        )

    )


    content.append(

        Spacer(1, 20)

    )


    content.append(

        Paragraph(

            f"<b>Reading ID:</b> {reading.id}",

            normal_style

        )

    )


    content.append(

        Paragraph(

            f"<b>Created At:</b> {reading.created_at}",

            normal_style

        )

    )


    document.build(content)


    pdf_buffer.seek(0)


    return StreamingResponse(

        pdf_buffer,

        media_type="application/pdf",

        headers={

            "Content-Disposition":

            f"attachment; filename=tarot_reading_{reading.id}.pdf"

        }

    )