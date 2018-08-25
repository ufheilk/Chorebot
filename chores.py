import datetime

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

class Chore:

    def __init__(self, chore,person):
        self.chore = chore
        self.chore_frequency = CHORE_FREQUENCIES[self.chore]
        self.person = person

        self.next_active_day = datetime.datetime.today()

    def active(self):
        return self.next_active_day == datetime.datetime.today()
