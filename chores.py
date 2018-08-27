import datetime
import random
import json
from chore_assignments import CHORES_TO_PEOPLE

CHORE_OPTIONS = (
'kitchen','sweeping/mopping','trash','general pickup','recycling'
)

CHORE_FREQUENCIES = {
'kitchen' : datetime.timedelta(1),
'sweeping/mopping' : datetime.timedelta(7),
'trash' : 1,
'general pickup' : 3,
'recycling' : 2
}

def get_random_greeting():
    random_greetings = ["Howdy","Buenas Dias","Sup fuckhead","Hey ballgobbler","Good'day",
                        "Eat my ballsack"]
    return random.choice(random_greetings)


class Chore:

    def update_person(self):
        people = CHORES_TO_PEOPLE[self.person]
        index = people.index(self.person)

        self.person = people[(index + 1) % len(people)]
        
    @classmethod
    def from_dict(cls, dict):
        ''' Initializes a chore from a dict '''

        obj = cls()
        for key in dict.keys():
            obj.__dict__[key] = dict[key]

        obj.__dict__['active'] = obj.next_active_day == datetime.datetime.today()
        
        return obj

    def to_dict(self):
        ''' 
            Returns a custom dictionary representation of the 
            chore, to use to convert the chore to json
        '''
        ret = { 'chore'             :   self.chore,
                'chore_frequency'   :   self.chore_frequency, 
                'next_active_day'   :   self.next_active_day,
                'person'            :   self.person
              }
        return ret

    def active(self):
        return self.active

    def accountability_message(self):
        return "{} is responsible for {} today.".format(self.person,self.chore)

    def chore_message(self):
        return "{} {}, please do your chore: {}".format(get_random_greeting(),self.person,self.chore)

def initialize_chores(filename):
    with open(filename) as f_obj:
        chores = json.load(f_obj)
        return chores

for chore in initialize_chores('chores.json'):
    tmp = Chore.from_dict(chore)
    print(tmp.chore_message())
