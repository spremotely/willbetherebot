from scenario.scenario import Scenario


class Welcome(Scenario):

    MESSAGE = "Отправьте текущую локацию"

    def __init__(self, context, state_repo, scenario=None):
        self.__context = context
        self.__state_repo = state_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        if state.command == "list" and state.state == "location" and not self.is_command(
                message) and not self.is_location(message):
            return "message", self.MESSAGE

        if not self.is_command(message, "list"):
            return super().handle(chat, user, state, message)

        if self.is_command(message, "list"):
            self.__state_repo.update_state(
                state.id, message.message_id, "list", "location")
            self.__context.save_changes()
            return "message", self.MESSAGE

        return super().handle(chat, user, state, message)
