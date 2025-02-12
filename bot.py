from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from dotenv import load_dotenv
from telegram.error import Conflict
import time
import os

COMMANDS = [
    ("start", "Почати роботу з ботом"),
    ("clear", "Очистити чат"),
    ("restart", "Перезапустити бота"),
    ("stop", "Зупинити бота")
]

# Завантаження змінних з .env файлу
load_dotenv()

# Отримання токену
TOKEN = os.getenv('TELEGRAM_TOKEN')



# Структура даних для меню
MENU_DATA = {

# ЩО РОБИТИ ЯКЩО
    "what_to_do": {
    "title": "❓ ЩО РОБИТИ ЯКЩО ❓",
    "content": "Оберіть, хто ви за роллю:",
    "submenu": {
        "student": {
            "title": "👨‍🎓 я — учень/учениця",
            "description": """<b>Якщо ви стали жертвою або свідком булінгу:</b>

1. Не мовчіть! Булінг не припиниться самостійно.

2. Розкажіть про ситуацію дорослим, яким довіряєте:
   • батькам
   • класному керівнику
   • шкільному психологу
   • соціальному педагогу

3. Зберігайте докази булінгу:
   • повідомлення
   • скріншоти
   • записи розмов
   • фотографії

4. Уникайте місць, де можливі випадки булінгу

5. Тримайтеся ближче до друзів, які можуть захистити

6. Зверніться на гарячу лінію з протидії булінгу:
   • 116 000
   • 0 800 500 225"""
        },
        "class_teacher": {
            "title": "👩‍🏫 я — класний керівник",
            "description": """<b>Алгоритм дій класного керівника:</b>

1. При виявленні булінгу негайно повідомте:
   • керівництво закладу освіти
   • психологічну службу
   • батьків усіх сторін булінгу

2. Зафіксуйте випадок:
   • опишіть ситуацію письмово
   • запишіть пояснення сторін
   • зберіть докази (за наявності)

3. Проведіть розмови:
   • з жертвою булінгу
   • з булером
   • зі свідками
   • з класом загалом

4. Складіть план заходів протидії булінгу в класі

5. Моніторте ситуацію після вжитих заходів

6. Проводьте профілактичні заходи щодо булінгу"""
        },
        "subject_teacher": {
            "title": "👨‍🏫 я — вчитель-предметник",
            "description": """<b>Алгоритм дій вчителя-предметника:</b>

1. При виявленні булінгу:
   • припиніть будь-які прояви булінгу
   • повідомте класного керівника
   • повідомте адміністрацію закладу

2. Зафіксуйте інцидент:
   • запишіть, що сталося
   • вкажіть час і місце
   • занотуйте учасників і свідків

3. За необхідності:
   • надайте першу допомогу
   • викличте медичного працівника

4. Підготуйте службову записку про інцидент

5. Відслідковуйте поведінку учасників на ваших уроках

6. Підтримуйте безпечну атмосферу на уроках"""
        },
        "principal": {
            "title": "👨‍💼 я — керівник закладу",
            "description": """<b>Алгоритм дій керівника закладу освіти:</b>

1. При отриманні заяви про булінг:
   • видайте наказ про проведення розслідування
   • створіть комісію з розгляду випадку
   • повідомте уповноважені органи (поліцію, службу у справах дітей)

2. Забезпечте:
   • припинення булінгу
   • надання допомоги постраждалому
   • роботу психолога з усіма сторонами

3. Контролюйте:
   • проведення розслідування
   • вжиття заходів протидії
   • надання допомоги сторонам

4. Затвердіть:
   • план заходів протидії булінгу
   • програму профілактики

5. Проведіть засідання педради щодо ситуації

6. Забезпечте виконання рішень комісії"""
        },
        "parents": {
            "title": "👨‍👩‍👧‍👦 я — батько/мати",
            "description": """<b>Якщо ваша дитина стала жертвою булінгу:</b>

1. Збережіть спокій та підтримайте дитину:
   • вислухайте її
   • запевніть у своїй підтримці
   • поясніть, що вона не винна

2. Зберіть докази:
   • зробіть фото ушкоджень
   • збережіть листування
   • запишіть розповідь дитини

3. Зверніться до школи:
   • напишіть заяву директору
   • зустріньтеся з класним керівником
   • поговоріть зі шкільним психологом

4. За потреби:
   • зверніться до поліції
   • напишіть заяву до служби у справах дітей
   • зверніться до юриста

5. Забезпечте психологічну підтримку дитині

6. Тримайте зв'язок зі школою до вирішення ситуації"""
        }
    }
},

# ТЕЛЕФОНИ ДОВІРИ
    "calling": {
    "title": "📞 ТЕЛЕФОНИ ДОВІРИ 📞",
    "content": """<b>Телефони гарячих ліній:</b>

- Національна дитяча «гаряча лінія»:
  ‣ <b>0 800 500 225</b>
  ‣ <b>116 111</b>

- Кол-центри Міністерства соціальної політики:
  -- з питань протидії торгівлі людьми: <b>1578</b>
  -- з питань протидії насильству: <b>1588</b>

- Національна безкоштовна гаряча лінія з протидії торгівлі людьми
  ‣ <b>0 800 505 501</b>
  ‣ <b>527</b>

- Урядова гаряча лінія з попередження домашнього насильства:
  ‣ <b>1547</b>

- Гаряча телефонна лінія щодо булінгу:
  ‣ <b>116 000</b>

- Гаряча лінія з протидії насильству
  ‣ <b>0 800 500 335</b>
  ‣ <b>116 123</b>

- Гаряча лінія Уповноваженого ВРУ з прав людини
  ‣ <b>0 800 501 720</b>

- Уповноважений Президента України з прав дитини
  ‣ <b>044 255 76 75</b>"""
},

# НОРМАТИВНА БАЗА
    "normative": {
        "title": "📚 НОРМАТИВНА БАЗА 📚",
        "content": """Офіційні документи МОН щодо булінгу:

• [Нормативна база МОН](https://mon.gov.ua/ua/tag/buling)
• [Протоколи реагування](https://link-to-protocols)""",
        "url": "https://mon.gov.ua/ua/tag/buling"
    },

# ПОСІБНИКИ
    "manuals": {
        "title": "📖 ПОСІБНИКИ 📖",
        "content": """Корисні матеріали та посібники:

• [Протидія булінгу в закладі освіти: системний підхід](https://mon.gov.ua/static-objects/mon/sites/1/zagalna%20serednya/protidia-bulingu/2019-11-25-protydiy-bullingy.pdf)
• [Посібник 2](https://link2)""",
    },

# ГОТОВІ ЗАНЯТТЯ
    "lessons": {
        "title": "🎓 ГОТОВІ ЗАНЯТТЯ 🎓",
        "submenu": {
            "age_groups": "За віком",
            "duration": "За тривалістю",
            "target_group": "За цільовою групою"
        }
    },

# КОРОБКА З МАТЕРІАЛАМИ
    "training": {
    "title": "📦 КОРОБКА З МАТЕРІАЛАМИ 📦",
    "submenu": {
        "exercises": {
            "title": "🎯 вправи"
        },
        "all_education": {
            "title": "🎓 анкети"
        },
        "educational_hours": {
            "title": "⏰ виховні години"
        },
        "info_materials": {
            "title": "📚 інформаційні матеріали"
        },
        "psychological_hours": {
            "title": "🧠 психологічні години"
        },
        "training_sessions": {
            "title": "✨ заняття-тренінги"
        },
        "quests": {
            "title": "🎲 квести"
        },
        "summaries": {
            "title": "📝 конспекти"
        },
        "situation_sets": {
            "title": "🎭 набори ситуацій"
        },
        "trainings": {
            "title": "👥 тренінги"
        }
    }
},

# КОРИСНЕ З ДІЇ
    "diia_edu": {
    "title": "📱 КОРИСНЕ з ДІЯ.ОСВІТА 📱",
    "content": "Оберіть курс:",
    "submenu": {
        
        "personal_safety": {
            "title": "Особиста безпека підлітків",
            "description": """<b>"Особиста безпека підлітків"</b>

<i>Експерти: <b>Саша Гонтар</b></i>

Булінг, кібербулінг, залякування, погрози, кіберпереслідування, насильство в житті та мережі — чому це все не ок і що із цим робити?

У серіалі «Особиста безпека підлітків» ми розглянемо ключові ризики, які можуть трапитися з підлітками в реальному житті та мережі, а також розповімо, які життєві навички можливо прокачати, щоб протидіяти їм.

Освітній серіал створено з ініціативи Мінцифри для платформи Дія.Освіта за підтримки благодійного фонду «Клуб Добродіїв» та міжнародної гуманітарної організації Plan International.

Серіал про те, як захистити себе від ризиків у житті та мережі й прокачати життєві навички для протидії викликам.""",
            "url": "https://osvita.diia.gov.ua/courses/teenagers-personal-safety"
        },
        
        "school_no_bullying_teacher": {
            "title": "Школа без цькувань. Учителю",
            "description": """<b>"Школа без цькувань. Учителю"</b>

<i>Експерти: <b>Настя Мельниченко, Юлія Завгородня</b></i>

Цькування серед дітей — проблема як вчителів, так і батьків. Цей освітній серіал дасть вам дієві поради та методи, як боротися з булінгом, в тому числі в роботі з дітьми з емоційно-поведінковими особливостями.

Програма розроблена і для батьків, і для вчителів, щоб наочно пояснити, як говорити на цю тему з молодшими, як протидіяти цькуванню і, зрештою, як зробити так, щоб проблема булінгу лишилася в минулому.

Курс розроблено ГО «Студена» за ініціативи Міністерства цифрової трансформації України для платформи Дія.Освіта, за підтримки Міністерства науки та освіти України та проєкту «Дружній простір».

Серіал про те, як запобігти цькуванню: поради та стратегії для вчителів.""",
            "url": "https://osvita.diia.gov.ua/courses/skola-bez-ckuvan-castina-1-ucitelu"
        },
        
        "school_no_bullying_parents": {
            "title": "Школа без цькувань. Батькам",
            "description": """<b>"Школа без цькувань. Батькам"</b>

<i>Експерти: <b>Настя Мельниченко, Юлія Завгородня</b></i>

Цькування — спільна проблема вчителів, батьків та дітей. Цей освітній серіал дасть вам дієві поради та методи, як боротися з булінгом, в тому числі в роботі з дітьми з емоційно-поведінковими особливостями.

Програма розроблена і для батьків, і для вчителів, щоб наочно пояснити, як говорити на цю тему з молодшими, як протидіяти цькуванню і, зрештою, як зробити так, щоб проблема булінгу лишилася в минулому.

Курс розроблено ГО «Студена» за ініціативи Міністерства цифрової трансформації України для платформи Дія.Освіта, за підтримки Міністерства науки та освіти України та проєкту «Дружній простір».

Сераіал про те, як запобігти цькуванню: поради та стратегії для батьків.""",
            "url": "https://osvita.diia.gov.ua/courses/skola-bez-ckuvan-castina-2-batkam"
        },
        
        "cyberbullying": {
            "title": "Про кібербулінг для підлітків",
            "description": """<b>"Про кібербулінг для підлітків"</b>

<i>Експерти: <b>Анна Трінчер, Настя Каменських</b></i>

У справжній дружбі немає місця приниженням та неповазі, особливо онлайн. Якщо тебе образив коментар, повідомлення чи будь-що інше в мережі — це може бути кібербулінг. Не терпи це, це не окей.

Щоб не помилитися, переглянь освітній серіал. Тут можна зрозуміти, як виглядає кібербулінг, які його причини та потенційні наслідки, та як припинити булінг в інтернеті.

Якщо від цькувань в інтернеті страждають твої друзі — окрема серія буде присвячена тому, як їм допомогти. Не дозволяй кривдникам тебе образити! Проєкт Міністерства цифрової трансформації України за підтримки ЮНІСЕФ в Україні.

Серіал про те, як протистояти буллінгу в інтернеті.""",
            "url": "https://osvita.diia.gov.ua/courses/cyberbullying"
        }
    }
},

# ГО ТРИКУТНИК
    "triangle": {
    "title": "🔺 ГО «ТРИКУТНИК» 🔺",
    "content": """ <b>"Трикутник" - платформа співдії освіти, культури та правозахисту.</b>

Контакти:
- <a href="tel:+380990889198">0990889198</a>
- trykutnyk.fest@gmail.com

Адреса:
- вул. Братів Білоусів 11, приміщення 12, Коломия, Україна""",
    
    "links": {
        "telegram": "https://t.me/ngo_trykutnyk",
        "facebook": "https://www.facebook.com/trykutnyk",
        "instagram": "https://www.instagram.com/triangle_ngo",
        "vulyk": "https://www.instagram.com/vulykzmistiv",
        "youth_space": "https://www.instagram.com/molod.prostir.klm"
    }
}
    
}

