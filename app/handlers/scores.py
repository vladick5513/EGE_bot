from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.bot.crud import create_student, get_student_by_name, add_score, get_scores
from app.database import async_session_factory
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class UserStates(StatesGroup):
    enter_scores = State()
    view_scores = State()


#Ввод баллов
@router.message(Command("enter_scores"))
async def enter_scores_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    if "student_id" in data:
        await state.set_state(UserStates.enter_scores)
        await message.answer("Введите данные в формате: предмет балл через пробел.")
    else:
        await message.answer("Вы не вошли в систему. Используйте /register или /login.")

@router.message(UserStates.enter_scores)
async def process_scores(message: Message, state: FSMContext):
    try:
        subject, score = message.text.split(maxsplit=1)
        score = int(score)
        data = await state.get_data()
        student_id = data["student_id"]
        async with async_session_factory() as session:
            # Сохраняем баллы в БД
            await add_score(session, student_id, subject, score)
            await message.answer(
                f"Баллы по предмету {subject} ({score}) сохранены.\n"
                "Вы можете:\n"
                "• Добавить ещё баллы — отправьте команду /enter_scores\n"
                "• Посмотреть все баллы — команда /view_scores"
            )
            # Завершаем текущее состояние после ввода
            await state.set_state(None)
    except ValueError:
        await message.answer("Ошибка! Введите данные в формате: предмет балл.")

@router.message(Command("view_scores"))
async def view_scores_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    if "student_id" in data:
        async with async_session_factory() as session:
            student_id = data["student_id"]
            scores = await get_scores(session, student_id)
            if scores:
                scores_text = "\n".join(f"{s.subject}: {s.score}" for s in scores)
                await message.answer(
                    f"Ваши баллы:\n{scores_text}\n\n"
                    "Вы можете:\n"
                    "• Добавить новые баллы — команда /enter_scores\n"
                )
            else:
                await message.answer("У вас пока нет сохранённых баллов.")
    else:
        await message.answer("Вы не вошли в систему. Используйте /register для регистрации или /login для входа.")