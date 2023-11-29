from objects import Cargo, Point, Cars, GeoMap


def create_map_object():
    # init points
    start_point = Point("Start point", 56.30973137511247, 54.89990171769366)
    perm = Point("Perm", 58.006207, 56.222767)
    chaykovskiy = Point("Chaykovskiy", 56.769138, 54.142214)
    izhevsk = Point("Izhevsk", 56.85485383594858, 53.233765237414126)
    kungur = Point("Kungur", 57.429283985832704, 56.9579566557034)
    sverdlovsk = Point("Sverdlovsk", 56.81961798026259, 60.59034893753525)
    kazan = Point("Kazan", 55.79921749411797, 49.1320310633986)
    points_list = [perm, chaykovskiy, izhevsk, kungur, sverdlovsk, kazan]

    # init cars
    car_1 = Cars(name="Car_1", max_cargo=2000, start_point=start_point)
    car_2 = Cars(name="Car_2", max_cargo=2000, start_point=start_point)
    car_3 = Cars(name="Car_3", max_cargo=2000, start_point=start_point)
    cars_list = [car_1, car_2, car_3]

    # init cargos
    cargo_1 = Cargo("Banana")
    cargo_2 = Cargo("Armor")
    cargo_3 = Cargo("Computer")
    cargo_4 = Cargo("Bread")
    cargo_5 = Cargo("Milk")
    cargo_6 = Cargo("Chocolate")
    cargo_7 = Cargo("Weapon")
    cargo_8 = Cargo("Clothes")
    cargo_9 = Cargo("Colors")
    cargo_10 = Cargo("Shoes")
    cargo_11 = Cargo("Water")
    cargo_12 = Cargo("Arbuz")

    # add cargos in points
    perm_cargo = [
        (cargo_1, 200), # 200
        (cargo_2, 100), # 100
        (cargo_3, 100), # 200
        (cargo_4, 100), # 100
        (cargo_5, 200), # 200
        (cargo_6, 200)  # 200
    ]
    chaykovskiy_cargo = [
        (cargo_1, 100), # 300
        (cargo_2, 100), # 300
        (cargo_3, 100), # 300
        (cargo_4, 100), # 200
        (cargo_5, 200), # 400
        (cargo_6, 200), # 400
    ]
    izhevsk_cargo = [
        (cargo_1, 200), # full
        (cargo_2, 200), # 400
        (cargo_3, 200), # 400
        (cargo_4, 200), # 400
        (cargo_5, 100), # full
        (cargo_6, 100), # full
    ]
    kungur_cargo = [
        (cargo_2, 100), # full
        (cargo_3, 100), # full
        (cargo_4, 100), # full
        (cargo_7, 200), # 200
        (cargo_8, 200), # 200
        (cargo_9, 200), # 200
        (cargo_10, 100), # 100
    ]
    sverdlovsk_cargo = [
        (cargo_7, 200), # 400
        (cargo_8, 100), # 300
        (cargo_9, 100), # 300
        (cargo_10, 200), # 300
        (cargo_11, 200), # 200
        (cargo_12, 200), # 200
    ]
    kazan_cargo = [
        (cargo_7, 100), # full
        (cargo_8, 200), # full
        (cargo_9, 200), # full
        (cargo_10, 200), # full
        (cargo_11, 300), # full
        (cargo_12, 300), # full
    ]

    # add cargos in the car
    car_1_cargo = [
        (cargo_1, 500),
        (cargo_2, 500),
        (cargo_3, 500),
        (cargo_4, 500)
    ]
    car_2_cargo = [
        (cargo_5, 500),
        (cargo_6, 500),
        (cargo_7, 500),
        (cargo_8, 500)
    ]
    car_3_cargo = [
        (cargo_9, 500),
        (cargo_10, 500),
        (cargo_11, 500),
        (cargo_12, 500)
    ]

    # add cargos in points
    perm.add_cargos_list_in_dict(perm_cargo)
    chaykovskiy.add_cargos_list_in_dict(chaykovskiy_cargo)
    izhevsk.add_cargos_list_in_dict(izhevsk_cargo)
    sverdlovsk.add_cargos_list_in_dict(sverdlovsk_cargo)
    kungur.add_cargos_list_in_dict(kungur_cargo)
    kazan.add_cargos_list_in_dict(kazan_cargo)

    # add cargos in cars
    car_1.add_cargo_list_in_dict(car_1_cargo)
    car_2.add_cargo_list_in_dict(car_2_cargo)
    car_3.add_cargo_list_in_dict(car_3_cargo)


    map_object = GeoMap()
    map_dict = map_object.add_points_on_map(points_list)
    car_dict = map_object.add_cars_on_map(cars_list)
    return map_object

# def create_map_object():
#     map_object = GeoMap()
#     car_1.add_cargo_list_in_dict(car_1_cargo)
#     car_2.add_cargo_list_in_dict(car_2_cargo)
#     car_3.add_cargo_list_in_dict(car_3_cargo)
#     perm.add_cargos_list_in_dict(perm_cargo)
#     chaykovskiy.add_cargos_list_in_dict(chaykovskiy_cargo)
#     izhevsk.add_cargos_list_in_dict(izhevsk_cargo)
#     sverdlovsk.add_cargos_list_in_dict(sverdlovsk_cargo)
#     kungur.add_cargos_list_in_dict(kungur_cargo)
#     kazan.add_cargos_list_in_dict(kazan_cargo)
#     map_dict = map_object.add_points_on_map(points_list)
#     car_dict = map_object.add_cars_on_map(cars_list)
#     return map_object

if __name__ == '__main__':
    tmp_dict = {
        cargo_1: 0,
        cargo_2: 0,
        cargo_3: 0,
        cargo_4: 0,
        cargo_5: 0,
        cargo_6: 0,
        cargo_7: 0,
        cargo_8: 0,
        cargo_9: 0,
        cargo_10: 0,
        cargo_11: 0,
        cargo_12: 0,
    }

