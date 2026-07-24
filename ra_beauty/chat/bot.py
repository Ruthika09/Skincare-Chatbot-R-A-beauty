"""
Conversational logic for R A Beauty chatbot.
Uses the Django session (passed in as `session`) to remember which step
of the conversation the customer is in, so it can hold a multi-step
back-and-forth instead of just one-off replies.
"""

import re

from .catalog import CATALOG, FAQ, SAMPLE_REVIEWS

MAIN_MENU_OPTIONS = [
    "🔍 Looking for a product",
    "❓ Have a question",
    "⭐ Reviews",
    "🌸 Know Your Skin/Hair",
]

CATEGORIES = ["Hair", "Face", "Body", "Fragrance"]

FAQ_TOPICS = ["Shipping", "Ingredients", "Return Policy", "Cruelty-Free", "⬅ Back to Menu"]

BACK_OPTION = "⬅ Back to Menu"


def norm(text: str) -> str:
    """Lowercase and strip emoji/punctuation for loose matching."""
    return re.sub(r'[^a-z0-9 ]', '', text.lower()).strip()


def match_option(message: str, options):
    """Match a typed or clicked message against a list of button options."""
    m = norm(message)
    for opt in options:
        if norm(opt) == m:
            return opt
    for opt in options:
        o = norm(opt)
        if o and (m in o or o in m):
            return opt
    return None


def greet():
    return ("Hi there! Welcome to 🌸 R A Beauty 🌸 — where honey meets nature. "
            "What can I help you with today?")


def reset_state(session):
    session['state'] = {'flow': 'main'}


def get_bot_response(session, message):
    message = (message or '').strip()
    state = session.get('state', {'flow': 'main'})

    if match_option(message, ['start over', 'restart', 'main menu', BACK_OPTION]) and state.get('flow') != 'main':
        reset_state(session)
        return greet(), MAIN_MENU_OPTIONS

    flow = state.get('flow', 'main')

    if flow == 'main':
        return handle_main(session, state, message)
    elif flow == 'product':
        return handle_product(session, state, message)
    elif flow == 'question':
        return handle_question(session, state, message)
    elif flow == 'review':
        return handle_review(session, state, message)
    elif flow == 'quiz':
        return handle_quiz(session, state, message)

    reset_state(session)
    return greet(), MAIN_MENU_OPTIONS


# ---------------------------------------------------------------- MAIN MENU
def handle_main(session, state, message):
    choice = match_option(message, MAIN_MENU_OPTIONS)

    if choice is None:
        return greet(), MAIN_MENU_OPTIONS

    if choice == MAIN_MENU_OPTIONS[0]:  # Looking for a product
        state = {'flow': 'product', 'step': 'category'}
        session['state'] = state
        return "Lovely! Which category are you interested in? 🌷", CATEGORIES + [BACK_OPTION]

    if choice == MAIN_MENU_OPTIONS[1]:  # Question
        state = {'flow': 'question', 'step': 'category'}
        session['state'] = state
        return "Sure, happy to help! Which category is your question about?", CATEGORIES + [BACK_OPTION]

    if choice == MAIN_MENU_OPTIONS[2]:  # Reviews
        state = {'flow': 'review', 'step': 'category'}
        session['state'] = state
        return "Great, let's find that product. Which category?", CATEGORIES + [BACK_OPTION]

    if choice == MAIN_MENU_OPTIONS[3]:  # Know your skin/hair
        state = {'flow': 'quiz', 'step': 'type'}
        session['state'] = state
        return "Let's find your perfect match! Is this for your Hair or your Skin (face)?", ["Hair", "Face", BACK_OPTION]

    reset_state(session)
    return greet(), MAIN_MENU_OPTIONS


