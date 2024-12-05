from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.bot.crud import create_student, get_student_by_name, add_score, get_scores
from app.database import async_session_factory
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    login = State()
    register = State()


router = Router()

# Команда /start
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать в бота для управления баллами ЕГЭ!\n"
        "Вот что я могу:\n"
        "1. Зарегистрироваться — команда /register\n"
        "2. Войти в аккаунт — команда /login\n"
        "3. Ввести баллы — команда /enter_scores\n"
        "4. Просмотреть баллы — команда /view_scores\n\n"
        "Попробуйте начать с команды /register или /login!"
    )

@router.message(Command("register"))
async def register_handler(message: Message, state: FSMContext):
    await state.set_state(UserStates.register)
    await message.answer("Введите своё имя и фамилию через пробел для регистрации.")

@router.message(UserStates.register)
async def process_registration(message: Message, state: FSMContext):
    try:
        # Проверяем корректность ввода
        first_name, last_name = message.text.split(maxsplit=1)
        async with async_session_factory() as session:
            student = await create_student(session, first_name, last_name)
            # Сохраняем данные в FSM
            await state.update_data(student_id=student.id, name=f"{first_name} {last_name}")
            await message.answer(
                f"Регистрация успешна! Ваш ID: {student.id}.\n"
                "Теперь вы можете:\n"
                "• Ввести баллы — команда /enter_scores\n"
                "• Просмотреть баллы — команда /view_scores"
            )
            # Завершаем текущее состояние
            await state.set_state(None)
    except ValueError:
        await message.answer("Ошибка! Введите имя и фамилию через пробел.")

@router.message(Command("login"))
async def login_handler(message: Message, state: FSMContext):
    # Проверяем, вошел ли пользователь уже
    data = await state.get_data()
    if "student_id" in data:
        await message.answer("Вы уже вошли в систему. Можете вводить баллы или просматривать их.")
        return
    await state.set_state(UserStates.login)
    await message.answer("Введите своё имя и фамилию через пробел для входа.")

@router.message(UserStates.login)
async def process_login(message: Message, state: FSMContext):
    try:
        first_name, last_name = message.text.split(maxsplit=1)
        async with async_session_factory() as session:
            student = await get_student_by_name(session, first_name, last_name)
            if student:
                # Сохраняем данные пользователя в FSM
                await state.update_data(student_id=student.id, name=f"{first_name} {last_name}")
                await message.answer(
                    f"Вы успешно вошли! Ваш ID: {student.id}.\n"
                    "Теперь вы можете:\n"
                    "• Ввести баллы — команда /enter_scores\n"
                    "• Просмотреть баллы — команда /view_scores"
                )
                # Завершаем текущее состояние
                await state.set_state(None)
            else:
                await message.answer("Пользователь не найден. Пожалуйста, зарегистрируйтесь с помощью /register.")
    except ValueError:
        await message.answer("Ошибка! Введите имя и фамилию через пробел.")