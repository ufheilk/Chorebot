import datetime	
class Person:
	
	def __init__(self):
		self.name = name
		self.phone_email = phone_email
		self.chore = chore
		self.chore_index = chore_index

		''' As of time of writing, I don't think we need this field '''
		# self.date_to_complete = datetime.datetime.today()

		self.reminder = True
		self.completed = False
		self.weekday_messages = ''
		self.weekend_messages = ''
	
	def get_message_time(self):
		today = datetime.datetime.today()
		return self.weekday_messages if today.weekday() < 5 else self.weekend_messages
