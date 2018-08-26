import datetime
import threading

import chores
import person


# sleep until this time
def sleep_until(time):
    pass

# send msg to person after sleeping until time 
def send_message(person, time, msg):
    sleep_until(time)
    # WAKE ME UP (WAKE ME UP INSIDE)
    while True:
        try:
            messager = Messager()
            messager.message(person.address, msg)
        except:
            continue
        break

# First, initialize all Person and Chore objects from files
people = initialize_people('people.json')
chores = initialize_chores('chores.json')

today = datetime.datetime.now()
accountability_msg = ''

for chore in chores:
    chore.check_date(today)
    if chore.active:
        # today's choredoer will be communicated to the others
        accountability_msg += chore.create_msg

for person in people:
    if person.recv_accountability:
        # dispatch a thread to send this message at the desired time
        threading.Thread(target=send_message, args=(person, '10:00PM', accountability_msg).start())
