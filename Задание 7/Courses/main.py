import datetime
import json
import os

import pymongo

import courses

if not os.path.isfile("courses_list.json") or not os.path.isfile("attendees_list.json"):
    courses_list, attendees_list = courses.generate_courses_list()
    print("Сгенерированы новые списки курсов и их посетителей.")
else:
    f = open("courses_list.json", "r")
    courses_list = json.load(f)
    f.close()
    f = open("attendees_list.json", "r")
    attendees_list = json.load(f)
    f.close()
    print("Списки курсов и их посетителей загружены из JSON-файлов.")
for i, course in enumerate(courses_list):
    courses_list[i]["date_begin"] = datetime.datetime.strptime(course["date_begin"], "%Y-%m-%d")
    courses_list[i]["date_end"] = datetime.datetime.strptime(course["date_end"], "%Y-%m-%d")
for i, attendee in enumerate(attendees_list):
    attendees_list[i]["birthdate"] = datetime.datetime.strptime(attendee["birthdate"], "%Y-%m-%d")
print("Количество курсов: " + str(len(courses_list)) + ".")
print("Количество посетителей курсов: " + str(len(attendees_list)) + ".")
client = pymongo.MongoClient("localhost", 27017)
db = client["CoursesDB"]
courses_collection = db["Courses"]
courses_collection.drop()
courses_collection.insert_many(courses_list)
print("Данные о курсах добавлены в коллекцию Courses.")
del courses_list
attendees_collection = db["Attendees"]
attendees_collection.drop()
attendees_collection.insert_many(attendees_list)
print("Данные о посетителях курсов добавлены в коллекцию Attendees.")
del attendees_list
print("Задание 1.")
stage_lookup_attendees = {
    "$lookup": {"from": "Attendees", "localField": "_id", "foreignField": "course_id", "as": "related_attendees"}}
stage_sum_age_attendees = {"$reduce": {"input": "$related_attendees.birthdate", "initialValue": "", "in": {
    "$sum": [{"$subtract": [{"$year": "$$NOW"}, {"$year": "$$this"}]}, "$$value"]}}}
stage_add_attendees_avg_age = {
    "$addFields": {"avg_age": {"$divide": [stage_sum_age_attendees, {"$size": "$related_attendees.birthdate"}]}}}
pipeline = [stage_lookup_attendees, stage_add_attendees_avg_age]
results = courses_collection.aggregate(pipeline)
for course in results:
    print(course["name"] + ": " + str(course["avg_age"]) + ".")
print("Задание 2.")
stage_sum_corp_attendees = {"$reduce": {"input": "$related_attendees.corporate_client", "initialValue": "",
                                        "in": {"$sum": ["$$value", {"$toInt": "$$this"}]}}}
stage_perc_noncorp_attendees = {"$subtract": [100, {
    "$multiply": [{"$divide": [stage_sum_corp_attendees, {"$size": "$related_attendees.corporate_client"}]}, 100]}]}
stage_add_corp_attendees_count = {"$addFields": {"corp_clients": stage_sum_corp_attendees}}
stage_add_non_corp_attendees_perc = {"$addFields": {"noncorp_clients_perc": stage_perc_noncorp_attendees}}
stage_match_non_corp_perc_over50 = {"$match": {"noncorp_clients_perc": {"$gt": 50}}}
pipeline = [stage_lookup_attendees, stage_add_corp_attendees_count, stage_add_non_corp_attendees_perc,
            stage_match_non_corp_perc_over50]
k = 0
results = courses_collection.aggregate(pipeline)
for course in results:
    print(course["name"] + ": " + str(course["noncorp_clients_perc"]) + ".")
    k += 1
if k < 1:
    print("Таких курсов нет.")
print("Задание 3.")
today_without_time = datetime.datetime.fromordinal(datetime.date.today().toordinal())
print("Полночь сегодня: " + str(today_without_time) + ".")
stage_match_course_ended = {"$match": {"date_end": {"$lt": today_without_time}}}
pipeline = [stage_match_course_ended]
results = courses_collection.aggregate(pipeline)
k = 0
for course in results:
    print(course["name"] + ": " + str(course["date_end"]) + ".")
    k += 1
if k < 1:
    print("Таких курсов нет.")
print("Задание 4.")
stage_add_count_attendees = {"$addFields": {"attendees_amount": {"$size": "$related_attendees"}}}
stage_match_course_future = {"$match": {"date_begin": {"$gt": today_without_time}}}
pipeline = [stage_lookup_attendees, stage_add_count_attendees, stage_match_course_future]
results = courses_collection.aggregate(pipeline)
k = 0
for course in results:
    print(course["name"] + ": " + str(course["attendees_amount"]) + ".")
    k += 1
if k < 1:
    print("Таких курсов нет.")
print("Задание 5.")
stage_match_course_ended_or_current = {
    "$match": {"$or": [{"date_end": {"$lt": today_without_time}}, {"date_start": {"$lt": today_without_time}}]}}
stage_group_sum_price = {"$group": {"_id": -1, "total_price": {"$sum": "$price"}}}
pipeline = [stage_match_course_ended_or_current, stage_group_sum_price]
results = courses_collection.aggregate(pipeline)
for result in results:
    print("Полная прибыль: " + str(result["total_price"]) + ".")
