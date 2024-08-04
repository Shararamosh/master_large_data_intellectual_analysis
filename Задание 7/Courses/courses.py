import datetime
import json

import numpy as np
from faker import Faker


def generate_courses_list():
    '''
    Функция для генерации списка курсов и пользователей и сохранения в виде JSON-файлов.
    :return: courses_list - список со словарями курсов, attendees_list - список со словарями пользователей.
    '''
    np_seed = 73
    np.random.seed(np_seed)
    date_start = datetime.date(2023, 2, 6)
    date_finish = datetime.date(2023, 6, 5)
    num_courses = 5
    num_attendees = 50
    courses_list = []
    faker_inst = Faker()
    faker_inst.seed_locale("en_US", 73)
    for i in range(num_courses):
        d1 = faker_inst.date_between(start_date=date_start, end_date=date_finish)
        d2 = faker_inst.date_between(start_date=d1, end_date=date_finish)
        dict_obj = {"_id": i + 1, "name": "Course #" + str(i + 1), "duration": np.random.randint(3, 13) * 10,
                    "date_begin": d1.isoformat(), "date_end": d2.isoformat(),
                    "description": "Course #" + str(i + 1) + " description.", "lecturer": faker_inst.unique.name(),
                    "price": np.random.randint(2, 9) * 10000}
        courses_list.append(dict_obj)
    with open("courses_list.json", "w") as courses_list_file:
        json.dump(courses_list, courses_list_file)
        courses_list_file.close()
    attendees_list = []
    for i in range(num_attendees):
        d = faker_inst.date_between(start_date=datetime.date(1990, 1, 1),
                                    end_date=datetime.date(2010, 12, 31)).isoformat()
        dict_obj = {"_id": i + 1, "course_id": np.random.randint(1, num_courses + 1), "name": faker_inst.unique.name(),
                    "birthdate": d, "corporate_client": bool(np.random.randint(0, 2))}
        country_name = faker_inst.country()
        dict_obj["country"] = country_name
        dict_obj["city"] = faker_inst.city()
        dict_obj["phone_number"] = faker_inst.unique.msisdn()
        dict_obj["online"] = bool(np.random.randint(0, 2))
        dict_obj["wishes"] = "Wishes for " + str(dict_obj["name"] + ".")
        attendees_list.append(dict_obj)
    with open("attendees_list.json", "w") as attendees_list_file:
        json.dump(attendees_list, attendees_list_file)
        attendees_list_file.close()
    return courses_list, attendees_list
