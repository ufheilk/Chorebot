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
                        "Eat my ballsack","Hi", "Hey", "Ayy", "Ahoy", "Buongiorno", "Hello", "What's up, ATTENTION"]
    return random.choice(random_greetings)

# for each additional time a chore isn't completed, send an angrier message
def anger_message(num_failed):
    anger = '>'*num_failed
    return 'You did not do your chore ' + anger + ':\\'

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
        next_day = self.next_active_day.strftime('%d/%m/%y')
        ret = { 
                'chore'             :   self.chore,
                'chore_frequency'   :   self.chore_frequency, 
                'next_active_day'   :   next_day,
                'person'            :   self.person
              }
        return ret

    def active(self):
        return self.active

    def accountability_msg(self):
        return "{} is responsible for {} today.".format(self.person,self.chore)

    def chore_msg(self):
        return "{} {}, please do your chore: {}".format(get_random_greeting(),self.person,self.chore)

