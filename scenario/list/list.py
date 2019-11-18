import math

from scenario.scenario import Scenario


class List(Scenario):

    EARTH_RADIUS = 6371.0
    NO_LOCATIONS_MESSAGE = "Не найдено ближайших мест"

    def __init__(self, context, state_repo, location_repo, scenario=None):
        self.__context = context
        self.__state_repo = state_repo
        self.__location_repo = location_repo
        super().__init__(scenario)

    def handle(self, chat, user, state, message):
        if state.command == "list" and state.state == "location" and self.is_location(
                message):
            self.__state_repo.update_state(
                state.id, message.message_id, "start", "welcome")
            self.__context.save_changes()
            locations = self.__location_repo.get_locations(chat.id, user.id)
            locations = self.patch_locations_by_distances(message.location, locations)
            locations = [location for location, distance in locations if distance <= 0.5]

            if len(locations) == 0:
                return "message", self.NO_LOCATIONS_MESSAGE
            return "locations", locations

        return super().handle(chat, user, state, message)

    def patch_locations_by_distances(self, current_location, locations):
        return [(location, self.get_distance(current_location, location))
                for location in locations]

    def get_distance(self, current_location, destination_location):
        latitude1 = math.radians(current_location.latitude)
        longitude1 = math.radians(current_location.longitude)
        latitude2 = math.radians(destination_location.latitude)
        longitude2 = math.radians(destination_location.longitude)

        delta_latitude = latitude2 - latitude1
        delta_longitude = longitude2 - longitude1
        a = math.sin(delta_latitude / 2.0)**2 + math.cos(latitude1) * \
            math.cos(latitude2) * math.sin(delta_longitude / 2.0)**2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return self.EARTH_RADIUS * c
