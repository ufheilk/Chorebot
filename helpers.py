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

def serialize_people(people,filename):
	with open(filename,'w') as f:
		obj = [person.to_dict() for person in people]
		json.dump(obj,f)

def serialize_chores(chores,filename):
	for chore in chores:
		chore.update_person()
	
	with open(filename,'w') as f:
		obj = [chore.to_dict() for chore in chores]
		json.dump(obj,f)

def get_random_greeting():
    random_greetings = ["Howdy","Buenas Dias","Sup fuckhead","Hey
	ballgobbler","Good'day",'Aloha', 'Suh','Praise Data',
                        "Eat my ballsack","Hi", "Hey", "Ayy", "Ahoy", "Buongiorno", "Hello", "What's up, ATTENTION"]
    return random.choice(random_greetings)

# for each additional time a chore isn't completed, send an angrier message
def anger_message(num_failed):
    anger = '>'*num_failed
    return 'You did not do your chore ' + anger + ':\\'
