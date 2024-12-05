from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    scores = relationship("Score", back_populates="student")

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="scores")