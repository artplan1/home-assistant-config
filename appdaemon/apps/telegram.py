# docs https://www.home-assistant.io/integrations/telegram_chatbot/

import appdaemon.plugins.hass.hassapi as hass

cleaner_keyboard = [
    [("Старт", "/start_clean"), ("Стоп", "/stop_clean")],
    [("На базу", "/cleaner_to_base")]
]

class TelegramBotEventListener(hass.Hass):
    def initialize(self):
        self.listen_event(self.receive_telegram_callback, 'telegram_callback')
        self.listen_event(self.receive_telegram_command, 'telegram_command')

    def receive_telegram_command(self, event_id, payload_event, *args):
        assert event_id == 'telegram_command'

        print("Telegram command " + str(payload_event))

        user_id = payload_event['user_id']
        command = payload_event['command']

        if command == '/cleaner':
            self.call_service('telegram_bot/send_message',
                            title='Команда',
                            target=user_id,
                            message="",
                            disable_notification=True,
                            inline_keyboard=cleaner_keyboard)

    def receive_telegram_callback(self, event_id, payload_event, *args):
        assert event_id == 'telegram_callback'

        print("Telegram callback " + str(payload_event))

        data_callback = payload_event['data']
        callback_id = payload_event['id']
        chat_id = payload_event['chat_id']

        if data_callback == "/start_clean":
            self.call_service('script/vacuum_all')

            self.call_service('telegram_bot/answer_callback_query',
                                message='Начало уборки',
                                callback_query_id=callback_id)

        elif data_callback == "/stop_clean":
            self.call_service('script/vacuum_stop')

            self.call_service('telegram_bot/answer_callback_query',
                                message='Остановка уборки',
                                callback_query_id=callback_id)

        elif data_callback == "/cleaner_to_base":
            self.call_service('script/vacuum_return_to_base')

            self.call_service('telegram_bot/answer_callback_query',
                                message='Возврат на базу',
                                callback_query_id=callback_id)
