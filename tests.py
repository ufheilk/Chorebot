import person

from helpers import initialize_people,serialize_chores
from helpers import serialize_people

people = initialize_people('people.json')
for person in people:
	print(person)

people[0].failure += 3

serialize_people(people,'people.json')
