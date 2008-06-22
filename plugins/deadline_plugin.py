#$ neutron_plugin 01
# -*- coding: UTF-8 -*-

# Author: gelin
#
# This plugin allows the admin to add multiple deadlines (date + message) 
# and display to all how many days remain till deadlines.
# Currently displays in Russian.

import datetime, time

DEADLINES_FILE = 'dynamic/DEADLINES.txt'
DEADLINES = []

def handler_deadline(type, source, parameters):
    global DEADLINES
    message = ''
    for deadline in DEADLINES:
        message += "\n"
        message += _format_deadline(
                deadline['date'] - datetime.date.today(),
                deadline['message'])
    if message == '':
        smsg(type, source, 'No deadlines.')
    else:
        smsg(type, source, message)

def handler_deadline_list(type, source, parameters):
    global DEADLINES
    message = ''
    i = 0
    for deadline in DEADLINES:
        message += "\n"
        message += '% 4i %s %s' % (i, deadline['date'], deadline['message'])
        i += 1
    smsg(type, source, message)

def handler_deadline_delete(type, source, parameters):
    global DEADLINES
    try:
        i = int(parameters)
        del DEADLINES[i]
        _save_deadlines()
        smsg(type, source, 'Removed deadline ' + str(i))
    except Exception, e:
        smsg(type, source, 'Error: ' + str(e))

def handler_deadline_add(type, source, parameters):
    global DEADLINES
    if len(string.split(parameters)) < 2:
        smsg(type, source, 'Invalid Syntax')
        return
    try:
        (sdate, message) = string.split(parameters, maxsplit=1)
        date = _parse_date(sdate)
        add_deadline(date, message)
        smsg(type, source, 'Added new deadline: %s %s' % (date, message))
    except Exception, e:
        smsg(type, source, 'Error: ' + str(e))

def add_deadline(date, message):
    global DEADLINES
    deadline = {}
    deadline['date'] = date
    deadline['message'] = message
    DEADLINES.append(deadline)
    _sort_deadlines()
    _save_deadlines()

def _format_deadline(timedelta, message):
    days = timedelta.days
    if days > 2:
        return message + u' - через ' + str(days - 1) + u' ' + _plural(days - 1, u'день', u'дня', u'дней') + '.'
    if days == 2:
        return message + u' - послезавтра.'
    if days == 1:
        return message + u' - завтра.'
    if days == 0:
        return message + u' - сегодня!'
    if days == -1:
        return message + u' - вчера!!'
    if days == -2:
        return message + u'- позавчера!!!'
    if days < -2:
        return message + u' - давно.'

def _plural(number, form1, form2, form3):
    if number in (11, 12, 13, 14):
        return form3
    else:
        tens = number % 10
        if tens == 1:
            return form1
        elif tens in (2, 3, 4):
            return form2
        else:
            return form3

def _load_deadlines():
    global DEADLINES
    DEADLINES = eval(read_file(DEADLINES_FILE))
    _sort_deadlines()

def _save_deadlines():
    global DEADLINES
    write_file(DEADLINES_FILE, str(DEADLINES))

def _sort_deadlines():
    global DEADLINES
    DEADLINES.sort(_cmp_deadlines)

def _cmp_deadlines(a, b):
    d = cmp(a['date'], b['date'])
    if d == 0:
        return cmp(a['message'], b['message'])
    else:
        return d

def _parse_date(sdate):
    date = time.strptime(sdate, '%Y-%m-%d')
    return datetime.date(date.tm_year, date.tm_mon, date.tm_mday)

initialize_file(DEADLINES_FILE, "[]")
_load_deadlines()

register_command_handler(handler_deadline,
    '!deadline', 0,
    'Displays the number of days till deadline.',
    '!deadline', ['!deadline', '!dl'])
register_command_handler(handler_deadline,
    '!dl', 0,
    'Displays the number of days till deadline.',
    '!dl', ['!deadline', '!dl'])
register_command_handler(handler_deadline_list,
    '!deadline_list', 100,
    'Displays all registered deadlines.',
    '!deadline_list', ['!deadline_list', '!dl_list'])
register_command_handler(handler_deadline_list,
    '!dl_list', 100,
    'Displays all registered deadlines.',
    '!dl_list', ['!deadline_list', '!dl_list'])
register_command_handler(handler_deadline_delete,
    '!deadline_del', 100,
    'Removes deadline with specified ID.',
    '!deadline_del id', ['!deadline_del 0', '!dl_del 5'])
register_command_handler(handler_deadline_delete,
    '!dl_del', 100,
    'Removes deadline with specified ID.',
    '!dl_del id', ['!deadline_del 0', '!dl_del 5'])
register_command_handler(handler_deadline_add,
    '!deadline_add', 100,
    'Adds new deadline.',
    '!deadline_add yyyy-mm-dd message',
    ['!deadline_add 2009-01-01 New Year', '!dl_add 2008-05-09 Victory'])
register_command_handler(handler_deadline_add,
    '!dl_add', 100,
    'Adds new deadline.',
    '!dl_add yyyy-mm-dd message',
    ['!deadline_add 2009-01-01 New Year', '!dl_add 2008-05-09 Victory'])