# Структура для підменю тренінгів
TRAINING_SUBMENUS = {
    "submenu_type": {
        "title": "Категорії матеріалів",
        "options": {
            "exercises": "📍 вправи",
            "all_education": "📍 всеобучі",
            "educational_hours": "📍 виховні години",
            "info_materials": "📍 інформаційні матеріали",
            "psychological_hours": "📍 психологічні години",
            "training_sessions": "📍 заняття-тренінги",
            "quests": "📍 квести",
            "summaries": "📍 конспекти",
            "situation_sets": "📍 набори ситуацій",
            "trainings": "📍 тренінги"
        }
    }
}

# Структура для підменю занять
LESSONS_SUBMENUS = {
    "age_groups": {
        "title": "Заняття за віком",
        "options": {
            "primary": "Початкова школа",
            "middle": "Середня школа",
            "high": "Старша школа"
        }
    },
    "duration": {
        "title": "Заняття за тривалістю",
        "options": {
            "short": "15-30 хвилин",
            "medium": "30-45 хвилин",
            "long": "45-60 хвилин"
        }
    },
    "target_group": {
        "title": "За цільовою групою",
        "options": {
            "students": "Для учнів",
            "teachers": "Для вчителів",
            "parents": "Для батьків"
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показує головне меню"""
    keyboard = [
        [InlineKeyboardButton(MENU_DATA["what_to_do"]["title"], callback_data="what_to_do")],
        [InlineKeyboardButton(MENU_DATA["calling"]["title"], callback_data="calling")],
        [InlineKeyboardButton(MENU_DATA["normative"]["title"], callback_data="normative")],
        [InlineKeyboardButton(MENU_DATA["manuals"]["title"], callback_data="manuals")],
        [InlineKeyboardButton(MENU_DATA["lessons"]["title"], callback_data="lessons")],
        [InlineKeyboardButton(MENU_DATA["training"]["title"], callback_data="training")],
        [InlineKeyboardButton(MENU_DATA["diia_edu"]["title"], callback_data="diia_edu")],
        [InlineKeyboardButton(MENU_DATA["triangle"]["title"], callback_data="triangle")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привіт! Я твій бот-помічник у питаннях булінгу. Тут Ти зможеш знайти все необхідне. Обери розділ:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    print(f"Received callback_data: {query.data}")

    if query.data == "diia_edu":
        return await show_diia_edu_menu(update, context)
        
    # Обробка вибору конкретного курсу
    if query.data.startswith("diia_edu_"):
        course_key = query.data.replace("diia_edu_", "")
        course = MENU_DATA["diia_edu"]["submenu"].get(course_key)
        
        if course:
            keyboard = [
                [InlineKeyboardButton("📱 Перейти до курсу", url=course["url"])],
                [InlineKeyboardButton("◀️ Назад до списку курсів", callback_data="diia_edu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=course["description"],
                reply_markup=reply_markup,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            return

    if query.data == "triangle":
        keyboard = [
            [
                InlineKeyboardButton("📱 Telegram", url=MENU_DATA["triangle"]["links"]["telegram"]),
                InlineKeyboardButton("📘 Facebook", url=MENU_DATA["triangle"]["links"]["facebook"]),
                InlineKeyboardButton("📸 Instagram", url=MENU_DATA["triangle"]["links"]["instagram"])
            ],
            [
                InlineKeyboardButton("🎯 Вулик Змістів", url=MENU_DATA["triangle"]["links"]["vulyk"]),
                InlineKeyboardButton("🌟 Молодіжний простір Коломиї", url=MENU_DATA["triangle"]["links"]["youth_space"])
            ],
            [InlineKeyboardButton("◀️ Назад до меню", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        full_text = f"""{MENU_DATA["triangle"]["content"]}

<b>Приєднуйтеся до нашої спільноти або до спільнот наших ініціатив:</b>"""
        
        try:
            await query.edit_message_text(
                text=full_text,
                reply_markup=reply_markup,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
        except Exception as e:
            await query.message.reply_text(
                text=full_text,
                reply_markup=reply_markup,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
        return
        
    if query.data == "main_menu":
        return await show_main_menu(update, context)
    
    if query.data == "lessons":
        return await show_lessons_menu(update, context)
    
    if query.data == "training":
        return await show_training_menu(update, context)
    
    if query.data in LESSONS_SUBMENUS:
        return await show_submenu(update, context, query.data)
    
    if query.data in TRAINING_SUBMENUS["submenu_type"]["options"]:
        return await show_training_submenu(update, context, query.data)
    
    # Показуємо інформацію з основного меню
    menu_item = MENU_DATA.get(query.data)
    if menu_item:
        keyboard = [[InlineKeyboardButton("◀️ Назад до меню", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=menu_item.get("content", "Інформація відсутня"),
            reply_markup=reply_markup,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    # В функції handle_button додаємо:
    if query.data == "what_to_do":
        return await show_what_to_do_menu(update, context)
    
    # Обробка вибору конкретної ролі
    if query.data.startswith("what_to_do_"):
        role_key = query.data.replace("what_to_do_", "")
        role = MENU_DATA["what_to_do"]["submenu"].get(role_key)
        
        if role:
            keyboard = [
                [InlineKeyboardButton("◀️ Назад до вибору ролі", callback_data="what_to_do")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=role["description"],
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            return

async def show_what_to_do_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показує меню вибору ролі"""
    query = update.callback_query
    keyboard = []
    
    # Додаємо кнопки для кожної ролі
    for key, item in MENU_DATA["what_to_do"]["submenu"].items():
        keyboard.append([InlineKeyboardButton(item["title"], callback_data=f"what_to_do_{key}")])
    
    # Додаємо кнопку повернення до головного меню
    keyboard.append([InlineKeyboardButton("◀️ Назад до меню", callback_data="main_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="Оберіть, хто ви за роллю:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def show_training_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показує меню матеріалів"""
    query = update.callback_query
    keyboard = []
    
    # Створюємо список всіх пунктів меню
    menu_items = list(MENU_DATA["training"]["submenu"].items())
    
    # Розбиваємо на пари (по 2 кнопки в ряд)
    for i in range(0, len(menu_items), 2):
        row = []
        # Додаємо першу кнопку в ряд
        row.append(InlineKeyboardButton(
            menu_items[i][1]["title"], 
            callback_data=f"training_{menu_items[i][0]}"
        ))
        # Додаємо другу кнопку, якщо вона є
        if i + 1 < len(menu_items):
            row.append(InlineKeyboardButton(
                menu_items[i + 1][1]["title"], 
                callback_data=f"training_{menu_items[i + 1][0]}"
            ))
        keyboard.append(row)
    
    # Додаємо кнопку повернення до головного меню
    keyboard.append([InlineKeyboardButton("◀️ Назад до меню", callback_data="main_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="Оберіть розділ матеріалів:",
        reply_markup=reply_markup
    )

async def show_training_submenu(update: Update, context: ContextTypes.DEFAULT_TYPE, selected_category: str):
    """Показує підменю для обраної категорії тренінгів"""
    query = update.callback_query
    category_text = TRAINING_SUBMENUS["submenu_type"]["options"].get(selected_category, "Категорія")
    
    keyboard = [
        [InlineKeyboardButton("◀️ Назад до тренінгів", callback_data="training")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"Ви обрали категорію: {category_text}\n\nОписання та матеріали готуються...",
        reply_markup=reply_markup
    )

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показує головне меню"""
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton(MENU_DATA["what_to_do"]["title"], callback_data="what_to_do")],
        [InlineKeyboardButton(MENU_DATA["calling"]["title"], callback_data="calling")],
        [InlineKeyboardButton(MENU_DATA["normative"]["title"], callback_data="normative")],
        [InlineKeyboardButton(MENU_DATA["manuals"]["title"], callback_data="manuals")],
        [InlineKeyboardButton(MENU_DATA["lessons"]["title"], callback_data="lessons")],
        [InlineKeyboardButton(MENU_DATA["training"]["title"], callback_data="training")],
        [InlineKeyboardButton(MENU_DATA["diia_edu"]["title"], callback_data="diia_edu")],
        [InlineKeyboardButton(MENU_DATA["triangle"]["title"], callback_data="triangle")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="Оберіть розділ:",
        reply_markup=reply_markup
    )


async def show_lessons_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показує меню занять"""
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("📚 За віком", callback_data="age_groups")],
        [InlineKeyboardButton("⏱ За тривалістю", callback_data="duration")],
        [InlineKeyboardButton("👥 За цільовою групою", callback_data="target_group")],
        [InlineKeyboardButton("◀️ Назад до меню", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="Оберіть категорію занять:",
        reply_markup=reply_markup
    )

async def show_submenu(update: Update, context: ContextTypes.DEFAULT_TYPE, submenu_type: str):
    """Показує підменю для обраної категорії занять"""
    query = update.callback_query
    submenu = LESSONS_SUBMENUS[submenu_type]
    
    keyboard = [
        [InlineKeyboardButton(text, callback_data=f"{submenu_type}_{key}")]
        for key, text in submenu["options"].items()
    ]
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="lessons")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"{submenu['title']}:",
        reply_markup=reply_markup
    )

async def clear_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Очищає чат"""
    await update.message.reply_text("Чат очищено!")

async def restart_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Перезапускає бота"""
    await update.message.reply_text("Бота перезапущено!")
    await start(update, context)

async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Зупиняє бота"""
    await update.message.reply_text("Бота зупинено. Щоб почати знову, напишіть /start")

async def show_diia_edu_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показує підменю розділу ДІЯ.ОСВІТА"""
    query = update.callback_query
    keyboard = []
    
    # Додаємо кнопки для кожного курсу
    for key, item in MENU_DATA["diia_edu"]["submenu"].items():
        keyboard.append([InlineKeyboardButton(item["title"], callback_data=f"diia_edu_{key}")])
    
    # Додаємо кнопку повернення до головного меню
    keyboard.append([InlineKeyboardButton("◀️ Назад до меню", callback_data="main_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="Оберіть курс на платформі ДІЯ.ОСВІТА:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

def run_bot():
    """Запускає бота"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            application = Application.builder().token(TOKEN).build()
            
            application.add_handler(CommandHandler("start", start))
            application.add_handler(CallbackQueryHandler(handle_button))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))
            
            print("Бот запускається...")
            application.run_polling()
            break
            
        except Conflict:
            retry_count += 1
            print(f"Спроба {retry_count} з {max_retries}: Бот вже запущений. Очікування...")
            time.sleep(10)  # Чекаємо 10 секунд перед повторною спробою
            
    if retry_count == max_retries:
        print("Не вдалося запустити бота після кількох спроб. Переконайтеся, що немає інших запущених екземплярів.")

    application = Application.builder().token(TOKEN).build()
    
    # Додаємо обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear_chat))
    application.add_handler(CommandHandler("restart", restart_bot))
    application.add_handler(CommandHandler("stop", stop_bot))
    application.add_handler(CallbackQueryHandler(handle_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))
    
    # Запускаємо бота
    application.run_polling()

if __name__ == "__main__":
    run_bot()