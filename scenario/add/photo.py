from scenario.scenario import Scenario


class Photo(Scenario):

    PHOTO_SAVED_MESSAGE = "Фото места сохранено"
    MESSAGE = "Отправьте локацию места"

    def __init__(
            self,
            context,
            state_repo,
            photo_repo,
            entity_repo,
            scenario=None):
        self.__context = context
        self.__state_repo = state_repo
        self.__photo_repo = photo_repo
        self.__entity_repo = entity_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        if state.command == "add" and state.state == "photo" and not self.is_command(
                message) and not self.is_location(message):
            return self.MESSAGE

        if state.command == "add" and (
                state.state == "welcome" or state.state == "photo") and self.is_photo(message):
            photo = self.__photo_repo.create_photo(message.photo[0].file_id)
            entity = self.__entity_repo.create_entity(photo.id, "photo")
            self.__state_repo.update_state(
                state.id, message.message_id, "add", "photo", entity)
            self.__context.save_changes()
            return f"{self.PHOTO_SAVED_MESSAGE}\n{self.MESSAGE}"

        return super().handle(chat, user, state, message)
