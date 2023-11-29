from geopy.distance import great_circle
import random
import copy


class Cargo:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Point:
    """This is class of geolocation objects"""
    def __init__(self, name: str, latitude: float, longitude: float):
        self.name = name
        self.geo = (latitude, longitude)
        # dict of cargo who need for this point
        self.cargo_need_dict = {}

    def check_empty(self):
        """This method check empty point are not"""
        for weight in self.cargo_need_dict.values():
            if weight != 0:
                return True
        return False

    def show_state(self):
        """This method show what cargo in car now"""
        state = ""
        for cargo, weight in enumerate(self.cargo_need_dict):
            state += f"{cargo}: {weight}; "
        return state

    def add_cargo_in_need_dict(self, cargo: Cargo, weight: int) -> None:
        """This method add cargo and weight what need on this point"""
        self.cargo_need_dict[cargo] = weight
        # print(f"[INFO] add {cargo}={weight} kg in {self.name}")

    def add_cargos_list_in_dict(self, cargo_list: list) -> None:
        for cargo, weight in cargo_list:
            self.add_cargo_in_need_dict(cargo, weight)

    def __str__(self):
        return self.name


class Cars:
    """This class of cars object who transporting cargo"""
    def __init__(self, name: str, max_cargo: int, start_point: Point):
        """:arg
            name - car name
            max_cargo - max cargo mass kg for this car
            start_point - start geo point for this car
        """
        self.name = name
        self.max_cargo = max_cargo
        # start cargo = 0 kg
        self.now_cargo = 0
        self.start_point = start_point
        # cars start for the start point
        self.now_point = start_point
        # route of car. Example [point_1, point_2, point_3]
        self.route_list = []
        # in start total distance = 0 km
        self.total_distance = 0
        # cargo what car transport
        self.cargo_dict = {}

    def check_empty(self):
        """This method check empty car are not"""
        for weight in self.cargo_dict.values():
            if weight != 0:
                return True
        return False

    def show_state(self):
        """This method show what cargo in car now"""
        state = ""
        for cargo, weight in self.cargo_dict.items():
            state += f"{cargo}: {weight}; "
        return state

    def add_point_in_route(self, point: Point) -> None:
        """This method add point in route_list"""
        self.route_list.append(point)
        # print(f"[INFO] add {point} in {self.name} car")

    def create_random_route_for_one_car(self, point_list: list) -> None:
        """This class create random route for one car"""
        copy_point_list = point_list.copy()
        while copy_point_list:
            point = random.choice(copy_point_list)
            self.add_point_in_route(point)
            copy_point_list.remove(point)

    def add_cargo_in_car(self, cargo: Cargo, weight: int) -> None:
        """This method add cargo in car to weight"""
        self.cargo_dict[cargo] = weight
        # print(f"[INFO] add {cargo}={weight} kg in {self.name}")

    def add_cargo_list_in_dict(self, cargo_list: list) -> None:
        for cargo, weight in cargo_list:
            self.add_cargo_in_car(cargo, weight)

    def __str__(self):
        return self.name


class GeoMap:
    map_points_dict = {}
    map_cars_dict = {}

    @classmethod
    def get_distance(cls, point_1: Point, point_2: Point) -> float:
        """This method calculate distance between 2 class Point object
            :arg
            point_1 - first point object
            point_2 - second point object
        """
        distance = great_circle(point_1.geo, point_2.geo).km
        return round(distance, 2)

    @classmethod
    def add_points_on_map(cls, points_list: list) -> dict:
        """This method add all points on map"""
        for index, point in enumerate(points_list):
            cls.map_points_dict[index] = point
        return cls.map_points_dict

    @classmethod
    def add_cars_on_map(cls, cars_list: list) -> dict:
        """This method add all cars on map"""
        for index, car in enumerate(cars_list):
            cls.map_cars_dict[index] = car
        return cls.map_cars_dict

    # def __deepcopy__(self):
    #     return GeoMap(copy.deepcopy(self.map_points_dict, self.map_points_dict))


if __name__ == '__main__':
    perm = Point("Perm", 58.006207, 56.222767)
    chaykivskiy = Point("Chaykovskiy", 56.769138, 54.142214)
    print(GeoMap.get_distance(perm, chaykivskiy))
