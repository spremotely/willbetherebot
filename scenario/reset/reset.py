from scenario.scenario import Scenario


class Reset(Scenario):

    MESSAGE = "Все сохраненные места удалены"

    def __init__(self, context, location_repo, scenario=None):
        self.__context = context
        self.__location_repo = location_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        if not self.is_command(message, "reset"):
            return super().handle(chat, user, state, message)

        self.__location_repo.clear_locations(chat.id, user.id)
        self.__context.save_changes()
        return "message", self.MESSAGE
