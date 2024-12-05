from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Student, Score

async def create_student(session: AsyncSession, first_name: str, last_name: str):
    student = Student(first_name=first_name, last_name=last_name)
    session.add(student)
    await session.commit()
    await session.refresh(student)
    return student

async def add_score(session: AsyncSession, student_id: int, subject: str, score: int):
    score_entry = Score(subject=subject, score=score, student_id=student_id)
    session.add(score_entry)
    await session.commit()

async def get_scores(session: AsyncSession, student_id: int):
    result = await session.execute(select(Score).where(Score.student_id == student_id))
    return result.scalars().all()

async def get_student_by_name(session: AsyncSession, first_name: str, last_name: str):
    result = await session.execute(
        select(Student).where(
            Student.first_name == first_name,
            Student.last_name == last_name
        )
    )
    return result.scalar()