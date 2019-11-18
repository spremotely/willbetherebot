from scenario.scenario import Scenario


class Default(Scenario):

    MESSAGE = "Этот бот сохраняет места для будущего посещения\n" \
              "/add - добавить место\n" \
              "/list - список мест\n" \
              "/reset - удалить все сохраненные места\n"

    def __init__(self, scenario=None):
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        return self.MESSAGE
