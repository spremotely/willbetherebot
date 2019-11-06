from scenario.scenario import Scenario


class Photo(Scenario):

    MESSAGE = "Отправьте локацию места"

    def __init__(self, context, state_repo, scenario=None):
        self.__context = context
        self.__state_repo = state_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        if message.content_type != "photo":
            return super().handle(chat, user, state, message)

        if not state:
            return super().handle(chat, user, state, message)

        if state.command != "add":
            return super().handle(chat, user, state, message)

        if state.command == "start" and state.state == "welcome":
            # update photo
            pass

        # create photo
        self.__state_repo.update_state(state.id, "add", "photo")
        self.__context.save_changes()
        return self.MESSAGE
