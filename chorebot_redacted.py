import smtplib
import imaplib
import time
import random
import email
import socket
from email.mime.text import MIMEText
from datetime import timedelta, datetime

socket.setdefaulttimeout(1000000) # defense against vunet's quality

MY_PHONE = "r" # for ease-of-use

# the number of days between when a person will do this chore
chores = {"recycling": timedelta(days=4), "kitchen": timedelta(days=5), "sweeping": timedelta(days=4),
          "clean table": timedelta(days=5)}

dumbass_greeting = ["Hi", "Hey", "Ayy", "Ahoy", "Buon giorno", "Hello", "What's up"]

#number of people assigned to a particular chore
num_per_chore = {"recycling": 2, "kitchen": 5, "sweeping": 2, "clean table": 1}

#this is the most disgusting data structure that has ever existed
#[0] is name. [1] is phone email. [2] is chore and index into set of people who have that chore.
#[3] is the time at which the need to be told to do the chore. [4] is whether they have set a reminder,
#and when that reminder should be. [5] is if they have already done the chore (the X thing)
#[6] is their preferred weekday reminder (in hours and minutes). [7] is their preferred weekend reminder
#(in hours and minutes).
people = [["K", "", ["kitchen", 0], datetime.today(), [False, 0], False, [16,0], [20,0]],
          ["J", "", ["sweeping", 1], datetime.today(), [False, 0], False, [10,0], [12,0]],
          ["R", "", ["kitchen", 1], datetime.today(), [False, 0], False, [9,0], [12,0]],
          ["N", "7", ["clean table", 0], datetime.today(), [False, 0], False, [9,0], [12,0]],
          ["L", "9787603833@vzwpix.com", ["sweeping", 0], datetime.today(), [False, 0], False, [17,0], [12,0]],
          ["A", "", ["kitchen", 2], datetime.today(), [False, 0], False, [11,0], [13,0]],
          ["B", "", ["kitchen", 3], datetime.today(), [False, 0], False, [9,0], [12, 0]],
          ["J", "", ["recycling", 0], datetime.today(), [False, 0], False, [20,0], [15,0]],
          ["N", "", ["recycling", 1], datetime.today(), [False, 0], False, [22,0], [20,0]],
          ["E", "", ["kitchen", 4], datetime.today(), [False, 0], False, [10,0], [12,0]]]


CHOREBOT_ADDRESS = "m"
CHOREBOT_PASSWORD = "nice try im not going to put this info on github" # nobody can hack chore bot with this unnecessarily long password

SMTP_CONNECTION = smtplib.SMTP(host='smtp.gmail.com', port=587, timeout=1000000)

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993
MAIL = imaplib.IMAP4_SSL(SMTP_SERVER)

chorebot_functionality_info_1 = "Hey, i am chorebot, an automated system designed to schedule chore stuff." \
                                " On the day you are supposed to do your chore, chorebot will tell you. Any other day" \
                                " you do not have to do your chore."
chorebot_functionality_info_2 = "The groups of people working each chore have their days that they do the chore staggered" \
                                " so that every day (or every other day) the chore is being done. For this reason it is" \
                                " imperative that you do your chore on the day told (by chorebot)"
chorebot_functionality_info_3 = "To aid you in doing this chorebot has some extra features. When you receive a notification" \
                                " from chorebot to do your chore, you can text back with a number (IN HOURS) so that" \
                                " chorebot will remind you to do your chore after that amount of time. The number can be a" \
                                " decimal, so e.g. 6.5 is 6 and a half hours before the reminder."
chorebot_functionality_info_4 = "While you can technically set your reminder for a whole day ahead, please do not do this" \
                                " because then you are doing the chore on the wrong day. Also please do not try to break" \
                                " chorebot, because you probably can. Chorebot is fragile and poorly coded and weird input" \
                                " may cause chorebot to have a meltdown, then explode."
chorebot_functionality_info_5 = "Finally, if you have already done your chore (on the day you are supposed to do it, see above)" \
                                " and do not want to be pestered by chorebot, you can text an X (or x) to chorebot. Then you" \
                                " won't get a notification until the next day you are supposed to do this chore. You can't spam" \
                                " X to chorebot to never get a notification."


def send_functionality_messages(person):
    send(person[1], chorebot_functionality_info_1, "WELCOME TO CHOREBOT")
    send(person[1], chorebot_functionality_info_2)
    send(person[1], chorebot_functionality_info_3)
    send(person[1], chorebot_functionality_info_4)
    send(person[1], chorebot_functionality_info_5)


def get_latest_email():
    print 'in get_latest_email'
    try:

		# select inbox
        MAIL.select('inbox')
        garbage, data = MAIL.search(None, 'ALL')

		# get most recent
        mail_ids = data[0]
        id_list = mail_ids.split()
        if len(id_list) == 0:
            print 'no emails found'
            return None
        else:
            return int(id_list[-1])
    except OSError:
        print 'exception caught in get_latest_email'
        pass # if the socket times out, just do nothing the issue will probably resolve itself


