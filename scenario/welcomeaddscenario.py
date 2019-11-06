from scenario.scenario import Scenario


class WelcomeAddScenario(Scenario):

    MESSAGE = "Отправьте фото места, которое хотите сохранить"

    def __init__(self, context, state_repo):
        self._context = context
        self._state_repo = state_repo

    def set_next(self, scenario):
        super().set_next(scenario)

    def handle(self, chat, user, message):
        state = self._state_repo.get_state(chat.id, user.id)

        if not state:
            self._state_repo.create_state(chat, user, message.message_id, "add", "welcome")
            self._context.save_changes()
            return self.MESSAGE

        if state.command != "add":
            self._state_repo.update_state(state.id, "add", "welcome")
            self._context.save_changes()
            return self.MESSAGE

        if state.command == "add" and state.state == "welcome":
            return self.MESSAGE

        return super().handle(chat, user, message)
