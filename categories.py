# categories.py

# Master category list (front-end compatible)
CATEGORIES = [
    "Electronics",
    "Fashion",
    "Books",
    "Home and Living",
    "Sports and Outdoors",
    "Toys",
    "Tools and DIY",
    "Health and Beauty",
    "Pets and Animals",
    "Plants and Gardening",
    "Cars and Vehicles",
    "Collectibles and Art",
    "Musical Instruments",
    "Others",
]

# Text prompts fed to CLIP for better discrimination
CATEGORY_PROMPTS = [
    "a product photo of an electronic device or accessory",
    "a product photo of fashion apparel, shoes, or accessories",
    "a product photo of a book or printed reading material",
    "a product photo for home and living",
    "a product photo for sports and outdoor gear",
    "a product photo of a toy or kids item",
    "a product photo of tools or DIY equipment",
    "a product photo for health and beauty product",
    "a product photo for pets and animals",
    "a product photo of plants or gardening tools",
    "a product photo of cars, vehicles, parts or accessories",
    "a product photo of collectibles or art piece",
    "a product photo of a musical instrument or gear",
    "a product photo of miscellaneous or others",
]

# Keyword boosts (EN + Tagalog). Lowercase lahat.
# Kapag may match sa title, tataas ang score ng category na ‘yon.
KEYWORDS_BY_CATEGORY = {
    "Fashion": [
        "sapatos","shoes","sneakers","sandals","tsinelas","heels",
        "shirt","tshirt","t-shirt","damit","pantalon","pants","shorts",
        "palda","skirt","jacket","hoodie","sando","cap","hat","bag","backpack",
        "dress","jersey","adidas","nike","jordan","uniqlo","shein",
    ],
    "Electronics": [
        "phone","iphone","samsung","cellphone","selpon","telepono",
        "charger","kargador","powerbank","earphones","headset","headphones",
        "laptop","notebook","pc","computer","mouse","keyboard","monitor",
        "camera","gopro","tv","speaker","router","tablet","ipad","usb","cable",
    ],
    "Sports and Outdoors": [
        "basketball","bola","pang basketball","soccer","football",
        "racket","tennis","badminton","bike","bisikleta","dumbbell",
        "gym","weights","skateboard","jogging","running","cleats",
    ],
    "Pets and Animals": [
        "aso","pusa","dog","cat","puppy","kitten","leash","kulungan",
        "dog food","cat food","pagkain ng aso","pagkain ng pusa","pet",
        "aquarium","fish","pagkain ng isda","bird",
    ],
    "Home and Living": [
        "furniture","sofa","table","chair","kitchen","lutuan","kalan","kawali",
        "kurtina","carpet","vacuum","appliances","ref","refrigerator","aircon",
        "electric fan","bed","mattress","unan","pillow","ilaw","lamp","plantita",
    ],
    "Toys": [
        "toy","laruan","lego","figure","doll","rc car","nerf","plushie",
    ],
    "Tools and DIY": [
        "tools","martilyo","pako","wrench","drill","screwdriver","lanseta",
        "grinder","kawad","pintura","saw","lagari","pliers",
    ],
    "Health and Beauty": [
        "makeup","skincare","lotion","shampoo","conditioner","vitamins",
        "supplements","perfume","cologne","sabong pampaganda","foundation",
        "lipstick","serum","sunscreen","toner",
    ],
    "Books": [
        "book","libro","novel","manga","komiks","textbook","reviewer",
    ],
    "Plants and Gardening": [
        "plant","halaman","garden","gardening","soil","pataba","fertilizer",
        "pot","plant pot","tanim",
    ],
    "Cars and Vehicles": [
        "kotse","sasakyan","car","motor","motorcycle","helmet","gulong","tire",
        "rims","spoiler","car seat","dashcam",
    ],
    "Collectibles and Art": [
        "collectible","koleksyon","art","painting","print","poster","funko","figure",
        "photocard","pc","album","bini","kpop","trading card","tcg",
    ],
    "Musical Instruments": [
        "guitar","gitara","bass","drums","piano","keyboard","violin","ukulele",
        "amplifier","amp","mixer","mic","microphone",
    ],
    # Others intentionally left empty to act as sink category
}
