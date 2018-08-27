import person,chores
import json

def initialize_chores(filename):
    with open(filename) as f_obj:
        chores = json.load(f_obj)
        return [chores.Chore.from_dict(chore) for chore in chores]

def initialize_people(filename):
    with open(filename) as f_obj:
        people = json.load(f_obj)
        return [person.Person.from_dict(item) for item in people]

import datetime
tmp = {'date' : str(datetime.datetime.now())}

person = initialize_people('people.json')
print(person[0].to_dict())
