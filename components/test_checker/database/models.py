from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

ModelsForChecker = declarative_base()

class KaAnswer(ModelsForChecker):
    __tablename__ = 'ka_answer'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False, default='')
    correct = Column(Boolean, nullable=False, default=False)
    ka_question_id = Column(Integer)

class KaAnswerLog(ModelsForChecker):
    __tablename__ = 'ka_answer_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ka_variants_id = Column(Integer)
    ka_questions_id = Column(Integer)
    ka_answers_id = Column(Integer, ForeignKey('ka_answer.id'))
    user_id = Column(Integer)
    date = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    answer = relationship("Answer", back_populates="answer_logs")
