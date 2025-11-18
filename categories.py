
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
# Kapag may match sa title, tataas ang score ng category na yon.
KEYWORDS_BY_CATEGORY = {
    "Fashion": [
        "sapatos","shoes","sneakers","sandals","tsinelas","heels",
        "shirt","tshirt","t-shirt","damit","pantalon","pants","shorts",
        "palda","skirt","jacket","hoodie","sando","cap","hat","bag","backpack",
        "dress","jersey","adidas","nike","jordan","uniqlo","shein",
        "hoodies","sneakerhead","jogger","tracksuit","beanie",
        "scarf","gloves","sling bag","pouch","wallet","belt","earrings",
        "necklace","rings","bracelet","socks","underwear","lingerie",
        "swimsuit","flipflops","loafers","formal shoes",
    ],
    "Electronics": [
        "phone","iphone","samsung","cellphone","selpon","telepono",
        "charger","kargador","powerbank","earphones","headset","headphones",
        "laptop","notebook","pc","computer","mouse","keyboard","monitor",
        "camera","gopro","tv","speaker","router","tablet","ipad","usb","cable",
        "smartwatch","fitbit","apple watch","android watch","camera lens",
        "drone","gimbal","projector","ps5","playstation","xbox","nintendo",
        "console","joystick","controller","hdmi","ssd","hard drive","ram",
        "graphics card","gpu","motherboard","printer","scanner","webcam",
    ],
    "Sports and Outdoors": [
        "basketball","bola","pang basketball","soccer","football",
        "racket","tennis","badminton","bike","bisikleta","dumbbell",
        "gym","weights","skateboard","jogging","running","cleats","ball",
        "treadmill","elliptical","yoga mat","resistance band","boxing gloves",
        "swimwear","swimming goggles","kayak","canoe","tent","sleeping bag",
        "hiking boots","trekking pole","camping stove","fishing rod","kayak paddle",
    ],
    "Pets and Animals": [
        "aso","pusa","dog","cat","puppy","kitten","leash","kulungan",
        "dog food","cat food","pagkain ng aso","pagkain ng pusa","pet",
        "aquarium","fish","pagkain ng isda","bird",
        "hamster","rabbit","guinea pig","parrot","canary","bird cage",
        "aquatic plant","dog toy","cat toy","pet carrier","pet bed","aquarium filter",
        "fish tank","pet grooming","claw trimmer","scratch post",
    ],
    "Home and Living": [
        "furniture","sofa","table","chair","kitchen","lutuan","kalan","kawali",
        "kurtina","carpet","vacuum","appliances","ref","refrigerator","aircon",
        "electric fan","bed","mattress","unan","pillow","ilaw","lamp","plantita",
        "blender","mixer","oven","toaster","coffee maker","cutlery","knife set",
        "vase","candle","wall art","mirror","clock","rug","curtain rod",
        "toolbox","drill set","paint brush","shelf","storage box","laundry basket",
    ],
    "Toys": [
        "toy","laruan","lego","figure","doll","rc car","nerf","plushie",
        "puzzle","board game","monopoly","scrabble","action figure",
        "lego set","playdoh","nerf gun","rc drone","educational toy",
    ],
    "Tools and DIY": [
        "tools","martilyo","pako","wrench","drill","screwdriver","lanseta",
        "grinder","kawad","pintura","saw","lagari","pliers",
        "level","measuring tape","pliers set","screw set","saw blade","welding mask",
        "helmet","drill bits","sandpaper","paint roller","paint tray","adhesive","glue gun",
    ],
    "Health and Beauty": [
        "makeup","skincare","lotion","shampoo","conditioner","vitamins",
        "supplements","perfume","cologne","sabong pampaganda","foundation",
        "lipstick","serum","sunscreen","toner",
        "hair dryer","curler","straightener","facial mask","toner pad",
        "body wash","hand cream","foot cream","essence","bath bomb",
        "massage oil","aromatherapy","protein powder","omega","collagen",
    ],
    "Books": [
        "book","libro","novel","manga","komiks","textbook","reviewer",
        "biography","history","science","fantasy","mystery","thriller",
        "romance","children book","cookbook","dictionary","atlas","magazine",
    ],
    "Plants and Gardening": [
        "plant","halaman","garden","gardening","soil","pataba","fertilizer",
        "pot","plant pot","tanim",
        "succulent","cactus","bonsai","orchid","seed","fertilizer","soil mix",
        "watering can","hose","pruner","trowel","plant pot cover","planter stand",
    ],
    "Cars and Vehicles": [
        "kotse","sasakyan","car","motor","motorcycle","helmet","gulong","tire",
        "rims","spoiler","car seat","dashcam",
        "engine oil","car mat","seat cover","headlight","taillight","wiper",
        "battery","spark plug","car wax","air freshener","roof rack","gps",
    ],
    "Collectibles and Art": [
        "collectible","koleksyon","art","painting","print","poster","funko","figure",
        "photocard","pc","album","bini","kpop","trading card","tcg",
        "miniature","figurine","action figure","vinyl","poster","comic book",
        "art print","painting set","sketchbook","drawing pen","puzzle","memorabilia",
    ],
    "Musical Instruments": [
        "guitar","gitara","bass","drums","piano","keyboard","violin","ukulele",
        "amplifier","amp","mixer","mic","microphone",
        "drumsticks","sheet music","guitar pick","capo","music stand",
        "ukulele strap","piano bench","synthesizer","loop pedal","effects pedal",
    ],
    # Others intentionally left empty to act as sink category
    "Others": [
        "gift","bundle","miscellaneous","random","handmade","custom","used","preloved"
    ]
}
