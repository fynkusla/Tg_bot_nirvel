import logging
from telegram import (Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext)
from datetime import datetime

# Включить ведение журнала
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
PHONE, MASTER, NAME, TIME, PRODUCTS, QUESTIONS, CONFIRMATION = range(7)

# Токен вашего бота
TOKEN = ''

# Основная клавиатура
main_keyboard = ReplyKeyboardMarkup(
    [['Косметика'], ['Контакты'], ['Наше расположение'], ['Составление заявки']],
    one_time_keyboard=True
)


def facts_to_str(user_data):
    facts = [f'{key}: {value}' for key, value in user_data.items()]
    return "\n".join(facts)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        """
Рады приветствовать вас!

Здесь вы можете узнать о косметике Nirvel и оформить заказ. Nirvel Professional – испанский бренд профессиональной косметики для волос с широким ассортиментом качественных средств для парикмахеров.

Мы ценим наших клиентов и рады как новым, так и постоянным покупателям. Для мастеров предусмотрена доставка продукции по городу Самара. 

Спасибо, что выбираете Nirvel! Мы всегда на связи и готовы помочь вам!

Ваш Nirvel.
        """,
        reply_markup=main_keyboard
    )


def cosmetics(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Nirvel", url="https://nirvel.ru")],
        [InlineKeyboardButton("Актуальный прайс", url="https://vk.com/market-224297936?screen=group")],
        [InlineKeyboardButton("Академия Nirvel", url="https://academy.nirvel.ru/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        '''
        Nirvel Professional – это испанский бренд профессиональной косметики для волос. Подробную информацию о бренде можно найти на официальном сайте Nirvel.

С ассортиментом и актуальными ценами на продукцию вы можете ознакомиться в нашей группе ВКонтакте.

Для мастеров доступно обучение на профессиональной косметике Nirvel в их академии. Получите новые знания и навыки, чтобы предоставлять своим клиентам лучшие услуги.
        ''',
        reply_markup=reply_markup
    )
    update.message.reply_text("""
Спасибо, что выбираете нас!    
    """, reply_markup=main_keyboard)


def contacts(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("VK", url="https://vk.com/nirvel_samara")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        """
Для получения актуальной информации о продукции, новинках и акциях, вы можете перейти в нашу группу ВКонтакте, где мы регулярно обновляем информацию.
Если у вас возникли вопросы или вы можете связаться с нами.
        """,
        reply_markup=reply_markup
    )
    update.message.reply_text("""
Контакты менеджеров:
Менеджер Лариса
Тел: +7 (846) 203-01-90    

Наши менеджеры работают и формируют заказы по следующему графику:
Понедельник - Четверг: 10:00 - 16:00
Пятница - Воскресенье: выходной    
    """, reply_markup=main_keyboard)


def addresses(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Наш адрес", url="https://yandex.ru/maps/-/CDG9bQZr")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        '''
Для наших клиентов доступен самовывоз. 
Заказ можно забрать в рабочие часы (пн-чт: 10:00 - 16:00)
Мы работаем по адресу г. Самара, ул. Академика Павлова, д. 80
Для мастеров предлагаем доставку по городу Самара, чтобы вы могли получать свои заказы быстро и удобно.

        ''', reply_markup=reply_markup
    )
    update.message.reply_text("""
Если у вас возникли вопросы или требуется дополнительная информация, пожалуйста, свяжитесь с нами. 
Мы всегда рады помочь!    
    """, reply_markup=main_keyboard)


def application_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Пожалуйста, поделитесь своим номером телефона или нажмите "Пропустить":',
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Отправить номер телефона", request_contact=True)], ['Пропустить']],
            one_time_keyboard=True
        )
    )
    return PHONE


def phone(update: Update, context: CallbackContext) -> int:
    if update.message.contact:
        contact = update.message.contact
        context.user_data['Телефон'] = contact.phone_number
    else:
        context.user_data['Телефон'] = 'Не указан'

    update.message.reply_text(
        'Если вы являетесь мастером, пожалуйста, подтвердите это!',
        reply_markup=ReplyKeyboardMarkup(
            [['Мастер', 'Покупатель']],
            one_time_keyboard=True
        )
    )
    return MASTER


def master(update: Update, context: CallbackContext) -> int:
    context.user_data['Мастер или Покупатель'] = update.message.text

    user = update.message.from_user
    context.user_data['Имя пользователя'] = f"@{user.username}" if user.username else user.first_name
    context.user_data['Дата обращения'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update.message.reply_text('Пожалуйста, введите ваше ФИО:', reply_markup=ReplyKeyboardRemove())
    return NAME


def name(update: Update, context: CallbackContext) -> int:
    context.user_data['ФИО'] = update.message.text
    update.message.reply_text('''Пожалуйста, введите удобное время для связи с вами, наши менеджеры работают по графику 
Понедельник - Четверг: 10:00 - 16:00''')
    return TIME


def time(update: Update, context: CallbackContext) -> int:
    context.user_data['Желаемое время для связи'] = update.message.text
    update.message.reply_text('''
Введите интересующие вас продукты, с ассортиментом и актуальными ценами вы можете ознакомится в нашей группе ВК
VK: vk.com/nirvel_samara 
    ''')
    return PRODUCTS


def products(update: Update, context: CallbackContext) -> int:
    context.user_data['Интересующие продукты'] = update.message.text
    update.message.reply_text(
        'Если у вас остались какие-то вопросы - напишите их здесь и наш менеджер вас проконсультирует!')
    return QUESTIONS


def questions(update: Update, context: CallbackContext) -> int:
    context.user_data['Возможные вопросы'] = update.message.text
    reply_keyboard = [['Подтвердить', 'Отменить']]
    update.message.reply_text(
        f"Пожалуйста, проверьте введённую информацию:\n{facts_to_str(context.user_data)}",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CONFIRMATION


def confirmation(update: Update, context: CallbackContext) -> int:
    if update.message.text == 'Подтвердить':
        # Отправка сообщения менеджеру
        manager_chat_id = ''
        context.bot.send_message(chat_id=manager_chat_id, text=f"Новая заявка:\n{facts_to_str(context.user_data)}")
        update.message.reply_text(
            'Спасибо! Ваша заявка отправлена менеджеру. Мы постараемся связаться с вами как можно скорее!',
            reply_markup=main_keyboard)
        return ConversationHandler.END
    else:
        update.message.reply_text('Заявка отменена.', reply_markup=main_keyboard)
        return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Заявка отменена.', reply_markup=main_keyboard)
    return ConversationHandler.END


def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.regex('Косметика'), cosmetics))
    dispatcher.add_handler(MessageHandler(Filters.regex('Контакты'), contacts))
    dispatcher.add_handler(MessageHandler(Filters.regex('Наше расположение'), addresses))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Составление заявки'), application_start)],
        states={
            PHONE: [MessageHandler(Filters.contact, phone), MessageHandler(Filters.regex('Пропустить'), phone)],
            MASTER: [MessageHandler(Filters.regex('^(Мастер|Покупатель)$'), master)],
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            TIME: [MessageHandler(Filters.text & ~Filters.command, time)],
            PRODUCTS: [MessageHandler(Filters.text & ~Filters.command, products)],
            QUESTIONS: [MessageHandler(Filters.text & ~Filters.command, questions)],
            CONFIRMATION: [MessageHandler(Filters.regex('^(Подтвердить|Отменить)$'), confirmation)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
