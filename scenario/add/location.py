from scenario.scenario import Scenario


class Location(Scenario):

    MESSAGE = "Место сохранено"

    def __init__(
            self,
            context,
            state_repo,
            photo_repo,
            location_repo,
            scenario=None):
        self.__context = context
        self.__state_repo = state_repo
        self.__photo_repo = photo_repo
        self.__location_repo = location_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        if state.command == "add" and (
                state.state == "photo" or state.state == "location") and self.is_location(message):
            photo = self.__photo_repo.get_photo(state.entity.entity_id)
            self.__location_repo.create_location(
                chat, user, photo, message.location.longitude, message.location.latitude)
            self.__state_repo.update_state(state.id, message.message_id, "start", "welcome")
            self.__context.save_changes()
            return self.MESSAGE

        return super().handle(chat, user, state, message)
