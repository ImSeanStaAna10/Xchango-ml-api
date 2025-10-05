# translator.py
import json
import os
import re
import time
from typing import Dict

import requests

from settings import ENABLE_TRANSLATION, LIBRETRANSLATE_URL

CACHE_DIR = "cache"
CACHE_PATH = os.path.join(CACHE_DIR, "translations.json")
CACHE_TTL_SECONDS = 60 * 60 * 24 * 7  # 7 days

# In-memory cache
_mem_cache: Dict[str, Dict] = {}

def _ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)

def _load_cache():
    _ensure_cache_dir()
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                # purge stale
                now = time.time()
                for k, v in list(data.items()):
                    if now - v.get("ts", 0) > CACHE_TTL_SECONDS:
                        data.pop(k, None)
                return data
        except Exception:
            return {}
    return {}

def _save_cache():
    _ensure_cache_dir()
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(_mem_cache, f, ensure_ascii=False)
    except Exception:
        pass

# init cache on import
_mem_cache.update(_load_cache())

_clean_re = re.compile(r"[^0-9A-Za-zÀ-ÖØ-öø-ÿ\s\-_/]+")

def clean_text(text: str) -> str:
    text = (text or "").strip().lower()
    text = _clean_re.sub("", text)
    # compress whitespace
    text = re.sub(r"\s+", " ", text)
    return text

def translate_to_english(text: str) -> str:
    """Translate Tagalog/Taglish to English (with cache + graceful fallback)."""
    if not ENABLE_TRANSLATION:
        return text

    cleaned = clean_text(text)
    if not cleaned:
        return text

    # cache hit?
    cached = _mem_cache.get(cleaned)
    if cached and time.time() - cached.get("ts", 0) <= CACHE_TTL_SECONDS:
        return cached.get("en", text)

    try:
        resp = requests.post(
            LIBRETRANSLATE_URL,
            params={"q": cleaned, "source": "auto", "target": "en"},
            timeout=6,
        )
        resp.raise_for_status()
        data = resp.json()
        translated = data.get("translatedText") or cleaned
    except Exception:
        # fallback: identity
        translated = cleaned

    # save cache
    _mem_cache[cleaned] = {"en": translated, "ts": time.time()}
    _save_cache()
    return translated
