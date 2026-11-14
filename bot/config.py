"""PlayMax Global — shared links and settings."""
import os

TOKEN = os.environ.get("TG_AF_TOKEN", "")
CHANNEL = os.environ.get("TG_CHANNEL", "@PlaymaxUZ_AF")
BOT_USERNAME = "PLAYMAXCatalogBot"
REPO_RAW = "https://raw.githubusercontent.com/playmaxuzb/playmax-global/main/"

LANGS = ["fa", "uz", "ru", "en", "ar"]
FLAGS = {"fa": "🇦🇫", "uz": "🇺🇿", "ru": "🇷🇺", "en": "🇬🇧", "ar": "🇸🇦"}
LANG_NAMES = {"fa": "دری", "uz": "O‘zbekcha", "ru": "Русский", "en": "English", "ar": "العربية"}

LINKS = {
    "site": "https://playmaxuz.com",
    "linkbio": "https://lnk.bio/PLAYMAX.UZ.AF",
    "ig_af": "https://www.instagram.com/playmax.uz.af/",
    "ig_uz": "https://www.instagram.com/playmax.uz/",
    "tiktok": "https://www.tiktok.com/@playmax.uz.af",
    "tg_global": "https://t.me/PlaymaxUZ_AF",
    "tg_uz": "https://t.me/playmax_box",
    "wa_af": "https://wa.me/93779901111",
    "email": "playmax.uzb@gmail.com",
    "office_map": "https://yandex.com/maps/?pt=69.236804,41.199058&z=17&l=map",
    "factory_map": "https://yandex.com/maps/?pt=69.151245,41.209238&z=17&l=map",
}

PHONES_UZ = ["+998 97 089 94 99", "+998 50 780 02 79"]
PHONE_AF = "+93 77 990 1111"

OFFICE = (41.199058, 69.236804)
FACTORY = (41.209238, 69.151245)

# Telegram user language_code -> our language
def map_lang(code):
    code = (code or "").lower()
    if code.startswith(("fa", "ps", "prs")):
        return "fa"
    if code.startswith("uz"):
        return "uz"
    if code.startswith(("ru", "uk", "be", "kk", "ky", "tg")):
        return "ru"
    if code.startswith("ar"):
        return "ar"
    return "en"
