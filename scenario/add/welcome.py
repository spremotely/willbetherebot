from scenario.scenario import Scenario


class Welcome(Scenario):

    MESSAGE = "Отправьте фото места, которое хотите сохранить"

    def __init__(self, context, state_repo, scenario=None):
        self.__context = context
        self.__state_repo = state_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        if state.command == "add" and state.state == "welcome" and not self.is_command(
                message) and not self.is_location(message) and not self.is_photo(message):
            return self.MESSAGE

        if self.is_command(message, "add"):
            self.__state_repo.update_state(
                state.id, message.message_id, "add", "welcome")
            self.__context.save_changes()
            return self.MESSAGE

        return super().handle(chat, user, state, message)
