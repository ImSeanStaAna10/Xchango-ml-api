# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

ENABLE_TRANSLATION = os.getenv("ENABLE_TRANSLATION", "true").lower() == "true"
LIBRETRANSLATE_URL = os.getenv("LIBRETRANSLATE_URL", "https://translate.astian.org/translate")

TEXT_WEIGHT = float(os.getenv("TEXT_WEIGHT", "0.6"))
IMAGE_WEIGHT = float(os.getenv("IMAGE_WEIGHT", "0.4"))

# Confidence thresholds (0-1 floats)
CONF_LOW = float(os.getenv("CONF_LOW", "0.40"))
CONF_HIGH = float(os.getenv("CONF_HIGH", "0.80"))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Safety guard: weights should be within 0..1
if TEXT_WEIGHT < 0 or IMAGE_WEIGHT < 0:
    TEXT_WEIGHT, IMAGE_WEIGHT = 0.6, 0.4
if TEXT_WEIGHT + IMAGE_WEIGHT == 0:
    TEXT_WEIGHT, IMAGE_WEIGHT = 1.0, 0.0
