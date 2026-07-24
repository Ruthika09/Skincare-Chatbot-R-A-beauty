"""
Dummy product catalog for R A Beauty demo chatbot.
Each product has: name, tags (used for quiz recommendations), stock (True/False)
Edit this file to add/remove/rename real products later.
"""

CATALOG = {
    "Hair": {
        "Shampoo": [
            {"name": "Honey Almond Nourishing Shampoo", "tags": ["dry", "normal"], "stock": True},
            {"name": "Rose Water Clarifying Shampoo", "tags": ["oily"], "stock": True},
            {"name": "Neem Anti-Dandruff Shampoo", "tags": ["dandruff"], "stock": False},
        ],
        "Conditioner": [
            {"name": "Honey Silk Deep Conditioner", "tags": ["dry"], "stock": True},
            {"name": "Aloe Vera Light Conditioner", "tags": ["oily", "normal"], "stock": True},
        ],
        "Hair Oil": [
            {"name": "Rosemary Growth Oil", "tags": ["hairfall"], "stock": True},
            {"name": "Jasmine Shine & Frizz Oil", "tags": ["frizz"], "stock": True},
        ],
        "Hair Mask": [
            {"name": "Honey Repair Hair Mask", "tags": ["dry", "frizz"], "stock": True},
        ],
    },
    "Face": {
        "Cleanser": [
            {"name": "Aloe Vera Gentle Face Wash", "tags": ["dry", "sensitive"], "stock": True},
            {"name": "Rose Water Foaming Cleanser", "tags": ["oily", "combination"], "stock": True},
        ],
        "Serum": [
            {"name": "Honey Glow Vitamin C Serum", "tags": ["dullness"], "stock": True},
            {"name": "Lavender Calming Serum", "tags": ["sensitive", "acne"], "stock": True},
        ],
        "Moisturizer": [
            {"name": "Aloe Vera Hydrating Gel Moisturizer", "tags": ["dry"], "stock": True},
            {"name": "Rose Oil-Free Moisturizer", "tags": ["oily", "combination"], "stock": False},
        ],
        "Sunscreen": [
            {"name": "Honey Silk SPF 50 Sunscreen", "tags": ["dry", "oily", "combination", "sensitive"], "stock": True},
        ],
    },
    "Body": {
        "Body Lotion": [
            {"name": "Honey Shea Body Butter Lotion", "tags": ["dry"], "stock": True},
        ],
        "Body Wash": [
            {"name": "Rose Jasmine Body Wash", "tags": [], "stock": True},
        ],
        "Body Scrub": [
            {"name": "Honey Sugar Body Scrub", "tags": [], "stock": True},
        ],
    },
    "Fragrance": {
        "Perfume": [
            {"name": "Jasmine Bloom Eau de Parfum", "tags": [], "stock": True},
            {"name": "Rose Petal Eau de Toilette", "tags": [], "stock": False},
        ],
        "Body Mist": [
            {"name": "Honey Blossom Body Mist", "tags": [], "stock": True},
        ],
    },
}

FAQ = {
    "Shipping": "We ship across India within 3-5 business days. Orders above ₹499 get free shipping!",
    "Ingredients": "All our products are made with natural ingredients like aloe vera, honey, and rose extracts — no parabens or sulfates.",
    "Return Policy": "You can return any unopened product within 7 days of delivery for a full refund.",
    "Cruelty-Free": "Yes! R A Beauty never tests on animals. 🐰",
}

SAMPLE_REVIEWS = [
    {"user": "Ananya", "rating": 5, "comment": "Loved the honey scent, my skin feels so soft!"},
    {"user": "Priya", "rating": 4, "comment": "Great product, a little pricey but worth it."},
    {"user": "Meera", "rating": 5, "comment": "My go-to now, smells like a garden!"},
]
