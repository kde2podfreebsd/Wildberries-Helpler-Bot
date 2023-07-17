import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold, hlink

from data.config import BOT_NAME, SUPPORT_LINK
from keyboards.inline.start_keyboard.connection import connection_keyboard, back_to_connection
from loader import dp, bot
from states.states import States
from utils.db_api.quick_commands.seller_inquiries import select_seller_by_api_x64, add_seller, check_free_trail, \
    append_free_trail, update_trail_fail
from utils.db_api.quick_commands.user_inquiries import update_user_seller
from utils.misc.start_by_time import first_scan
from utils.wb_api.method_warehouse import valid_token


@dp.callback_query_handler(text="free_connection")
async def show_connection_menu(call: CallbackQuery):
    await bot.send_video(chat_id=call.message.chat.id, video=open('static/welcome_video.mp4', 'rb'))
    await call.message.answer(
        "\n".join(
            [
                f'🛠 {hbold("ПОДКЛЮЧЕНИЕ")}\n',
                f'1️⃣ Зайдите в личный кабинет Wildberries → Настройки → Доступ к API ',
                f'{hlink("ссылка", "https://seller.wildberries.ru/supplier-settings/access-to-api")}\n',
                f'2️⃣ Скопируйте ключ для работы с {hbold("API статистики x64")}(если ключа нет, создайте его и потом скопируйте).\n',
                f'3️⃣ Вставьте ключ в сообщении этого чата.\n',

            ]
        ), reply_markup=connection_keyboard
    )
    await States.FREE_CONNECTING_API.set()


@dp.callback_query_handler(text="about_api", state=States.FREE_CONNECTING_API)
async def show_about_api(call: CallbackQuery):
    await call.message.edit_text(
        "\n".join(
            [
                f'⚙️ {hbold("API-ключ Wildberries")}\n',
                f'Если кратко, то ➡️ API-ключ — это идентификатор поставщика Wildberries, '
                f'с помощью которого можно получать информацию о заказах, продажах, поступлениях, наличию на '
                f'складах и другим данным конкретного поставщика, без доступа к личному кабинету. '
                f'Далее на основе полученной информации можно строить аналитику.\n',
                f'API-ключ — это способ интегрирования с теми или иными сервисами (в том числе {hbold("WB Ninja Bot")}), '
                f'которые созданы для того, чтобы помочь поставщикам в работе с Wildberries. \n',
                f'{hbold("Преимущества API:")}\n',
                f'✴️ С помощью API вы получаете {hbold("детализированную")} информацию по продажам, заказам и поставкам. '
                f'WB же в большинстве своих отчетов даёт лишь общую информацию. '
                f'✴️ API безопасен и даёт возможность {hbold("только получать данные")}, это значит, что вероятность изменения или '
                f'какого-либо влияния на информацию исключена. \n',
                f'✴️ Вы в любой момент можете сгенерировать новый API-ключ в личном кабинете WB, а значит {hbold("отменить доступ")} к '
                f'статистическим данным для нашего бота или других сервисов.',

            ]
        ), reply_markup=back_to_connection
    )


@dp.callback_query_handler(text="back_connection", state=States.FREE_CONNECTING_API)
async def back_connection(call: CallbackQuery):
    await call.message.edit_text(
        "\n".join(
            [
                f'🛠 {hbold("ПОДКЛЮЧЕНИЕ")}\n',
                f'1️⃣ Зайдите в личный кабинет Wildberries → Настройки → Доступ к API ',
                f'{hlink("ссылка", "https://seller.wildberries.ru/supplier-settings/access-to-api")}\n',
                f'2️⃣ Скопируйте ключ для работы с {hbold("API статистики x64")}(если ключа нет, создайте его и потом скопируйте).\n',
                f'3️⃣ Вставьте ключ в сообщении этого чата.\n',

            ]
        ), reply_markup=connection_keyboard
    )


@dp.message_handler(state=States.FREE_CONNECTING_API)
async def connection_api_x64(message: types.Message, state: FSMContext):
    status = await valid_token(message.text)
    support_keyboard = InlineKeyboardMarkup(row_width=1)
    support_button = InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)
    support_keyboard.insert(support_button)
    if status == 200:
        await state.finish()
        api_x64 = message.text
        seller = await select_seller_by_api_x64(api_x64)
        if seller:
            await update_user_seller(seller=seller, user_id=message.from_user.id)
        else:
            if await check_free_trail(message.chat.id, api_x64):
                seller = await add_seller(api_x64=api_x64, reserve=14, export=True, bot_enable=True,
                                          name=message.from_user.full_name, tarif=True)
                await update_user_seller(seller=seller, user_id=message.from_user.id)
                await first_scan(seller.id, seller.api_x64)
                await append_free_trail(message.from_user.id, seller.api_x64)
            else:
                seller = await add_seller(api_x64=api_x64, reserve=14, export=True, bot_enable=False,
                                          name=message.from_user.full_name, tarif=False)
                await update_user_seller(seller=seller, user_id=message.from_user.id)
                await update_trail_fail(seller_id=seller.id)
        await message.answer(
            "\n".join(
                [
                    f'🛠 {hbold(BOT_NAME)} теперь работает на вас 🤜\n',
                    f'⏳ Как только на WB появится новый заказ, бот соберет необходимую статистику и пришлет уведомление.\n',
                    f'🚙 Если вы работаете по схеме {hbold("FBS")} (продажа со склада поставщика), используйте дополнительный API-ключ, '
                    f'чтобы бот мог отслеживать новые заказы.\n',
                ]
            )
        )
    elif status == 400 or status == 500:
        await message.answer(
            "\n".join(
                [
                    f'❌ {hbold("Ошибка!!")}',
                    f'⏱ {datetime.datetime.now().time().strftime("%H:%M:%S")}\n',
                    f'API-ключ (x64) некорректен!\n',
                    f'Отправьте правильный ключ заново в этом сообщении:',

                ]
            ), reply_markup=support_keyboard
        )
    else:
        await message.answer(
            "\n".join(
                [
                    f'👤 {hbold("Добавление продавца")}',
                    f'⏱ {datetime.datetime.now().time().strftime("%H:%M:%S")}\n',
                    f'❌{hbold("Ошибка!")} К сожалению сервера Wildberries не отвечают, '
                    f'пожалуйста попробуйте позже!\n',

                ]
            ), reply_markup=support_keyboard
        )
