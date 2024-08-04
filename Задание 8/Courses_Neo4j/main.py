import datetime
import json
import os

from dateutil import relativedelta

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
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher

courses_nodes = []
for course in courses_list:
    n = Node("Course", name=course["name"], duration=course["duration"], date_begin=course["date_begin"],
             date_end=course["date_end"], description=course["description"], lecturer=course["lecturer"],
             price=course["price"])
    courses_nodes.append(n)
attendees_nodes = []
relationships = []
for attendee in attendees_list:
    n = Node("Attendee", name=attendee["name"], birthdate=attendee["birthdate"],
             corporate_client=attendee["corporate_client"], country=attendee["country"], city=attendee["city"],
             phone_number=attendee["phone_number"], online=attendee["online"], wishes=attendee["wishes"])
    attendees_nodes.append(n)
    relationships.append(Relationship(n, "ATTENDS", courses_nodes[attendee["course_id"] - 1]))
graph = Graph(password="SQL_is_better")
graph.delete_all()
tx = graph.begin()
for course_node in courses_nodes:
    tx.create(course_node)
for attendee_node in attendees_nodes:
    tx.create(attendee_node)
for relationship in relationships:
    tx.create(relationship)
graph.commit(tx)
nm = NodeMatcher(graph)
rm = RelationshipMatcher(graph)
print("Задание 1.")
today_without_time = datetime.datetime.fromordinal(datetime.date.today().toordinal())
c_nodes = nm.match("Course")
for c_node in c_nodes:
    r_nodes = RelationshipMatcher(graph).match((None, c_node), "ATTENDS")
    a_nodes_age = 0.0
    for r_node in r_nodes:
        a_nodes_age += relativedelta.relativedelta(today_without_time, r_node.start_node["birthdate"].to_native()).years
    a_nodes_age /= len(r_nodes)
    print(c_node["name"] + ": " + str(a_nodes_age) + ".")
print("Задание 2.")
b = False
for c_node in c_nodes:
    r_nodes = RelationshipMatcher(graph).match((None, c_node), "ATTENDS")
    a_nodes_noncorp_count = 0
    for r_node in r_nodes:
        if not r_node.start_node["corporate_client"]:
            a_nodes_noncorp_count += 1
    f = a_nodes_noncorp_count / len(r_nodes) * 100
    if f > 50:
        print(c_node["name"] + ": " + str(f))
        b = True
if not b:
    print("Таких курсов нет.")
print("Задание 3.")
b = False
for c_node in c_nodes:
    if today_without_time > c_node["date_end"]:
        print(c_node["name"] + ": " + str(c_node["date_end"]) + ".")
        b = True
if not b:
    print("Таких курсов нет.")
print("Задание 4.")
b = False
for c_node in c_nodes:
    if today_without_time < c_node["date_begin"]:
        r_nodes = RelationshipMatcher(graph).match((None, c_node), "ATTENDS")
        print(c_node["name"] + ": " + str(len(r_nodes) + "."))
        b = True
if not b:
    print("Таких курсов нет.")
print("Задание 5.")
f = 0
for c_node in c_nodes:
    if today_without_time > c_node["date_end"] or today_without_time < c_node["date_begin"]:
        f += c_node["price"]
print("Полная прибыль: " + str(f) + ".")