def send(to_address, message_txt, subject_txt=""):
    msg = MIMEText(message_txt)
    msg['From'] = CHOREBOT_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject_txt
    SMTP_CONNECTION.sendmail(CHOREBOT_ADDRESS, to_address, msg.as_string())


# this function returns the body of the most recent email in the inbox
def get_message(message_id):
    type, data = MAIL.fetch(message_id, '(RFC822)')
    message_body = data[0][1]
    start = message_body.find('<td>')
    end = message_body.find('</td>')
    body_txt = message_body[start+4:end].strip() # +4 to get rid of initial <td>
    email_message = email.message_from_string(message_body)
    sender = email_message['From']
    return sender, body_txt


# takes the message to delete, then deletes it (technically moved to trash in gmail)
def delete_message(message_id):
    MAIL.store(message_id, '+FLAGS', r'\Deleted')
    MAIL.expunge()


def time_for_ping(time_to_ping):
    print time_to_ping
    return datetime.today() > time_to_ping


def time_for_reminder(time_to_remind):
    print time_to_remind
    return datetime.today() > time_to_remind


def is_number(potential_number):
    try:
        float(potential_number)
        if float(potential_number) > 0:
            return True
        else:
            return False
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(potential_number)
        return True
    except (TypeError, ValueError):
        pass
    return False


# is this day a weekday?
def is_weekday(day):
    return day.weekday() < 5


# stagger chore start times
def setup_chore_times():
    tomorrow = datetime.today() + timedelta(days=1)
    for person in people:
        # the person will start their chore tomorrow staggered by how many people are doing the chore
        person[3] = tomorrow + (chores[person[2][0]]*person[2][1]/num_per_chore[person[2][0]])
        person[3] = preferred_time(person) # factor in the person's preferred weekend / weekday time


# changes the chore time of the person wrt their preferred time and if it is the weekend or a weekday
def preferred_time(person):
    if is_weekday(person[3]):
        person[3] = person[3].replace(hour=person[6][0], minute=person[6][1], second=0, microsecond=0) # modify date on this copy of person
        return person[3]
    else:
        person[3] = person[3].replace(hour=person[7][0], minute=person[7][1], second=0, microsecond=0)
        return person[3]


def random_dumbass_greeting():
    return dumbass_greeting[random.randrange(0, len(dumbass_greeting))]


MAIL.login(CHOREBOT_ADDRESS, CHOREBOT_PASSWORD)
MAIL.select('inbox') # only want to deal with inbox
SMTP_CONNECTION.starttls()
SMTP_CONNECTION.login(CHOREBOT_ADDRESS, CHOREBOT_PASSWORD)

setup_chore_times()

# tell everyone the chorebot features
#for person in people:
#    send_functionality_messages(person)

for person in people:
    print person[3]

time.sleep(500)

while True:
    for person in people:
        if time_for_ping(person[3]):
            send(person[1], random_dumbass_greeting() + " " + person[0] + ". Please do your chore, " + person[2][0])
            person[3] += chores[person[2][0]] # must update new ping time
            person[3] = preferred_time(person)
            person[5] = False # this person can hit X again

        # checks if a secondary reminder ping has been set
        if person[4][0]:
            if time_for_reminder(person[4][1]):
                send(person[1], person[0] + " please do your chore", "Reminder")
                # must reset the reminder options
                person[4][0] = False

        print 'about to get latest email'
        latest_message_id = get_latest_email()
        if latest_message_id is not None:
            # if there is at least 1 email in the inbox
            latest_email_info = get_message(latest_message_id)
            if latest_email_info[0] == person[1]:
                # the most recent email was sent by this person
                if is_number(latest_email_info[1]):
                    # this person emailed chorebot with a number
                    minutes_to_remind = float(latest_email_info[1])
                    # if the reminder would be after next main ping, ignore
                    if datetime.today() + timedelta(minutes=minutes_to_remind) < person[3]:
                        person[4][0] = True # there is now a secondary reminder
                        person[4][1] = datetime.today() + timedelta(minutes=minutes_to_remind)
                else:
                    # the email was from this person, but was not a reminder time. get rid of it
                    # also must check (with person[5] that this person has not sent X recently
                    # so the cannot abuse the system
                    if latest_email_info[1].lower() == 'x' and not person[5]:
                        # reset the main ping counter and reminder counter
                        person[3] += chores[person[2][0]]
                        person[3] = preferred_time(person)
                        person[4][0] = False
                        person[5] = True
            delete_message(latest_message_id)
        time.sleep(1)


SMTP_CONNECTION.quit()
