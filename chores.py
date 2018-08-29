import datetime
import random
import json
from chore_assignments import CHORES_TO_PEOPLE

from helpers import get_random_greeting

CHORE_OPTIONS = (
'kitchen','sweeping/mopping','trash','general pickup','recycling'
)

CHORE_FREQUENCIES = {
'kitchen' : datetime.timedelta(days=1),
'sweeping/mopping' : datetime.timedelta(days=7),
'trash' : datetime.timedelta(days=1),
'general pickup' : datetime.timedelta(days=3),
'recycling' : datetime.timedelta(days=2)
}

class Chore:

    def update_person(self):
        people = CHORES_TO_PEOPLE[self.person]
        index = people.index(self.person)

        self.person = people[(index + 1) % len(people)]
	
	def update_date(self):
		if self.active:
			self.next_active_day += CHORE_FREQUENCIES[self.chore]
	
	def update_chore(self):
		self.update_person()
		self.update_date()
        
    @classmethod
    def from_dict(cls, dict):
        ''' Initializes a chore from a dict '''

        obj = cls()
        for key in dict.keys():
            obj.__dict__[key] = dict[key]
		obj.__dict__['next_active_day'] = datetime.datetime.strptime(obj['next_active_day'],"%m/%d/%Y")
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

    def accountability_msg(self):
        return "{} is responsible for {} today.".format(self.person,self.chore)

    def chore_msg(self):
        return "{} {}, please do your chore: {}".format(get_random_greeting(),self.person,self.chore)

