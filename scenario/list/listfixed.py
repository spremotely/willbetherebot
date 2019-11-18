from scenario.scenario import Scenario


class ListFixed(Scenario):

    def __init__(self, location_repo, scenario=None):
        self.__location_repo = location_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        if not self.is_command(message, "list", r"[\d]*$"):
            return super().handle(chat, user, state, message)

        limit = self.get_number(message, "list", r"[\d]*$")
        return "locations", self.__location_repo.get_locations(chat.id, user.id, limit)
