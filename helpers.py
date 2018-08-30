from person import Person
from chores import Chore
import json

import random

def initialize_chores():
	with open('chores.json') as f_obj:
		chores = json.load(f_obj)
		return [Chore.from_dict(chore) for chore in chores]

def initialize_people():
	# get person metadata
	try:
		with open('people_config.json') as f_obj:
			meta_data = json.load(f_obj)
	except FileNotFoundError:
		print('Could not open ' + 'people_config')
		exit()

	try:
		with open('failure_count.json') as f_obj:
			chores = json.load(f_obj)
	except FileNotFoundError:
		print('Could not open ' + 'failure_count.json')
		exit()

	# we have a chores object and a count of the times they have failed
	people = []
	for person in meta_data:
		tmp = Person.from_dict(person)
		tmp.__dict__['failure_count'] = chores[tmp.name]
		people.append(tmp)
	
	return people

def serialize_people(people):
	with open('failure_count.json','w') as f:
		obj = {person.name : person.failure_count for person in people}
		json.dump(obj,f)

def serialize_chores(chores):
	for chore in chores:
		chore.update_person()
	
	with open('chores.json','w') as f:
		obj = [chore.to_dict() for chore in chores]
		json.dump(obj,f)


# for each additional time a chore isn't completed, send an angrier message
def anger_message(num_failed):
    anger = '>'*num_failed
    return 'You did not do your chore ' + anger + ':\\'
