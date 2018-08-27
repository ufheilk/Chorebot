import datetime

class Person:
    @classmethod
    def from_dict(cls, dict):
        ''' Initializes a chore from a dict '''

        obj = cls()
        for key in dict.keys():
            obj.__dict__[key] = dict[key]

        print(obj.__dict__)

        obj.failure = int(obj.failure)
        obj.weekday_messages = datetime.datetime.strptime(obj.weekday_messages,'%H:%M')
        obj.weekend_messages = datetime.datetime.strptime(obj.weekend_messages,'%H:%M')

		obj.chore_done = False

        return obj

    def to_dict(self):
        ''' 
            Returns a custom dictionary representation of the 
            chore, to use to convert the chore to json
        '''
        weekday_messages = self.weekday_messages.strftime('%H:%M')
        weekend_messages = self.weekend_messages.strftime('%H:%M')
        ret = { 'name'             :   self.name,
                'chore'   :   self.chore, 
				'address' : self.address,
				'failure'	: self.failure,
				'recv_accountability' : self.recv_accountability,
				'reminder' : self.reminder,
				'weekday_messages' : weekday_messages,
				'weekend_messages' : weekend_messages
              }
        return ret

