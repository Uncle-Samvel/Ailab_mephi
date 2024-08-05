from sqlalchemy.orm import joinedload
from db.abstract_client import DataBaseClient
from components.test_generator.database.models import ModelsForGenerate, KAQuestion, KAQuestionVariant, KATest, KAVariant

class DbGeneratorTest(DataBaseClient):
    def create_tables(self):
        ModelsForGenerate.metadata.create_all(self.engine)
    
    def update_tables(self):
        ModelsForGenerate.metadata.create_all(self.engine, checkfirst=True)
    
    def add_question(self, text, difficulty, disable):
        session = self.Session()
        new_question = KAQuestion(text=text, difficulty=difficulty, disable=disable)
        session.add(new_question)
        session.commit()
        session.refresh(new_question)
        session.close()
        return new_question.id

    def get_question(self, question_id):
        session = self.Session()
        question = session.query(KAQuestion).get(question_id)
        session.close()
        return question

    def add_test(self, text, on, variants_count, minutes):
        session = self.Session()
        new_test = KATest(text=text, on=on, variants_count=variants_count, minutes=minutes)
        session.add(new_test)
        session.commit()
        session.refresh(new_test)
        session.close()
        return new_test.id


    def get_test(self, test_id):
        session = self.Session()
        test = session.query(KATest).get(test_id)
        session.close()
        return test

    def add_variant(self, test_id, number):
        session = self.Session()
        new_variant = KAVariant(ka_test=test_id, number=number)
        session.add(new_variant)
        session.commit()
        session.refresh(new_variant)
        session.close()
        return new_variant.id


    def get_variant(self, variant_id):
        session = self.Session()
        variant = session.query(KAVariant).get(variant_id)
        session.close()
        return variant

    def add_question_to_variant(self, question_id, variant_id):
        session = self.Session()
        new_qv = KAQuestionVariant(ka_question_id=question_id, ka_variant_id=variant_id)
        session.add(new_qv)
        session.commit()
        session.refresh(new_qv)
        session.close()
        return new_qv.id


    def get_question_variant(self, qv_id):
        session = self.Session()
        question_variant = session.query(KAQuestionVariant).get(qv_id)
        session.close()
        return question_variant

    def get_all_questions(self):
        session = self.Session()
        questions = session.query(KAQuestion).all()
        session.close()
        return questions

    def get_all_tests(self):
        session = self.Session()
        tests = session.query(KATest).all()
        session.close()
        return tests

    def get_all_variants(self):
        session = self.Session()
        variants = session.query(KAVariant).all()
        session.close()
        return variants

    def get_all_question_variants(self):
        session = self.Session()
        question_variants = session.query(KAQuestionVariant).all()
        session.close()
        return question_variants

    def update_question(self, question_id, text=None, difficulty=None, disable=None):
        session = self.Session()
        question = session.query(KAQuestion).get(question_id)
        if question:
            if text is not None:
                question.text = text
            if difficulty is not None:
                question.difficulty = difficulty
            if disable is not None:
                question.disable = disable
            session.commit()
        session.close()

    def update_test(self, test_id, text=None, on=None, variants_count=None, minutes=None):
        session = self.Session()
        test = session.query(KATest).get(test_id)
        if test:
            if text is not None:
                test.text = text
            if on is not None:
                test.on = on
            if variants_count is not None:
                test.variants_count = variants_count
            if minutes is not None:
                test.minutes = minutes
            session.commit()
        session.close()

    def update_variant(self, variant_id, test_id=None, number=None):
        session = self.Session()
        variant = session.query(KAVariant).get(variant_id)
        if variant:
            if test_id is not None:
                variant.ka_test = test_id
            if number is not None:
                variant.number = number
            session.commit()
        session.close()

    def update_question_variant(self, qv_id, question_id=None, variant_id=None):
        session = self.Session()
        qv = session.query(KAQuestionVariant).get(qv_id)
        if qv:
            if question_id is not None:
                qv.ka_question_id = question_id
            if variant_id is not None:
                qv.ka_variant_id = variant_id
            session.commit()
        session.close()


    def get_questions_by_test_and_variant_number(self, test_id, variant_number):
        session = self.Session()
        questions = (
            session.query(KAQuestion)
            .join(KAQuestionVariant, KAQuestion.id == KAQuestionVariant.ka_question_id)
            .join(KAVariant, KAVariant.id == KAQuestionVariant.ka_variant_id)
            .join(KATest, KATest.id == KAVariant.ka_test)
            .filter(KATest.id == test_id, KAVariant.number == variant_number)
            .options(joinedload(KAQuestion.question_variants).joinedload(KAQuestionVariant.variant))
            .all()
        )
        session.close()
        return questions