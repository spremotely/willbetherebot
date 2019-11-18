from scenario.scenario import Scenario


class Reset(Scenario):

    def __init__(self, location_repo, scenario=None):
        self.__location_repo = location_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        pass
