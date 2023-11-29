import random
import logging
import copy
import time

from objects import GeoMap, Cars, Point
from obj_fil import create_map_object


logging.basicConfig(level=logging.INFO)


epochs_mut_dict = {
    0: 0.6,
    200: 0.6,
    400: 0.4,
    600: 0.3,
    800: 0.2,
    900: 0.1
}


class RouteGenetic:
    """This class create genetic algorithm for find optimal route for cars"""
    POPULATION_DICT = {}
    POPULATION_RESULT = {}
    RESULTS_LIST = []
    COINCIDENCE = 0
    NEED_STOP_FLAG = False

    def __init__(self, bot_counts=100, populations=1000, alive_bots=10):
        self.map_obj = create_map_object()
        # self.map_obj_one_bot = None
        self.mut = epochs_mut_dict[0]
        self.bot_counts = bot_counts
        self.populations = populations
        self.alive_bots = alive_bots
        logging.info("Init genecit object")

    def show_distance(self, target_point_number: int, car_number: int):
        """This method check distance between 2 points"""
        car_point_now = self.map_obj_one_bot.map_cars_dict[car_number].now_point
        target_point = self.map_obj_one_bot.map_points_dict[target_point_number]
        logging.info(f"Car-{car_number} try to visit Point-{target_point_number}")
        # check need car visit this point are not
        need = self.check_need_visit_point_are_not(target_point_number=target_point_number, car_number=car_number)
        if need == True:
            car = self.map_obj_one_bot.map_cars_dict[car_number]
            # create string then show how cargo in this car
            state_before = self.map_obj_one_bot.map_cars_dict[car_number].show_state()
            logging.info(f"Before visit Point {target_point}: {car} -> {state_before}")
            self.unload_cargo_on_point(car=car, point=target_point)
            state_after = self.map_obj.map_cars_dict[car_number].show_state()
            # create string then show how cargo in this car after unload
            logging.info(f"After visit {target_point}: {car} -> {state_after}")
            # calc distance between 2 points
            distance = self.map_obj_one_bot.get_distance(point_1=car_point_now, point_2=target_point)
            car.total_distance += distance
            self.map_obj.map_cars_dict[car_number].route_list.append(target_point_number)
            logging.info(f"{car} gone {distance} KM")
            # change point (car was travel on next point)
            self.map_obj_one_bot.map_cars_dict[car_number].now_point = target_point
            return distance
        else:
            logging.info(f"In Point-{target_point_number} don't need cargo from Car-{car_number}")

    def unload_cargo_on_point(self, car: Cars, point: Point) -> None:
        """This method for sycle on all cargo and car, and dec weight this cargo in weight on point"""
        for cargo, weight in car.cargo_dict.items():
            if cargo in point.cargo_need_dict:
                if weight != 0 and point.cargo_need_dict[cargo] != 0:
                    # if weight cargo on point > car
                    if point.cargo_need_dict[cargo] > weight:
                        point.cargo_need_dict[cargo] = point.cargo_need_dict[cargo] - weight
                        car.cargo_dict[cargo] = 0
                        logging.info(f"{car} unload {weight} {cargo} in {point}")
                    # if weight cargo on point == car
                    elif point.cargo_need_dict[cargo] == weight:
                        point.cargo_need_dict[cargo] = 0
                        car.cargo_dict[cargo] = 0
                        logging.info(f"{car} unload {weight} {cargo} in {point}")
                    # if weight cargo on point < car
                    else:
                        logging.info(f"{car} unload {point.cargo_need_dict[cargo]} {cargo} in {point}")
                        car.cargo_dict[cargo] = car.cargo_dict[cargo] - point.cargo_need_dict[cargo]
                        point.cargo_need_dict[cargo] = 0

    def check_need_visit_point_are_not(self, target_point_number: int, car_number: int) -> float:
        """This method look cargo in car and see need this cargo in point are not"""
        target_point = self.map_obj_one_bot.map_points_dict[target_point_number]
        car = self.map_obj_one_bot.map_cars_dict[car_number]
        for cargo in car.cargo_dict:
            # if car in not empty
            if car.cargo_dict[cargo] != 0:
                # if cargo need on point
                if cargo in target_point.cargo_need_dict:
                    if target_point.cargo_need_dict[cargo] != 0:
                        return True
        return False

    def run_genetics(self):
        """This method run genetic algorithm"""
        time_start = time.time()
        logging.info(f"Start algoritmn\n\n{'#'*100}")
        start_flag = True
        for population in range(self.populations):
            if self.NEED_STOP_FLAG == True:
                break
            if population in epochs_mut_dict:
                self.mut = epochs_mut_dict[population]
            self.POPULATION_RESULT = {}

            if start_flag == True:          # first iteration
                self.create_population()
                start_flag = False
                self.run_one_population(population)
                best_epochs_bots_dict = self.find_best_bot_result()
                self.create_genetic_population(best_epochs_bots_dict)
            else:
                print(f"GEN POPUL: {self.POPULATION_DICT}")
                self.run_one_population(population)
                best_epochs_bots_dict = self.find_best_bot_result()
                self.create_genetic_population(best_epochs_bots_dict)
            logging.info(f"POPULATION {population} end: {time.time() - time_start}\n\n{'#'*100}")
            self.print_final_res(best_epochs_bots_dict)
        logging.info(f"Algoritmn end: {time.time() - time_start}")
        # logging.info(f"Best result: {best_epochs_bots_dict}")
        self.print_final_res(best_epochs_bots_dict, True)

    def print_final_res(self, best_rest: dict, final_flag=False):
        distance_dict = {}
        distance_list = []
        for key in best_rest:
            distance_dict[best_rest[key]["bot_total_distance"]] = best_rest[key]
            distance_list.append(best_rest[key]["bot_total_distance"])
        res = max(distance_list)
        logging.info(f"BEST ROUTE: {distance_dict[res]}")
        if self.RESULTS_LIST:
            if res == self.RESULTS_LIST[-1]:
                self.COINCIDENCE += 1
            if res != self.RESULTS_LIST[-1]:
                self.COINCIDENCE = 0
            if self.COINCIDENCE > 50:
                self.NEED_STOP_FLAG = True
            self.RESULTS_LIST.append(res)
        if final_flag == True:
            logging.info(f"\n{'#'*100}\nBEST RESULT: {res}")
        else:
            logging.info(f"\n{'#'*100}\nPOPULATION BEST RESULT: {res}")
            print(self.RESULTS_LIST)

    def find_best_bot_result(self):
        result_dict = {}
        result_list = []
        for bot_data in self.POPULATION_RESULT.values():
            result_list.append(bot_data["bot_total_distance"])
        tmp_result_list = copy.copy(result_list)
        sorted_list = sorted(tmp_result_list)[:self.alive_bots]
        for res in sorted_list:
            index = result_list.index(res)
            result_dict[index] = self.POPULATION_RESULT[index]
        return result_dict

    def run_one_population(self, i):
        logging.info(f"\nSTART POPULATION {i} in {self.populations}\n{'#'*100}")
        for bot_number in self.POPULATION_DICT.keys():
            logging.info(f"\n\nSTART BOT - {bot_number} in {self.bot_counts}. POPULATION: {i}\n{'#'*100}")
            self.run_one_bot(bot_number)

    def run_one_bot(self, bot_number=0):
        bot = self.POPULATION_DICT[bot_number]
        self.map_obj_one_bot = create_map_object()
        n = 0
        while bot:
            # if car visit all point break while
            if not bot:
                self.fill_info_about_one_bot_work(bot_number)
                break
            for car_number in list(bot.keys()):                 # car
                one_car_route = bot[car_number]
                target_point_number = one_car_route.pop(0)      # target
                self.show_distance(target_point_number=target_point_number, car_number=car_number)
                # if car visit all points del car in list
                if not one_car_route:
                    now_point = self.map_obj_one_bot.map_cars_dict[car_number].now_point
                    start_point = self.map_obj_one_bot.map_cars_dict[car_number].start_point
                    return_in_base = self.map_obj_one_bot.get_distance(point_1=now_point, point_2=start_point)
                    self.map_obj_one_bot.map_cars_dict[car_number].total_distance += return_in_base
                    logging.info(f"Car-{car_number} gone {now_point} -> Base (END ROUTE) ")
                    del bot[car_number]
            n += 1
        self.fill_info_about_one_bot_work(bot_number)

    def fill_info_about_one_bot_work(self, bot_number: int):
        bot_work_dict = {}
        bot_total_distans = 0
        logging.info(f"\nRESULTS BOT - {bot_number}\n{'#'*100}")
        for index, car in enumerate(self.map_obj_one_bot.map_cars_dict.values()):
            logging.info(f"{car} -> {car.total_distance} -> {car.route_list}")
            bot_total_distans += car.total_distance
            bot_work_dict[index] = {
                "car_distance": car.total_distance,
                'car_route': car.route_list
            }
        bot_work_dict["bot_total_distance"] = bot_total_distans
        self.POPULATION_RESULT[bot_number] = bot_work_dict

    def create_population(self):
        """
        Create one population
        """
        for i in range(self.bot_counts):
            self.POPULATION_DICT[i] = self.create_random_route_for_all_cars_on_map()
            logging.info(f"Create one bot. Number-{i}: {self.POPULATION_DICT[i]}")
        logging.info(f"Create one population: {self.POPULATION_DICT}")

    def create_genetic_population(self, best_population_dict: dict) -> None:
        """
        This method create new population in pre population
        :param best_population_dict: dict with the best results of pre population
        :return: None
        """
        self.POPULATION_DICT = {}
        for i in range(self.bot_counts):
            self.create_routes_for_one_bot_use_genetic(best_population_dict, i)

    def create_routes_for_one_bot_use_genetic(self, best_population_dict: dict, bot_number: int):
        car_route_dict = {}
        for bot in best_population_dict.values():
            # print(bot)
            for car_number, car in bot.items():
                if type(car) == dict:
                    if car_number not in car_route_dict:
                        car_route_dict[car_number] = [car["car_route"]]
                    else:
                        car_route_dict[car_number].append(car["car_route"])
        route_list = self.create_rote_for_one_car_use_genetic(car_route_dict)
        one_bot_dict = {}
        for i, value in enumerate(route_list):
            one_bot_dict[i] = value
        self.POPULATION_DICT[bot_number] = one_bot_dict

    def create_rote_for_one_car_use_genetic(self, cars_dict_with_route: dict):
        # print(cars_dict_with_route)
        route_list = []
        for i in list(self.map_obj.map_points_dict.keys()):
            car_number = 0
            for car in cars_dict_with_route.values():
                # print(f"CHOICE point {i} for all cars")
                # print(f"CHOICE for car: {car_number}")
                one_car = []
                # print(car)
                one_bot_version = random.choice(car)
                if len(route_list) == car_number:
                    one_car.append(one_bot_version[i])
                    route_list.append(one_car)
                else:
                    try:
                        point_number = self.choice_route_point(car, route_list[car_number], i)
                        # print(f"ADD POINT NUMBER -> {point_number}")
                        route_list[car_number].append(point_number)
                    except:
                        self.add_point_if_len_lower(route_list, car_number)
                # print(route_list)
                car_number += 1
        return route_list

    def add_point_if_len_lower(self, route_list, car_number):
        different = list(set(self.map_obj.map_points_dict.keys())-set(route_list[car_number]))
        value = random.choice(different)
        # print(f"VALUE: {value}")
        route_list[car_number].append(value)


    def choice_route_point(self, car: list, inner_list: list, index: int):
        one_bot_version = random.choice(car)
        chance = random.random()
        if chance < self.mut:
            point_number = random.choice(list(self.map_obj.map_points_dict.keys()))
            if point_number in inner_list:
                return self.choice_route_point(car, inner_list, index)
            else:
                return point_number
        if one_bot_version[index] in inner_list:
            return self.choice_route_point(car, inner_list, index)
        else:
            return one_bot_version[index]


    def create_random_route_for_all_cars_on_map(self) -> dict:
        """This method create random route for all cars"""
        bot = {}
        for car_number in self.map_obj.map_cars_dict.keys():
            bot[car_number] = self.create_random_one_car_route()
        return bot

    def create_random_one_car_route(self) -> list:
        """This method create random route for one car"""
        one_car_route = []
        points_numbers = list(self.map_obj.map_points_dict.keys())
        while points_numbers:
            point = random.choice(points_numbers)
            one_car_route.append(point)
            points_numbers.remove(point)
        return one_car_route



if __name__ == '__main__':
    gen = RouteGenetic()
    # gen.create_population()
    # print(gen.POPULATION_DICT)
    # gen.run_one_bot()
    # gen.run_one_population()
    gen.run_genetics()
    # print(gen.POPULATION_RESULT)
