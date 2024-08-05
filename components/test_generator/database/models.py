from sqlalchemy import create_engine, Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

ModelsForGenerate = declarative_base()

class KAQuestion(ModelsForGenerate):
    __tablename__ = 'ka_question'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False, default="")
    difficulty = Column(Integer, nullable=False, default=0)
    disable = Column(Boolean, nullable=False, default=False)

    question_variants = relationship('KAQuestionVariant', back_populates='question')

    def __repr__(self):
        return f"<KAQuestion(id={self.id}, text={self.text}, difficulty={self.difficulty}, disable={self.disable})>"

class KATest(ModelsForGenerate):
    __tablename__ = 'ka_test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=True)
    on = Column(Boolean, nullable=False, default=False)
    variants_count = Column(Integer, nullable=False, default=0)
    minutes = Column(Integer, nullable=False, default=0)

    variants = relationship('KAVariant', back_populates='test')

    def __repr__(self):
        return f"<KATest(id={self.id}, text={self.text}, on={self.on}, variants_count={self.variants_count}, minutes={self.minutes})>"


class KAVariant(ModelsForGenerate):
    __tablename__ = 'ka_variant'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)
    ka_test = Column(Integer, ForeignKey('ka_test.id'))

    test = relationship('KATest', back_populates='variants')
    question_variants = relationship('KAQuestionVariant', back_populates='variant')

    def __repr__(self):
        return f"<KAVariant(id={self.id}, number={self.number}, ka_test={self.ka_test})>"



class KAQuestionVariant(ModelsForGenerate):
    __tablename__ = 'ka_question_variant'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ka_question_id = Column(Integer, ForeignKey('ka_question.id'))
    ka_variant_id = Column(Integer, ForeignKey('ka_variant.id'))

    question = relationship('KAQuestion', back_populates='question_variants')
    variant = relationship('KAVariant', back_populates='question_variants')

    def __repr__(self):
        return f"<KAQuestionVariant(id={self.id}, ka_question_id={self.ka_question_id}, ka_variant_id={self.ka_variant_id})>"
