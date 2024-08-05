from db.abstract_client import DataBaseClient
from components.test_checker.database.models import ModelsForChecker, KaAnswer, KaAnswerLog

class DbCheckerTest(DataBaseClient):
    def create_tables(self):
        ModelsForChecker.metadata.create_all(self.engine)
    
    def update_tables(self):
        ModelsForChecker.metadata.create_all(self.engine, checkfirst=True)
    
    def add_ka_answer(self, text, explanation, question_id):
        session = self.Session()
        new_answer = KaAnswer(text=text, explanation=explanation, question_id=question_id)
        session.add(new_answer)
        session.commit()
        session.refresh(new_answer)
        session.close()
        return new_answer.id

    def get_ka_answer(self, answer_id):
        session = self.Session()
        answer = session.query(KaAnswer).get(answer_id)
        session.close()
        return answer

    def add_ka_answer_log(self, answer_id, correct, timestamp, user_id):
        session = self.Session()
        new_answer_log = KaAnswerLog(answer_id=answer_id, correct=correct, timestamp=timestamp, user_id=user_id)
        session.add(new_answer_log)
        session.commit()
        session.refresh(new_answer_log)
        session.close()
        return new_answer_log.id

    def get_ka_answer_log(self, log_id):
        session = self.Session()
        answer_log = session.query(KaAnswerLog).get(log_id)
        session.close()
        return answer_log

    def get_answers_by_question_id(self, question_id):
        session = self.Session()
        answers = session.query(KaAnswer).filter(KaAnswer.question_id == question_id).all()
        session.close()
        return answers