import datetime
import random
import time
import threading

import chores
import person
from collection import Messager, Mailbox

from helpers import anger_message,initialize_chores,initialize_people

from credentials import credentials

# sleep until this time
def sleep_until(time):
    if type(time) is str:
        time = datetime.datetime.strptime('%H:%M')
    diff = time - datetime.datetime.now()
    time.sleep(diff)

# send msg to person immediately
def send_message(person, msg):
    while True:
        try:
            messager = Messager()

            # i included a field for 
            messager.message(person.address, msg)
        except:
            time.sleep(15)
            continue
        break

# wait a little bit before sending msg to person
def send_timed_message(person, msg):
    sleep_until(person.time())
    # WAKE ME UP (WAKE ME UP INSIDE)
    send_message(person, msg)

# check chorebot's email account to see who has dared message it
def check_mail(people):
    # why does this method have a loop?
    # won't this stall our program?
    while True:
        try:
            box = Mailbox(people,credentials.email,credentials.password)
            box.process_mail()
            box.delete_mail()
        except:
            time.sleep(15)
            continue
        break

# First, initialize all Person and Chore objects from files

# people: list of person objects
people = initialize_people()

# chores: list of chore objects
chores = initialize_chores()

today = datetime.datetime.now()
accountability_msg = ''

for chore in chores:
    if chore.active:
        # today's choredoer will be communicated to the others
        accountability_msg += chore.accountability_msg()

for person in people:
    if person.recv_accountability:
        # dispatch a thread to send this message at the desired time
        threading.Thread(target=send_timed_message, args=(person, accountability_msg).start())

# send out the daily chore messages
for chore in chores:
    if chore.active:
        person = chore.person
        msg = chore.chore_msg()
        threading.Thread(target=send_timed_message, args=(person, accountability_msg).start())
    
# chorebot now enters its eternal slumber (until 10, that is)
sleep_until('22:00')

check_mail(people)

for person in people:
    if not person.chore_done:
        # sending this slacking peon a reminder
        send_message(person, "Please remember to do your chore")
        

# give these fools a little more time
sleep_until('04:30')

check_mail(people)

for person in people:
    if not person.chore_done:
        # commence scolding
        send_message(person, anger_message(person.failure))
        person.failure += 1

# serialize everything to a file
serialize_people(people)
serialize_chores(chores)
