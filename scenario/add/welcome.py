from scenario.scenario import Scenario


class Welcome(Scenario):

    MESSAGE = "Отправьте фото места, которое хотите сохранить"

    def __init__(self, context, state_repo, scenario=None):
        self.__context = context
        self.__state_repo = state_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        if message.content_type != "text" or not message.text.startswith("/add"):
            return super().handle(chat, user, state, message)

        if not state:
            self.__state_repo.create_state(chat, user, message.message_id, "add", "welcome")
            self.__context.save_changes()
            return self.MESSAGE

        if state.command != "add":
            self.__state_repo.update_state(state.id, "add", "welcome")
            self.__context.save_changes()
            return self.MESSAGE

        if state.command == "add" and state.state == "welcome":
            return self.MESSAGE

        return super().handle(chat, user, state, message)
