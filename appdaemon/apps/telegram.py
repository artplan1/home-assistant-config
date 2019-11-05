# docs https://www.home-assistant.io/integrations/telegram_chatbot/

import appdaemon.plugins.hass.hassapi as hass

cleaner_keyboard = [
    [("Старт", "/start_clean"), ("Стоп", "/stop_clean")],
    [("На базу", "/cleaner_to_base")]
]

kettle_keyboard = [
    [('Вскипятить', '/kettle_boil'), ('Стоп', '/stop_boiling')],
    [('Статус', '/kettle_status')]
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
        elif command == '/kettle':
            self.call_service('telegram_bot/send_message',
                            title='Команда',
                            target=user_id,
                            message="",
                            disable_notification=True,
                            inline_keyboard=kettle_keyboard)

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

        elif data_callback == '/kettle_boil':
            self.call_service('water_heater/turn_on')

            self.call_service('telegram_bot/answer_callback_query',
                                message='Кипятим',
                                callback_query_id=callback_id)

        elif data_callback == '/stop_boiling':
            self.call_service('water_heater/turn_off')

            self.call_service('telegram_bot/answer_callback_query',
                                message='ОК',
                                callback_query_id=callback_id)

        elif data_callback == '/kettle_status':
            kettle_state = self.get_state("water_heater.g200s", attribute="all")

            self.call_service('telegram_bot/send_message',
                                message=str(kettle_state['attributes']),
                                target=chat_id)
