from scenario.scenario import Scenario


class Default(Scenario):

    MESSAGE = "Этот бот сохраняет места для будущего посещения\n" \
              "/add - добавить место\n" \
              "/list_all - список всех сохраненных мест\n" \
              "/list - список ближайших в радиусе 500 метров мест\n" \
              "/reset - удалить все сохраненные места\n"

    def __init__(self, scenario=None):
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        return "message", self.MESSAGE
