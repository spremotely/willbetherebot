from scenario.scenario import Scenario


class ListAll(Scenario):

    NO_LOCATIONS_MESSAGE = "Не найдено сохраненных мест"

    def __init__(self, location_repo, scenario=None):
        self.__location_repo = location_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        if not self.is_command(message, "list_all"):
            return super().handle(chat, user, state, message)

        locations = self.__location_repo.get_locations(chat.id, user.id)

        if len(locations) == 0:
            return "message", self.NO_LOCATIONS_MESSAGE
        return "locations", locations
