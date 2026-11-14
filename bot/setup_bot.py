"""Bot profile per language: command menu, description, short description."""
from tg import call

CMDS = {
    "fa": ["منوی اصلی", "کاتالوگ و سفارش", "فروش ماشین در بازار", "بازار PLAYMAX", "تماس با ما", "دفتر و فابریکه", "تغییر زبان"],
    "uz": ["Bosh menyu", "Katalog va buyurtma", "Bozorda avtomat sotish", "PLAYMAX bozori", "Aloqa", "Ofis va zavodlar", "Tilni o‘zgartirish"],
    "ru": ["Главное меню", "Каталог и заказ", "Продать автомат на рынке", "Рынок PLAYMAX", "Контакты", "Офис и заводы", "Сменить язык"],
    "en": ["Main menu", "Catalog & order", "Sell a machine", "PLAYMAX Market", "Contact us", "Office & factories", "Change language"],
    "ar": ["القائمة الرئيسية", "الكتالوج والطلب", "بيع جهاز في السوق", "سوق PLAYMAX", "تواصل معنا", "المكتب والمصانع", "تغيير اللغة"],
}
KEYS = ["menu", "catalog", "sell", "market", "contacts", "places", "lang"]

DESC = {
    "fa": "PLAYMAX — تولیدکننده ماشین‌های بوکس، بازی و سرگرمی با فابریکه در تاشکند و مزارشریف.\n\n🛒 کاتالوگ و سفارش\n🏪 بازار خرید و فروش ماشین\n📞 مشاوره رایگان\n\nبه ۵ زبان: دری، ازبکی، روسی، انگلیسی، عربی",
    "uz": "PLAYMAX — boks, o‘yin va ko‘ngilochar avtomatlar ishlab chiqaruvchisi. Zavodlar: Toshkent va Mozori Sharif.\n\n🛒 Katalog va buyurtma\n🏪 Avtomatlar oldi-sotdi bozori\n📞 Bepul maslahat\n\n5 tilda: dari, o‘zbek, rus, ingliz, arab",
    "ru": "PLAYMAX — производитель боксёрских, игровых и развлекательных автоматов. Заводы в Ташкенте и Мазари-Шарифе.\n\n🛒 Каталог и заказ\n🏪 Рынок купли-продажи автоматов\n📞 Бесплатная консультация\n\n5 языков: дари, узбекский, русский, английский, арабский",
    "en": "PLAYMAX — maker of boxing, arcade and entertainment machines. Factories in Tashkent and Mazar-i-Sharif.\n\n🛒 Catalog & orders\n🏪 Machine buy & sell market\n📞 Free consultation\n\n5 languages: Dari, Uzbek, Russian, English, Arabic",
    "ar": "PLAYMAX — مصنّع أجهزة الملاكمة والألعاب والترفيه. مصانعنا في طشقند ومزار الشريف.\n\n🛒 الكتالوج والطلب\n🏪 سوق بيع وشراء الأجهزة\n📞 استشارة مجانية\n\nبخمس لغات: الدرية، الأوزبكية، الروسية، الإنجليزية، العربية",
}
SHORT = {
    "fa": "ماشین‌های بوکس و بازی PLAYMAX — کاتالوگ، بازار و مشاوره به ۵ زبان",
    "uz": "PLAYMAX boks va o‘yin avtomatlari — katalog, bozor va maslahat 5 tilda",
    "ru": "Автоматы PLAYMAX — каталог, рынок и консультации на 5 языках",
    "en": "PLAYMAX boxing & arcade machines — catalog, market and advice in 5 languages",
    "ar": "أجهزة PLAYMAX للملاكمة والألعاب — كتالوج وسوق واستشارة بخمس لغات",
}
TG_CODES = {"fa": ["fa"], "uz": ["uz"], "ru": ["ru", "uk", "kk"], "en": [None, "en"], "ar": ["ar"]}


def run():
    for lang, codes in TG_CODES.items():
        cmds = [{"command": k, "description": d} for k, d in zip(KEYS, CMDS[lang])]
        for code in codes:
            call("setMyCommands", commands=cmds, language_code=code)
            call("setMyDescription", description=DESC[lang], language_code=code)
            call("setMyShortDescription", short_description=SHORT[lang], language_code=code)


if __name__ == "__main__":
    run()
