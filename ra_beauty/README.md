# R A Beauty — Chatbot Assistant

A Django-powered chatbot for a skin care brand ("R A Beauty").
No API keys, no internet connection, no AI model needed — it's a smart,
rule-based conversational bot that remembers where you are in the chat
(using Django sessions) and guides customers through:

- 🔍 **Finding a product** — browse by category (Hair / Face / Body /
  Fragrance) → sub-category → see stock, or get a personalized pick
- ❓ **Asking a question** — shipping, ingredients, returns, cruelty-free
- ⭐ **Reviews** — view sample reviews or "submit" your own (demo only,
  not saved permanently)
- 🌸 **Know Your Skin/Hair** — a short quiz (scalp/skin type + concern)
  that recommends 1–2 matching dummy products

Pink, floral, honey-toned UI with clickable quick-reply buttons.

> 📌 **Note:** This is a portfolio/demo project — there is no live hosted
> link. To see it in action, either watch the demo video below or run it
> locally on your own machine using the steps in this README.

## 🎥 Demo Video

[Add your demo video link here — e.g. a YouTube/Loom link, or embed a
`.gif`/`.mp4` file if uploading directly to the repo]

## How to run it

1. Install Python 3.9+ if you don't have it: https://www.python.org/downloads/
   (tick **"Add python.exe to PATH"** during install on Windows)

2. Open a terminal in this folder (`chatbot_project`).

3. Install Django:
   ```
   pip install -r requirements.txt
   ```

4. Set up the local database (just a small file, no setup needed):
   ```
   python manage.py migrate
   ```

5. Run the server:
   ```
   python manage.py runserver
   ```

6. Open your browser to:
   ```
   http://127.0.0.1:8000/
   ```

## Editing the product catalog

Open `chat/catalog.py`. It's a plain Python dictionary — add, rename, or
remove products there. Each product has:
```python
{"name": "Aloe Vera Face Wash", "tags": ["dry", "sensitive"], "stock": True}
```
- `tags` control which quiz answers recommend this product (e.g. a
  product tagged `"dry"` gets suggested when the customer picks "Dry" skin/scalp).
- `stock` controls whether it shows as In Stock or "We don't have it right now."

FAQ answers live in the same file under `FAQ = {...}`.
Sample reviews are under `SAMPLE_REVIEWS = [...]`.

## Editing the conversation logic

`chat/bot.py` controls the flow (what's asked, in what order, what
triggers what). Each flow — product search, questions, reviews, the
quiz — has its own function (`handle_product`, `handle_question`,
`handle_review`, `handle_quiz`).

## About Google Colab

Colab is built for notebooks, not for hosting a live website, so Django
doesn't fit it well — there's no clean way to keep a server running and
reachable there. Running it locally (as above) or later deploying free
to Render / Railway / PythonAnywhere is the more reliable route once
you're happy with the demo.

## Notes on this being a demo

- No real database of products/customers — everything lives in
  `chat/catalog.py` as Python data, easy to read and edit.
- "Submitted" reviews aren't actually saved anywhere (no persistent
  storage) — good enough to demo the flow, not for production.
- No login/signup — this is a pure chatbot demo, not a full e-commerce site.
