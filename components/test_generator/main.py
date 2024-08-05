import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from at_queue.core.at_component import ATComponent
from at_queue.core.session import ConnectionParameters
from at_queue.utils.decorators import component_method
from components.test_generator.database import DbGeneratorTest
from components.test_generator.database.serialaze import *
from random import randint

import json
import asyncio
import logging

class Generator(ATComponent): 
    @component_method
    def generate(self, amount: int, test_id: int) -> list:
        questions = db.get_all_questions()
        response = []
        var = list()
        amount_var = len(list(filter(lambda x: x.ka_test == test_id, db.get_all_variants())))
        for i in range(amount):
            amount_var += 1
            response.append(db.add_variant(test_id=test_id, number=amount_var))
            set_questions = set()
            while len(set_questions) != 5:
                set_questions.add(randint(1,len(questions)))
            for question in set_questions:
                db.add_question_to_variant(question, response[-1])
        
        db.update_test(test_id=test_id, variants_count=amount_var)

        return response
    
    @component_method
    def get_variant(self, test_id: int) -> list:
        number_variant = randint(1,db.get_test(test_id=test_id).variants_count)
        questions = db.get_questions_by_test_and_variant_number(test_id=test_id,variant_number=number_variant)
        question_schema = KAQuestionSchema(many=True)
        questions_json = question_schema.dump(questions)
        return questions_json


        
    
async def main():
    connection_parameters = ConnectionParameters('amqp://localhost:5672/') # Параметры подключения к RabbitMQ
    generator = Generator(connection_parameters=connection_parameters) # Создание компонента
    await generator.initialize() # Подключение компонента к RabbitMQ
    await generator.register() # Отправка сообщения на регистрацию в брокер
    await generator.start() # Запуск компонента в режиме ожидания сообщений

if __name__ == '__main__':
    db = DbGeneratorTest(user="user", password="pass", host="localhost", port=5555, database="database")
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())