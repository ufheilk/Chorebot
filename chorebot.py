import datetime
import random
import time
import threading

import chores
import person
from collection import Messager, Mailbox

def random_dumbass_greeting():
    return random.choice(["Hi", "Hey", "Ayy", "Ahoy", "Buongiorno", "Hello", "What's up, ATTENTION"])

# for each additional time a chore isn't completed, send an angrier message
def anger_message(num_failed):
    anger = '>'*num_failed
    return 'You did not do your chore ' + anger + ':\\'

# sleep until this time
def sleep_until(time):
    pass

# send msg to person immediately
def send_message(person, msg):
    while True:
        try:
            messager = Messager()
            messager.message(person.address, msg)
        except:
            time.sleep(15)
            continue
        break

# wait a little bit before sending msg to person
def send_timed_message(person, msg):
    sleep_until(person.send_time)
    # WAKE ME UP (WAKE ME UP INSIDE)
    send_message(person, msg)

# check chorebot's email account to see who has dared message it
def check_mail(people):
    while True:
        try:
            box = Mailbox(people)
            box.process_mail()
            box.delete_mail()
        except:
            time.sleep(15)
            continue
    break

# First, initialize all Person and Chore objects from files

# people: list of person objects
people = initialize_people('people.json')

# chores: list of chore objects
chores = initialize_chores('chores.json')

today = datetime.datetime.now()
accountability_msg = ''

for chore in chores:
    chore.check_date(today)
    if chore.active:
        # today's choredoer will be communicated to the others
        accountability_msg += chore.accountability_msg()

for person in people:
    if person.recv_accountability:
        # dispatch a thread to send this message at the desired time
        threading.Thread(target=send_timed_message, args=(person, person.time, accountability_msg).start())

# send out the daily chore messages
for chore in chores:
    if chore.active:
        person = chore.person
        msg = chore.chore_msg(random_dumbass_greeting())
        threading.Thread(target=send_timed_message, args=(person, person.time, accountability_msg).start())
    
# chorebot now enters its eternal slumber (until 10, that is)
sleep_until('10:00PM')

check_mail(people)

for person in people:
    if not person.chore_done:
        # sending this slacking peon a reminder
        send_message(person, "Please remember to do your chore")
        

# give these fools a little more time
sleep_until('4:30AM')

check_mail(people)

for person in people:
    if not person.chore_done:
        send_message('

