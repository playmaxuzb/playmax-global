"""All bot interface texts in 5 languages: Dari, Uzbek, Russian, English, Arabic."""
from config import PHONES_UZ, PHONE_AF, LINKS

P1, P2 = PHONES_UZ

T = {
"choose": "🌐 زبان را انتخاب کنید\n🌐 Tilni tanlang\n🌐 Выберите язык\n🌐 Choose your language\n🌐 اختر اللغة",

"welcome": {
"fa": "به <b>PLAYMAX</b> خوش آمدید 🥊\n\nما ماشین‌های بوکس، بازی و سرگرمی را خودمان تولید می‌کنیم — فابریکه در تاشکند و مزارشریف.\n\nاز منوی پایین یکی را انتخاب کنید 👇",
"uz": "<b>PLAYMAX</b>'ga xush kelibsiz 🥊\n\nBoks, o‘yin va ko‘ngilochar avtomatlarni o‘zimiz ishlab chiqaramiz — zavodlarimiz Toshkent va Mozori Sharifda.\n\nQuyidagi menyudan tanlang 👇",
"ru": "Добро пожаловать в <b>PLAYMAX</b> 🥊\n\nМы сами производим боксёрские, игровые и развлекательные автоматы — заводы в Ташкенте и Мазари-Шарифе.\n\nВыберите раздел ниже 👇",
"en": "Welcome to <b>PLAYMAX</b> 🥊\n\nWe build our own boxing, arcade and entertainment machines — factories in Tashkent and Mazar-i-Sharif.\n\nPick a section below 👇",
"ar": "أهلاً بك في <b>PLAYMAX</b> 🥊\n\nنصنع بأنفسنا أجهزة الملاكمة والألعاب والترفيه — مصانعنا في طشقند ومزار الشريف.\n\nاختر من القائمة بالأسفل 👇",
},

"b_catalog": {"fa": "🛒 کاتالوگ و سفارش", "uz": "🛒 Katalog va buyurtma", "ru": "🛒 Каталог и заказ", "en": "🛒 Catalog & order", "ar": "🛒 الكتالوج والطلب"},
"b_contacts": {"fa": "📞 تماس با ما", "uz": "📞 Aloqa", "ru": "📞 Контакты", "en": "📞 Contact us", "ar": "📞 تواصل معنا"},
"b_places": {"fa": "📍 دفتر و فابریکه", "uz": "📍 Ofis va zavodlar", "ru": "📍 Офис и заводы", "en": "📍 Office & factories", "ar": "📍 المكتب والمصانع"},
"b_channels": {"fa": "📢 کانال‌های ما", "uz": "📢 Kanallarimiz", "ru": "📢 Наши каналы", "en": "📢 Our channels", "ar": "📢 قنواتنا"},
"b_social": {"fa": "🌐 سایت و اینستاگرام", "uz": "🌐 Sayt va Instagram", "ru": "🌐 Сайт и Instagram", "en": "🌐 Website & Instagram", "ar": "🌐 الموقع وإنستغرام"},
"b_consult": {"fa": "💬 مشاوره رایگان", "uz": "💬 Bepul maslahat", "ru": "💬 Бесплатная консультация", "en": "💬 Free consultation", "ar": "💬 استشارة مجانية"},
"b_lang": {"fa": "🌐 تغییر زبان", "uz": "🌐 Tilni o‘zgartirish", "ru": "🌐 Сменить язык", "en": "🌐 Change language", "ar": "🌐 تغيير اللغة"},
"b_back": {"fa": "⬅️ منوی اصلی", "uz": "⬅️ Bosh menyu", "ru": "⬅️ Главное меню", "en": "⬅️ Main menu", "ar": "⬅️ القائمة الرئيسية"},
"b_site": {"fa": "🌐 سایت PLAYMAX", "uz": "🌐 PLAYMAX sayti", "ru": "🌐 Сайт PLAYMAX", "en": "🌐 PLAYMAX website", "ar": "🌐 موقع PLAYMAX"},
"b_office": {"fa": "🏢 دفتر تاشکند — نقشه", "uz": "🏢 Toshkent ofisi — xarita", "ru": "🏢 Офис в Ташкенте — карта", "en": "🏢 Tashkent office — map", "ar": "🏢 مكتب طشقند — الخريطة"},
"b_factory": {"fa": "🏭 فابریکه تاشکند — نقشه", "uz": "🏭 Toshkent zavodi — xarita", "ru": "🏭 Завод в Ташкенте — карта", "en": "🏭 Tashkent factory — map", "ar": "🏭 مصنع طشقند — الخريطة"},
"b_ch_global": {"fa": "📢 PLAYMAX Global (این کانال)", "uz": "📢 PLAYMAX Global", "ru": "📢 PLAYMAX Global", "en": "📢 PLAYMAX Global", "ar": "📢 PLAYMAX Global"},
"b_ch_uz": {"fa": "🇺🇿 کانال ازبکستان", "uz": "🇺🇿 O‘zbekiston kanali", "ru": "🇺🇿 Канал Узбекистан", "en": "🇺🇿 Uzbekistan channel", "ar": "🇺🇿 قناة أوزبكستان"},
"b_wa": {"fa": "💬 واتس‌اپ افغانستان", "uz": "💬 WhatsApp (Afg‘oniston)", "ru": "💬 WhatsApp (Афганистан)", "en": "💬 WhatsApp (Afghanistan)", "ar": "💬 واتساب (أفغانستان)"},
"b_write": {"fa": "✍️ سؤال خود را بنویسید", "uz": "✍️ Savolingizni yozing", "ru": "✍️ Написать вопрос", "en": "✍️ Write your question", "ar": "✍️ اكتب سؤالك"},
"write_now": {"fa": "✍️ سؤال یا درخواست خود را همین‌جا بنویسید (متن، عکس یا پیام صوتی). تیم PLAYMAX مستقیم جواب می‌دهد.", "uz": "✍️ Savol yoki so‘rovingizni shu yerga yozing (matn, rasm yoki ovozli xabar). PLAYMAX jamoasi shaxsan javob beradi.", "ru": "✍️ Напишите вопрос или заявку прямо здесь (текст, фото или голосовое). Команда PLAYMAX ответит лично.", "en": "✍️ Type your question or request right here (text, photo or voice). The PLAYMAX team will reply personally.", "ar": "✍️ اكتب سؤالك أو طلبك هنا مباشرة (نص أو صورة أو رسالة صوتية)، وفريق PLAYMAX بيرد عليك شخصياً."},
"received": {"fa": "✅ پیام شما به تیم PLAYMAX رسید. به‌زودی همین‌جا جواب می‌گیرید.", "uz": "✅ Xabaringiz PLAYMAX jamoasiga yetib bordi. Tez orada shu yerda javob olasiz.", "ru": "✅ Ваше сообщение получено командой PLAYMAX. Ответ придёт сюда в ближайшее время.", "en": "✅ Your message reached the PLAYMAX team. You'll get a reply here shortly.", "ar": "✅ وصلت رسالتك لفريق PLAYMAX، وبيوصلك الرد هون قريباً."},
"team_reply": {"fa": "💬 <b>PLAYMAX</b>", "uz": "💬 <b>PLAYMAX</b>", "ru": "💬 <b>PLAYMAX</b>", "en": "💬 <b>PLAYMAX</b>", "ar": "💬 <b>PLAYMAX</b>"},
"b_more_lang": {"fa": "🌐 زبان‌های دیگر", "uz": "🌐 Boshqa tillar", "ru": "🌐 Другие языки", "en": "🌐 Other languages", "ar": "🌐 لغات أخرى"},

"catalog": {
"fa": "🛒 <b>کاتالوگ کامل PLAYMAX</b>\n\nماشین‌های بوکس، ماشین‌های جایزه (چنگک)، میز هاکی و فوتبال دستی، صندلی ماساژ، ماشین‌های فروش خودکار، VR و پارک بازی کودکان.\n\nدر سایت: مدل را ببینید، رنگ را انتخاب کنید و سفارش بدهید 👇",
"uz": "🛒 <b>PLAYMAX to‘liq katalogi</b>\n\nBoks avtomatlari, sovg‘a avtomatlari, xokkey va futbol stollari, massaj kreslolari, vending avtomatlar, VR va bolalar maydonchalari.\n\nSaytda modelni ko‘ring, rangini tanlang va buyurtma bering 👇",
"ru": "🛒 <b>Полный каталог PLAYMAX</b>\n\nБоксёрские автоматы, призовые автоматы с клешнёй, аэрохоккей и настольный футбол, массажные кресла, вендинг, VR и детские площадки.\n\nНа сайте: смотрите модель, выбирайте цвет и оформляйте заказ 👇",
"en": "🛒 <b>Full PLAYMAX catalog</b>\n\nBoxing machines, prize claw machines, air hockey and table football, massage chairs, vending machines, VR and kids' playgrounds.\n\nOn the website: view the model, pick a colour and order 👇",
"ar": "🛒 <b>كتالوج PLAYMAX الكامل</b>\n\nأجهزة الملاكمة، أجهزة الجوائز (الكلّاب)، طاولات الهوكي وكرة القدم، كراسي المساج، أجهزة البيع الذاتي، VR وملاعب الأطفال.\n\nعلى الموقع: شاهد الموديل، اختر اللون واطلب 👇",
},

"contacts": {
"fa": f"📞 <b>تماس با PLAYMAX</b>\n\n🇦🇫 افغانستان: <code>{PHONE_AF}</code> (واتس‌اپ / تلگرام)\n🇺🇿 ازبکستان: <code>{P1}</code>\n🇺🇿 ازبکستان: <code>{P2}</code>\n\n✉️ {LINKS['email']}\n🌐 {LINKS['site']}",
"uz": f"📞 <b>PLAYMAX bilan aloqa</b>\n\n🇺🇿 O‘zbekiston: <code>{P1}</code>\n🇺🇿 O‘zbekiston: <code>{P2}</code>\n🇦🇫 Afg‘oniston: <code>{PHONE_AF}</code> (WhatsApp / Telegram)\n\n✉️ {LINKS['email']}\n🌐 {LINKS['site']}",
"ru": f"📞 <b>Связь с PLAYMAX</b>\n\n🇺🇿 Узбекистан: <code>{P1}</code>\n🇺🇿 Узбекистан: <code>{P2}</code>\n🇦🇫 Афганистан: <code>{PHONE_AF}</code> (WhatsApp / Telegram)\n\n✉️ {LINKS['email']}\n🌐 {LINKS['site']}",
"en": f"📞 <b>Contact PLAYMAX</b>\n\n🇺🇿 Uzbekistan: <code>{P1}</code>\n🇺🇿 Uzbekistan: <code>{P2}</code>\n🇦🇫 Afghanistan: <code>{PHONE_AF}</code> (WhatsApp / Telegram)\n\n✉️ {LINKS['email']}\n🌐 {LINKS['site']}",
"ar": f"📞 <b>تواصل مع PLAYMAX</b>\n\n🇺🇿 أوزبكستان: <code>{P1}</code>\n🇺🇿 أوزبكستان: <code>{P2}</code>\n🇦🇫 أفغانستان: <code>{PHONE_AF}</code> (واتساب / تليجرام)\n\n✉️ {LINKS['email']}\n🌐 {LINKS['site']}",
},

"places": {
"fa": "📍 <b>دفتر و فابریکه‌های PLAYMAX</b>\n\n🏢 <b>دفتر — تاشکند</b>\nدیدن ماشین‌ها از نزدیک، مشاوره و سفارش\n\n🏭 <b>فابریکه — تاشکند</b>\nتولید و آماده‌سازی ماشین‌ها\n\n🏭 <b>فابریکه — مزارشریف، افغانستان</b>\nتولید و تحویل برای افغانستان\n\nبرای آدرس دقیق مزارشریف زنگ بزنید: <code>" + PHONE_AF + "</code>",
"uz": "📍 <b>PLAYMAX ofisi va zavodlari</b>\n\n🏢 <b>Ofis — Toshkent</b>\nAvtomatlarni ko‘rish, maslahat va buyurtma\n\n🏭 <b>Zavod — Toshkent</b>\nAvtomatlarni ishlab chiqarish va tayyorlash\n\n🏭 <b>Zavod — Mozori Sharif, Afg‘oniston</b>\nAfg‘oniston uchun ishlab chiqarish va yetkazish",
"ru": "📍 <b>Офис и заводы PLAYMAX</b>\n\n🏢 <b>Офис — Ташкент</b>\nПосмотреть автоматы вживую, консультация и заказ\n\n🏭 <b>Завод — Ташкент</b>\nПроизводство и подготовка автоматов\n\n🏭 <b>Завод — Мазари-Шариф, Афганистан</b>\nПроизводство и доставка по Афганистану",
"en": "📍 <b>PLAYMAX office & factories</b>\n\n🏢 <b>Office — Tashkent</b>\nSee the machines in person, get advice and order\n\n🏭 <b>Factory — Tashkent</b>\nManufacturing and preparing the machines\n\n🏭 <b>Factory — Mazar-i-Sharif, Afghanistan</b>\nProduction and delivery across Afghanistan",
"ar": "📍 <b>مكتب ومصانع PLAYMAX</b>\n\n🏢 <b>المكتب — طشقند</b>\nمعاينة الأجهزة، استشارة وطلب\n\n🏭 <b>المصنع — طشقند</b>\nتصنيع وتجهيز الأجهزة\n\n🏭 <b>المصنع — مزار الشريف، أفغانستان</b>\nتصنيع وتوصيل داخل أفغانستان",
},
"office_pin": {"fa": "دفتر PLAYMAX — تاشکند", "uz": "PLAYMAX ofisi — Toshkent", "ru": "Офис PLAYMAX — Ташкент", "en": "PLAYMAX Office — Tashkent", "ar": "مكتب PLAYMAX — طشقند"},
"factory_pin": {"fa": "فابریکه PLAYMAX — تاشکند", "uz": "PLAYMAX zavodi — Toshkent", "ru": "Завод PLAYMAX — Ташкент", "en": "PLAYMAX Factory — Tashkent", "ar": "مصنع PLAYMAX — طشقند"},

"channels": {
"fa": "📢 <b>کانال‌های تلگرام PLAYMAX</b>\n\n• PLAYMAX Global — به ۵ زبان، برای همه کشورها\n• PLAYMAX Uzbekistan — مخصوص ازبکستان، به زبان ازبکی",
"uz": "📢 <b>PLAYMAX Telegram kanallari</b>\n\n• PLAYMAX Global — 5 tilda, barcha davlatlar uchun\n• PLAYMAX Uzbekistan — O‘zbekiston uchun, o‘zbek tilida",
"ru": "📢 <b>Telegram-каналы PLAYMAX</b>\n\n• PLAYMAX Global — на 5 языках, для всех стран\n• PLAYMAX Uzbekistan — для Узбекистана, на узбекском",
"en": "📢 <b>PLAYMAX Telegram channels</b>\n\n• PLAYMAX Global — 5 languages, for every country\n• PLAYMAX Uzbekistan — for Uzbekistan, in Uzbek",
"ar": "📢 <b>قنوات PLAYMAX على تليجرام</b>\n\n• PLAYMAX Global — بخمس لغات، لكل الدول\n• PLAYMAX Uzbekistan — خاصة بأوزبكستان، باللغة الأوزبكية",
},

"social": {
"fa": "🌐 <b>سایت و شبکه‌های PLAYMAX</b>\n\nسایت رسمی: کاتالوگ کامل، رنگ‌ها و سفارش آنلاین.\nاینستاگرام: ویدیوهای تازه و ماشین‌های جدید 👇",
"uz": "🌐 <b>PLAYMAX sayti va tarmoqlari</b>\n\nRasmiy sayt: to‘liq katalog, ranglar va onlayn buyurtma.\nInstagram: yangi videolar va yangi avtomatlar 👇",
"ru": "🌐 <b>Сайт и соцсети PLAYMAX</b>\n\nОфициальный сайт: полный каталог, цвета и онлайн-заказ.\nInstagram: свежие видео и новые автоматы 👇",
"en": "🌐 <b>PLAYMAX website & socials</b>\n\nOfficial website: full catalog, colours and online ordering.\nInstagram: fresh videos and new machines 👇",
"ar": "🌐 <b>موقع PLAYMAX وحساباتنا</b>\n\nالموقع الرسمي: الكتالوج الكامل والألوان والطلب أونلاين.\nإنستغرام: فيديوهات وأجهزة جديدة أولاً بأول 👇",
},

"consult": {
"fa": f"💬 <b>مشاوره رایگان</b>\n\nبگویید کجا می‌خواهید ماشین بگذارید (مول، کافه، پارک، باشگاه...) — ما بهترین مدل و جای مناسب را پیشنهاد می‌کنیم.\n\n📞 <code>{PHONE_AF}</code>\n📞 <code>{P1}</code>\n📞 <code>{P2}</code>",
"uz": f"💬 <b>Bepul maslahat</b>\n\nAvtomatni qayerga qo‘ymoqchisiz (savdo markazi, kafe, park, sport zal...) — eng mos modelni va joyni tavsiya qilamiz.\n\n📞 <code>{P1}</code>\n📞 <code>{P2}</code>\n📞 <code>{PHONE_AF}</code>",
"ru": f"💬 <b>Бесплатная консультация</b>\n\nРасскажите, где хотите поставить автомат (ТЦ, кафе, парк, спортзал...) — подберём лучшую модель и место.\n\n📞 <code>{P1}</code>\n📞 <code>{P2}</code>\n📞 <code>{PHONE_AF}</code>",
"en": f"💬 <b>Free consultation</b>\n\nTell us where you want to place a machine (mall, café, park, gym...) — we'll suggest the best model and spot.\n\n📞 <code>{P1}</code>\n📞 <code>{P2}</code>\n📞 <code>{PHONE_AF}</code>",
"ar": f"💬 <b>استشارة مجانية</b>\n\nأخبرنا أين تريد وضع الجهاز (مول، كافيه، حديقة، نادي...) — ونقترح لك أفضل موديل وأفضل مكان.\n\n📞 <code>{P1}</code>\n📞 <code>{P2}</code>\n📞 <code>{PHONE_AF}</code>",
},

"not_found": {"fa": "این پست پیدا نشد. منوی اصلی 👇", "uz": "Post topilmadi. Bosh menyu 👇", "ru": "Пост не найден. Главное меню 👇", "en": "Post not found. Main menu 👇", "ar": "لم يتم العثور على المنشور. القائمة الرئيسية 👇"},
"fallback": {"fa": "از منوی پایین انتخاب کنید یا مستقیم زنگ بزنید 👇", "uz": "Menyudan tanlang yoki to‘g‘ridan-to‘g‘ri qo‘ng‘iroq qiling 👇", "ru": "Выберите в меню или позвоните нам напрямую 👇", "en": "Pick from the menu or call us directly 👇", "ar": "اختر من القائمة أو اتصل بنا مباشرة 👇"},

# Channel post footer (short, fits under captions)
"footer": {
"fa": f"\n\n📞 {PHONE_AF} | {P2}\n🌐 playmaxuz.com",
"uz": f"\n\n📞 {P1} | {P2}\n🌐 playmaxuz.com",
"ru": f"\n\n📞 {P1} | {PHONE_AF}\n🌐 playmaxuz.com",
"en": f"\n\n📞 {P2} | {PHONE_AF}\n🌐 playmaxuz.com",
"ar": f"\n\n📞 {P2} | {PHONE_AF}\n🌐 playmaxuz.com",
},
"b_read": {"fa": "🇦🇫 دری", "uz": "🇺🇿 UZ", "ru": "🇷🇺 RU", "en": "🇬🇧 EN", "ar": "🇸🇦 AR"},
"b_order_short": {"fa": "🛒 سفارش", "uz": "🛒 Buyurtma", "ru": "🛒 Заказать", "en": "🛒 Order", "ar": "🛒 اطلب"},
"b_ask": {"fa": "💬 مشاوره", "uz": "💬 Maslahat", "ru": "💬 Консультация", "en": "💬 Ask us", "ar": "💬 استشارة"},
}


def t(key, lang):
    v = T[key]
    if isinstance(v, str):
        return v
    return v.get(lang) or v["en"]
