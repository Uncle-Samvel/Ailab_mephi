from at_queue.core.at_component import ATComponent
from at_queue.core.session import ConnectionParameters
from at_queue.utils.decorators import component_method
import asyncio

class SummRequester(ATComponent):

    # вызов внешнего метода с корректными данными
    @component_method
    async def request_variant(self) -> int:
        result = await self.exec_external_method(
            reciever='Generator', 
            methode_name='get_variant', 
            method_args={}
        )
        return result



async def main():
    connection_parameters = ConnectionParameters('amqp://localhost:5672/') # Параметры подключения к RabbitMQ

    summ_requester = SummRequester(connection_parameters=connection_parameters) # Создание компонента
    await summ_requester.initialize() # Подключение компонента к RabbitMQ
    await summ_requester.register() # Отправка сообщения на регистрацию в брокер

    # Запуск в режиме ожидания сообщений, не блокируя выполнение
    loop = asyncio.get_event_loop()
    task = loop.create_task(summ_requester.start())

    # Запрос суммы без ошибок
    res = await summ_requester.request_sum()
    print('External result:', res)

    # Запрос суммы с ошибками
    await summ_requester.request_sum_with_errors()

    # Обждание завершения
    await task


if __name__ == '__main__':
    asyncio.run(main())