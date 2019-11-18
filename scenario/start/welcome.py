from scenario.scenario import Scenario


class Welcome(Scenario):
    MESSAGE = "Этот бот сохраняет места для будущего посещения\n" \
              "/add - добавить место\n" \
              "/list - список мест\n" \
              "/reset - удалить все сохраненные места\n"

    def __init__(self, context, state_repo, scenario=None):
        self.__context = context
        self.__state_repo = state_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        if not state:
            self.__state_repo.create_state(
                chat, user, message.message_id, "start", "welcome")
            self.__context.save_changes()
            return self.MESSAGE

        if state.command == "start" and state.state == "welcome" and not self.is_command(
                message):
            return self.MESSAGE

        if self.is_command(message, "start"):
            self.__state_repo.update_state(
                state.id, message.message_id, "start", "welcome")
            self.__context.save_changes()
            return self.MESSAGE

        return super().handle(chat, user, state, message)
