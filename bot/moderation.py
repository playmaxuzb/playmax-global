"""Bad-word and spam filter for 5 languages (Dari/Persian, Uzbek, Russian, English, Arabic)."""
import re

# whole words (exact match after normalising)
WORDS = {
    # Dari / Persian
    "کس", "کیر", "کون", "جنده", "کسکش", "کسخل", "حرومزاده", "حرامزاده", "لاشی", "کونی", "گوه", "مادرجنده", "پدرسگ", "بیناموس", "بی‌ناموس", "قحبه",
    # Arabic
    "كس", "زب", "شرموط", "شرموطة", "منيوك", "عرص", "خول", "قحبة", "متناك", "ابن_الكلب", "زبالة", "حقير",
    # Uzbek (Latin + Cyrillic)
    "jalab", "qanjiq", "sik", "siktir", "skay", "haromi", "itvachcha", "dalbayob", "ahmoq", "onangni", "eshak", "xunasa",
    "жалаб", "қанжиқ", "харомi", "итвачча", "далбаёб",
    # English
    "fuck", "fucking", "fucker", "shit", "bitch", "bastard", "asshole", "cunt", "dick", "whore", "slut", "motherfucker", "idiot", "stupid",
    # Russian short ones
    "сука", "суки", "мудак", "гандон", "дебил", "урод", "тварь", "чмо", "шлюха", "лох",
}
# stems (substring match, only long/unambiguous ones)
STEMS = ["хуй", "хуе", "хуё", "пизд", "ебат", "ебан", "ёбан", "заеб", "уеб", "бляд", "блят", "пидор", "пидар", "залуп", "долбоё", "долбое",
         "fuck", "shit", "جنده", "شرموط", "منيوك", "dalbayob", "qanjiq"]

LINK = re.compile(r"(https?://|www\.|t\.me/|telegram\.me/|\b[\w-]+\.(com|net|org|ru|uz|af|io|me|link|xyz|top)\b|@\w{4,})", re.I)
WORD = re.compile(r"[\w؀-ۿ‌]+", re.U)

ARABIC_FIX = str.maketrans({"ي": "ی", "ك": "ک", "ة": "ه", "ى": "ی"})


def _norm(text):
    return (text or "").lower().replace("ё", "е")


def bad_words(text):
    t = _norm(text)
    words = set(WORD.findall(t))
    fixed = {w.translate(ARABIC_FIX) for w in words}
    if words & WORDS or fixed & {w.translate(ARABIC_FIX) for w in WORDS}:
        return True
    return any(s in t for s in STEMS)


def has_link(text):
    return bool(LINK.search(text or ""))


def clean(text):
    """True when text is acceptable for the market."""
    return not bad_words(text) and not has_link(text)
