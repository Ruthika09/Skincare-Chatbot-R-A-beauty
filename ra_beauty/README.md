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




