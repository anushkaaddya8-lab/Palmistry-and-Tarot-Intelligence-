from app.database import SessionLocal
from app.model.tarot_card import TarotCard


major_arcana = [
    {
        "name": "The Fool",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "New beginnings, adventure, freedom, and unlimited potential.",
        "reversed_meaning": "Recklessness, poor decisions, naivety, and lack of direction.",
        "keywords": "Beginnings, adventure, freedom, innocence",
        "image_url": None
    },
    {
        "name": "The Magician",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Manifestation, skill, power, and confidence.",
        "reversed_meaning": "Manipulation, deception, and unused potential.",
        "keywords": "Manifestation, power, skill, action",
        "image_url": None
    },
    {
        "name": "The High Priestess",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Intuition, mystery, inner wisdom, and hidden knowledge.",
        "reversed_meaning": "Secrets, confusion, and ignored intuition.",
        "keywords": "Intuition, mystery, wisdom, secrets",
        "image_url": None
    },
    {
        "name": "The Empress",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Abundance, creativity, nurturing, and growth.",
        "reversed_meaning": "Creative block, dependence, and lack of growth.",
        "keywords": "Abundance, creativity, nurturing, growth",
        "image_url": None
    },
    {
        "name": "The Emperor",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Authority, structure, leadership, and stability.",
        "reversed_meaning": "Control, rigidity, and misuse of power.",
        "keywords": "Authority, leadership, structure, stability",
        "image_url": None
    },
    {
        "name": "The Hierophant",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Tradition, guidance, learning, and spiritual wisdom.",
        "reversed_meaning": "Rebellion, unconventional thinking, and restriction.",
        "keywords": "Tradition, guidance, learning, wisdom",
        "image_url": None
    },
    {
        "name": "The Lovers",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Love, harmony, partnership, and important choices.",
        "reversed_meaning": "Disharmony, conflict, and difficult choices.",
        "keywords": "Love, harmony, choices, partnership",
        "image_url": None
    },
    {
        "name": "The Chariot",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Determination, willpower, victory, and progress.",
        "reversed_meaning": "Lack of direction, aggression, and loss of control.",
        "keywords": "Determination, victory, willpower, progress",
        "image_url": None
    },
    {
        "name": "Strength",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Courage, patience, compassion, and inner strength.",
        "reversed_meaning": "Self-doubt, weakness, and lack of confidence.",
        "keywords": "Courage, patience, compassion, strength",
        "image_url": None
    },
    {
        "name": "The Hermit",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Reflection, solitude, inner guidance, and wisdom.",
        "reversed_meaning": "Isolation, loneliness, and withdrawal.",
        "keywords": "Reflection, solitude, wisdom, guidance",
        "image_url": None
    },
    {
        "name": "Wheel of Fortune",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Change, cycles, luck, and new opportunities.",
        "reversed_meaning": "Bad luck, resistance to change, and setbacks.",
        "keywords": "Change, luck, cycles, opportunity",
        "image_url": None
    },
    {
        "name": "Justice",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Truth, fairness, balance, and accountability.",
        "reversed_meaning": "Injustice, dishonesty, and unfairness.",
        "keywords": "Truth, fairness, balance, accountability",
        "image_url": None
    },
    {
        "name": "The Hanged Man",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Surrender, patience, new perspective, and letting go.",
        "reversed_meaning": "Resistance, delay, and unwillingness to change.",
        "keywords": "Surrender, patience, perspective, sacrifice",
        "image_url": None
    },
    {
        "name": "Death",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Transformation, endings, change, and new beginnings.",
        "reversed_meaning": "Resistance to change, stagnation, and fear of endings.",
        "keywords": "Transformation, endings, change, rebirth",
        "image_url": None
    },
    {
        "name": "Temperance",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Balance, harmony, patience, and moderation.",
        "reversed_meaning": "Imbalance, impatience, and excess.",
        "keywords": "Balance, harmony, patience, moderation",
        "image_url": None
    },
    {
        "name": "The Devil",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Temptation, attachment, materialism, and unhealthy patterns.",
        "reversed_meaning": "Freedom, release, and overcoming limitations.",
        "keywords": "Temptation, attachment, materialism, freedom",
        "image_url": None
    },
    {
        "name": "The Tower",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Sudden change, disruption, revelation, and transformation.",
        "reversed_meaning": "Avoiding change, fear, and delayed disruption.",
        "keywords": "Change, disruption, revelation, transformation",
        "image_url": None
    },
    {
        "name": "The Star",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Hope, healing, inspiration, and renewal.",
        "reversed_meaning": "Hopelessness, discouragement, and lack of faith.",
        "keywords": "Hope, healing, inspiration, renewal",
        "image_url": None
    },
    {
        "name": "The Moon",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Intuition, mystery, uncertainty, and hidden emotions.",
        "reversed_meaning": "Confusion, fear, and hidden truths being revealed.",
        "keywords": "Intuition, mystery, uncertainty, imagination",
        "image_url": None
    },
    {
        "name": "The Sun",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Joy, success, positivity, clarity, and vitality.",
        "reversed_meaning": "Temporary sadness, delays, and lack of enthusiasm.",
        "keywords": "Joy, success, positivity, clarity",
        "image_url": None
    },
    {
        "name": "Judgement",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Awakening, reflection, renewal, and important decisions.",
        "reversed_meaning": "Self-doubt, regret, and refusal to learn from the past.",
        "keywords": "Awakening, renewal, reflection, decisions",
        "image_url": None
    },
    {
        "name": "The World",
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "Completion, achievement, success, and fulfillment.",
        "reversed_meaning": "Incomplete goals, delays, and lack of closure.",
        "keywords": "Completion, achievement, success, fulfillment",
        "image_url": None
    }
]
wands_cards = [
    ("Ace of Wands", "New beginnings, inspiration, creativity, opportunity",
     "Delays, lack of motivation, missed opportunities"),

    ("Two of Wands", "Planning, future decisions, discovery",
     "Fear of the unknown, poor planning, lack of direction"),

    ("Three of Wands", "Expansion, progress, future opportunities",
     "Delays, obstacles, lack of progress"),

    ("Four of Wands", "Celebration, harmony, stability, achievement",
     "Conflict, instability, lack of support"),

    ("Five of Wands", "Competition, conflict, challenges",
     "Avoiding conflict, cooperation, resolution"),

    ("Six of Wands", "Victory, recognition, success, confidence",
     "Failure, lack of recognition, self-doubt"),

    ("Seven of Wands", "Defence, courage, perseverance",
     "Giving up, weakness, lack of confidence"),

    ("Eight of Wands", "Speed, movement, progress, communication",
     "Delays, frustration, lack of progress"),

    ("Nine of Wands", "Resilience, persistence, courage",
     "Exhaustion, giving up, weakness"),

    ("Ten of Wands", "Burden, responsibility, hard work",
     "Release of burdens, delegation, exhaustion"),

    ("Page of Wands", "Exploration, enthusiasm, discovery",
     "Lack of direction, immaturity, bad news"),

    ("Knight of Wands", "Adventure, action, passion, confidence",
     "Impulsiveness, recklessness, frustration"),

    ("Queen of Wands", "Confidence, independence, creativity",
     "Insecurity, jealousy, lack of confidence"),

    ("King of Wands", "Leadership, vision, ambition",
     "Arrogance, impulsiveness, misuse of power")
]
cups_cards = [
    ("Ace of Cups",
     "New love, emotional fulfillment, compassion, and spiritual connection",
     "Emotional blockage, emptiness, and repressed feelings"),

    ("Two of Cups",
     "Partnership, mutual love, harmony, and connection",
     "Conflict, separation, and imbalance"),

    ("Three of Cups",
     "Celebration, friendship, community, and joy",
     "Isolation, overindulgence, and gossip"),

    ("Four of Cups",
     "Contemplation, apathy, and missed opportunities",
     "New awareness, acceptance, and renewed interest"),

    ("Five of Cups",
     "Loss, grief, disappointment, and regret",
     "Acceptance, healing, and moving forward"),

    ("Six of Cups",
     "Nostalgia, childhood memories, kindness, and reunion",
     "Living in the past, immaturity, and unrealistic nostalgia"),

    ("Seven of Cups",
     "Choices, imagination, dreams, and possibilities",
     "Confusion, unrealistic expectations, and poor decisions"),

    ("Eight of Cups",
     "Walking away, seeking deeper meaning, and emotional growth",
     "Fear of change, avoidance, and stagnation"),

    ("Nine of Cups",
     "Wish fulfillment, satisfaction, happiness, and gratitude",
     "Dissatisfaction, materialism, and unfulfilled wishes"),

    ("Ten of Cups",
     "Emotional fulfillment, family happiness, harmony, and love",
     "Family conflict, broken relationships, and unhappiness"),

    ("Page of Cups",
     "Creativity, emotional messages, intuition, and new feelings",
     "Emotional immaturity, insecurity, and disappointing news"),

    ("Knight of Cups",
     "Romance, charm, imagination, and emotional expression",
     "Moodiness, unrealistic expectations, and disappointment"),

    ("Queen of Cups",
     "Compassion, intuition, emotional maturity, and empathy",
     "Emotional dependence, insecurity, and poor boundaries"),

    ("King of Cups",
     "Emotional balance, wisdom, compassion, and maturity",
     "Emotional manipulation, repression, and instability")
]
swords_cards = [
    ("Ace of Swords",
     "Clarity, truth, breakthrough, and new ideas",
     "Confusion, misinformation, and lack of clarity"),

    ("Two of Swords",
     "Difficult decision, balance, and stalemate",
     "Indecision, confusion, and avoidance"),

    ("Three of Swords",
     "Heartbreak, sorrow, grief, and painful truth",
     "Healing, recovery, and releasing pain"),

    ("Four of Swords",
     "Rest, recovery, contemplation, and peace",
     "Restlessness, burnout, and lack of recovery"),

    ("Five of Swords",
     "Conflict, tension, defeat, and winning at all costs",
     "Reconciliation, compromise, and ending conflict"),

    ("Six of Swords",
     "Transition, moving forward, healing, and leaving difficulties behind",
     "Resistance to change, emotional baggage, and delayed progress"),

    ("Seven of Swords",
     "Strategy, independence, secrecy, and careful planning",
     "Deception revealed, dishonesty, and confession"),

    ("Eight of Swords",
     "Restriction, fear, limiting beliefs, and feeling trapped",
     "Freedom, new perspective, and overcoming limitations"),

    ("Nine of Swords",
     "Anxiety, worry, fear, and sleeplessness",
     "Recovery, hope, and releasing anxiety"),

    ("Ten of Swords",
     "Ending, painful transition, betrayal, and closure",
     "Recovery, regeneration, and a new beginning"),

    ("Page of Swords",
     "Curiosity, new ideas, communication, and alertness",
     "Gossip, immaturity, and lack of preparation"),

    ("Knight of Swords",
     "Action, ambition, determination, and fast decisions",
     "Impulsiveness, aggression, and reckless decisions"),

    ("Queen of Swords",
     "Independence, intelligence, honesty, and clear judgment",
     "Bitterness, coldness, and excessive criticism"),

    ("King of Swords",
     "Authority, logic, wisdom, truth, and leadership",
     "Manipulation, tyranny, and misuse of power")
]
pentacles_cards = [
    ("Ace of Pentacles",
     "New financial opportunity, prosperity, stability, and abundance",
     "Missed opportunity, financial instability, and lack of planning"),

    ("Two of Pentacles",
     "Balance, adaptability, time management, and flexibility",
     "Overwhelm, imbalance, and poor time management"),

    ("Three of Pentacles",
     "Teamwork, collaboration, skill, and craftsmanship",
     "Poor teamwork, lack of quality, and lack of recognition"),

    ("Four of Pentacles",
     "Security, saving, stability, and control",
     "Greed, possessiveness, fear of loss, and financial insecurity"),

    ("Five of Pentacles",
     "Financial hardship, isolation, struggle, and insecurity",
     "Recovery, improvement, support, and new opportunities"),

    ("Six of Pentacles",
     "Generosity, charity, support, and balance",
     "Unequal giving, debt, strings attached, and selfishness"),

    ("Seven of Pentacles",
     "Patience, investment, long-term growth, and assessment",
     "Impatience, poor results, and lack of progress"),

    ("Eight of Pentacles",
     "Hard work, skill development, dedication, and mastery",
     "Lack of focus, poor quality, and lack of motivation"),

    ("Nine of Pentacles",
     "Independence, financial security, luxury, and achievement",
     "Financial dependence, insecurity, and overworking"),

    ("Ten of Pentacles",
     "Wealth, family legacy, long-term success, and stability",
     "Financial loss, family conflict, and instability"),

    ("Page of Pentacles",
     "Learning, ambition, new opportunities, and practicality",
     "Lack of progress, laziness, and missed opportunities"),

    ("Knight of Pentacles",
     "Responsibility, hard work, reliability, and persistence",
     "Stagnation, boredom, and lack of progress"),

    ("Queen of Pentacles",
     "Nurturing, practicality, security, and abundance",
     "Financial insecurity, imbalance, and neglect"),

    ("King of Pentacles",
     "Wealth, success, leadership, stability, and business achievement",
     "Greed, materialism, financial failure, and misuse of power")
]
def create_minor_cards(card_list, suit):
    cards = []

    for name, upright, reversed_meaning in card_list:
        cards.append({
            "name": name,
            "arcana": "Minor Arcana",
            "suit": suit,
            "upright_meaning": upright,
            "reversed_meaning": reversed_meaning,
            "keywords": suit,
            "image_url": None
        })

    return cards


minor_arcana = []

minor_arcana.extend(
    create_minor_cards(wands_cards, "Wands")
)

minor_arcana.extend(
    create_minor_cards(cups_cards, "Cups")
)

minor_arcana.extend(
    create_minor_cards(swords_cards, "Swords")
)

minor_arcana.extend(
    create_minor_cards(pentacles_cards, "Pentacles")
)


db = SessionLocal()

try:
    all_cards = major_arcana + minor_arcana
    for card_data in all_cards:

        existing_card = db.query(TarotCard).filter(
            TarotCard.name == card_data["name"]
        ).first()

        if existing_card:
            print(f"Skipping: {card_data['name']} - already exists")
            continue

        card = TarotCard(**card_data)
        db.add(card)

        print(f"Added: {card_data['name']}")

    db.commit()

    print("\nMajor Arcana cards seeded successfully!")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()