# ------------------------------------------------------------- PRODUCT FLOW
def handle_product(session, state, message):
    step = state.get('step')

    if step == 'category':
        cat = match_option(message, CATEGORIES)
        if not cat:
            return "Please pick one of the categories below. 🌸", CATEGORIES + [BACK_OPTION]
        state['category'] = cat
        state['step'] = 'subcategory'
        session['state'] = state
        subcats = list(CATALOG[cat].keys())
        return f"Here's what we have under {cat}:", subcats + [BACK_OPTION]

    if step == 'subcategory':
        cat = state.get('category')
        subcats = list(CATALOG.get(cat, {}).keys())
        subcat = match_option(message, subcats)
        if not subcat:
            return "Please choose one of these options.", subcats + [BACK_OPTION]
        state['subcategory'] = subcat
        state['step'] = 'action'
        session['state'] = state

        options = ["📦 See available stock"]
        if cat in ("Hair", "Face"):
            options.append("🌸 Know Your " + ("Hair" if cat == "Hair" else "Skin"))
        options.append(BACK_OPTION)
        return f"Great choice — {subcat}. What would you like to do?", options

    if step == 'action':
        cat = state.get('category')
        subcat = state.get('subcategory')

        if match_option(message, ["See available stock"]):
            products = CATALOG[cat][subcat]
            lines = []
            for p in products:
                status = "✅ In Stock" if p['stock'] else "❌ We don't have it right now"
                lines.append(f"• {p['name']} — {status}")
            reply = f"Here's our {subcat} range:\n" + "\n".join(lines)
            session['state'] = {'flow': 'main'}
            return reply + "\n\nAnything else I can help with?", MAIN_MENU_OPTIONS

        if "know your" in norm(message):
            quiz_type = 'hair' if cat == 'Hair' else 'face'
            state = {'flow': 'quiz', 'step': 'q1', 'quiz_type': quiz_type, 'answers': {}}
            session['state'] = state
            return start_quiz_question(quiz_type)

        options = ["📦 See available stock"]
        if cat in ("Hair", "Face"):
            options.append("🌸 Know Your " + ("Hair" if cat == "Hair" else "Skin"))
        options.append(BACK_OPTION)
        return "Please choose one of the options below.", options

    reset_state(session)
    return greet(), MAIN_MENU_OPTIONS


# ------------------------------------------------------------ QUESTION FLOW
def handle_question(session, state, message):
    step = state.get('step')

    if step == 'category':
        cat = match_option(message, CATEGORIES)
        if not cat:
            return "Which category is your question about?", CATEGORIES + [BACK_OPTION]
        state['category'] = cat
        state['step'] = 'topic'
        session['state'] = state
        return "What would you like to know?", FAQ_TOPICS

    if step == 'topic':
        topic = match_option(message, list(FAQ.keys()))
        if not topic:
            return "Please pick a topic below.", FAQ_TOPICS
        answer = FAQ[topic]
        session['state'] = {'flow': 'main'}
        return answer + "\n\nAnything else I can help with?", MAIN_MENU_OPTIONS

    reset_state(session)
    return greet(), MAIN_MENU_OPTIONS


# ------------------------------------------------------------- REVIEW FLOW
def handle_review(session, state, message):
    step = state.get('step')

    if step == 'category':
        cat = match_option(message, CATEGORIES)
        if not cat:
            return "Which category is the product in?", CATEGORIES + [BACK_OPTION]
        state['category'] = cat
        state['step'] = 'subcategory'
        session['state'] = state
        subcats = list(CATALOG[cat].keys())
        return "Which type of product?", subcats + [BACK_OPTION]

    if step == 'subcategory':
        cat = state.get('category')
        subcats = list(CATALOG.get(cat, {}).keys())
        subcat = match_option(message, subcats)
        if not subcat:
            return "Please choose one of these options.", subcats + [BACK_OPTION]
        state['subcategory'] = subcat
        state['step'] = 'product'
        session['state'] = state
        names = [p['name'] for p in CATALOG[cat][subcat]]
        return "Which product?", names + [BACK_OPTION]

    if step == 'product':
        cat = state.get('category')
        subcat = state.get('subcategory')
        names = [p['name'] for p in CATALOG[cat][subcat]]
        product = match_option(message, names)
        if not product:
            return "Please pick a product from the list.", names + [BACK_OPTION]
        state['product'] = product
        state['step'] = 'action'
        session['state'] = state
        return f"Would you like to view reviews for {product}, or write your own?", ["View Reviews", "Write a Review", BACK_OPTION]

    if step == 'action':
        if match_option(message, ["View Reviews"]):
            lines = [f"⭐ {r['rating']}/5 — {r['user']}: \"{r['comment']}\"" for r in SAMPLE_REVIEWS]
            reply = f"Here's what customers say about {state.get('product')}:\n" + "\n".join(lines)
            session['state'] = {'flow': 'main'}
            return reply + "\n\nAnything else I can help with?", MAIN_MENU_OPTIONS

        if match_option(message, ["Write a Review"]):
            state['step'] = 'rating'
            session['state'] = state
            return "How many stars would you give it?", ["1", "2", "3", "4", "5"]

        return "Would you like to View Reviews or Write a Review?", ["View Reviews", "Write a Review", BACK_OPTION]

    if step == 'rating':
        rating = match_option(message, ["1", "2", "3", "4", "5"])
        if not rating:
            return "Please pick a star rating from 1 to 5.", ["1", "2", "3", "4", "5"]
        state['rating'] = rating
        state['step'] = 'comment'
        session['state'] = state
        return "Thanks! Want to add a short comment? (or type 'skip')", []

    if step == 'comment':
        rating = state.get('rating')
        product = state.get('product')
        session['state'] = {'flow': 'main'}
        reply = (f"🌸 Thank you! Your {rating}-star review for {product} has been submitted.\n\n"
                 f"Anything else I can help with?")
        return reply, MAIN_MENU_OPTIONS

    reset_state(session)
    return greet(), MAIN_MENU_OPTIONS


