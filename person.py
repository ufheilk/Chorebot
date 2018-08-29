import datetime

class Person:
    time_format = "%H:%M"

    @classmethod
    def from_dict(cls, dict):
        ''' Initializes a chore from a dict '''

        obj = cls()
        for key in dict.keys():
            obj.__dict__[key] = dict[key]

        obj.weekday_messages = datetime.datetime.strptime(obj.weekday_messages,Person.time_format)
        obj.weekend_messages = datetime.datetime.strptime(obj.weekend_messages,Person.time_format)
        obj.chore_done = False

        return obj

    def to_dict(self):
        ''' 
            Returns a custom dictionary representation of the 
            chore, to use to convert the chore to json
        '''
        ret = { self.name : self.failure_count }
        return ret

    def time(self):
        weekday = datetime.datetime.today().day() < 5
        return self.weekday_messages if weekday else self.weekend_messages

    def __str__(self):
        return "[{}: {}]".format(self.name,self.chore)