# --------------------------------------------------------------- QUIZ FLOW
HAIR_QUESTIONS = {
    'q1': ("Is your scalp dry, oily, or normal?", ["Dry", "Oily", "Normal"], 'scalp'),
    'q2': ("Is your hair straight, wavy, or curly?", ["Straight", "Wavy", "Curly"], 'hairtype'),
    'q3': ("Any specific concern?", ["Hairfall", "Dandruff", "Frizz", "None"], 'concern'),
}
HAIR_ORDER = ['q1', 'q2', 'q3']

FACE_QUESTIONS = {
    'q1': ("Is your skin dry, oily, combination, or sensitive?", ["Dry", "Oily", "Combination", "Sensitive"], 'skintype'),
    'q2': ("What's your main concern?", ["Acne", "Dark spots", "Aging", "Dullness", "None"], 'concern'),
}
FACE_ORDER = ['q1', 'q2']


def start_quiz_question(quiz_type):
    order = HAIR_ORDER if quiz_type == 'hair' else FACE_ORDER
    qs = HAIR_QUESTIONS if quiz_type == 'hair' else FACE_QUESTIONS
    text, options, _ = qs[order[0]]
    return text, options + [BACK_OPTION]


def handle_quiz(session, state, message):
    step = state.get('step')

    if step == 'type':
        t = match_option(message, ["Hair", "Face"])
        if not t:
            return "Is this for your Hair or your Skin (face)?", ["Hair", "Face", BACK_OPTION]
        quiz_type = t.lower()
        state = {'flow': 'quiz', 'step': 'q1', 'quiz_type': quiz_type, 'answers': {}}
        session['state'] = state
        return start_quiz_question(quiz_type)

    quiz_type = state.get('quiz_type', 'hair')
    order = HAIR_ORDER if quiz_type == 'hair' else FACE_ORDER
    qs = HAIR_QUESTIONS if quiz_type == 'hair' else FACE_QUESTIONS

    if step in order:
        text, options, key = qs[step]
        answer = match_option(message, options)
        if not answer:
            return text, options + [BACK_OPTION]

        answers = state.get('answers', {})
        answers[key] = answer.lower()
        state['answers'] = answers

        idx = order.index(step)
        if idx + 1 < len(order):
            next_step = order[idx + 1]
            state['step'] = next_step
            session['state'] = state
            next_text, next_options, _ = qs[next_step]
            return next_text, next_options + [BACK_OPTION]
        else:
            reply = recommend(quiz_type, answers)
            session['state'] = {'flow': 'main'}
            return reply + "\n\nAnything else I can help with?", MAIN_MENU_OPTIONS

    reset_state(session)
    return greet(), MAIN_MENU_OPTIONS


def recommend(quiz_type, answers):
    tags = set()
    if quiz_type == 'hair':
        tags.add(answers.get('scalp', ''))
        concern = answers.get('concern', 'none')
        if concern != 'none':
            tags.add(concern)
        category = 'Hair'
        intro = "Based on your hair type"
    else:
        tags.add(answers.get('skintype', ''))
        concern = answers.get('concern', 'none')
        if concern != 'none':
            tags.add(concern.replace(' ', ''))
            tags.add(concern)
        category = 'Face'
        intro = "Based on your skin type"

    matches = []
    for subcat, products in CATALOG[category].items():
        for p in products:
            if tags & set(p['tags']):
                matches.append(p)

    if not matches:
        for subcat in list(CATALOG[category].keys())[:2]:
            matches.append(CATALOG[category][subcat][0])

    seen = set()
    unique_matches = []
    for p in matches:
        if p['name'] not in seen:
            unique_matches.append(p)
            seen.add(p['name'])
    unique_matches = unique_matches[:2]

    names = " and ".join(f"{p['name']}" for p in unique_matches)
    return f"{intro}, I'd recommend: {names} 🌸"
