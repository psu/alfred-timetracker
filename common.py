# encoding: utf-8

import sys, re, os, time
from workflow import web, Workflow3
from workflow.background import run_in_background
from datetime import datetime

ifttt_event         = os.getenv('ifttt_event')
ifttt_key           = os.getenv('ifttt_key')
reminder_autostart  = os.getenv('reminder_autostart') or 'true'
workhours_begin     = os.getenv('workhours_begin') or '08:30'
workhours_end       = os.getenv('workhours_end') or '18:00'
reminder_interval   = os.getenv('reminder_interval') or '15'
default_length      = os.getenv('default_length') or '60'
wf                  = Workflow3()

def check_workhours():
  begin_h, begin_m  = workhours_begin.split(':')
  end_h, end_m      = workhours_end.split(':')
  now               = datetime.now()
  begin             = now.replace(hour=int(begin_h), minute=int(begin_m))
  end               = now.replace(hour=int(end_h), minute=int(end_m))
  day               = datetime.datetime.today().weekday()
  weekdays          = False
  if day < 5: weekdays = True
  return (begin <= now <= end) and weekdays

def calc_interval():
  return int(reminder_interval) * 60

def start_reminder():
  active_reminder = wf.stored_data('active_reminder')
  active_timer = wf.stored_data('active_timer')
  if not active_reminder: wf.store_data('active_reminder', unix_timestamp())
  if not active_timer and active_reminder <= (unix_timestamp() - calc_interval()):
    run_in_background('reminder'+str(unix_timestamp()), ['/usr/bin/python', wf.workflowfile('reminder.py')])
    wf.store_data('active_reminder', unix_timestamp())

def unix_timestamp():
  return int( time.mktime( datetime.now().timetuple() ) )

def date_from_timestamp(timestamp):
  return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")

def closest_quarter(timestamp):
  return int( 900.0 * round(timestamp/900.0) )

def output_string(task, project, note):
  return note.capitalize()+u' - '+task.lower()+project.lower()

def start_timer(task, project):
  wf.store_data('active_timer', task+project)
  wf.store_data('start_timestamp', unix_timestamp())

def stop_timer(task, project, note):
  start = wf.stored_data('start_timestamp')
  end = unix_timestamp()
  duration = closest_quarter(end - start)
  if duration < 1800: duration = 1800
  end = closest_quarter(end)
  trigger_ifttt(output_string(task, project, note),
                date_from_timestamp(end-duration),
                date_from_timestamp(end))
  save_history(task, project)
  wf.store_data('active_timer', None)
  wf.store_data('start_timestamp', None)
  if reminder_autostart == 'true': start_reminder()

def check_timer():
  return wf.stored_data('active_timer')

def reg_timer(task, project, note):
  end = closest_quarter(unix_timestamp())
  trigger_ifttt(output_string(task, project, note),
                date_from_timestamp(end-int(default_length)*60),
                date_from_timestamp(end))
  save_history(task, project)

def search_friendly(str):
  return re.sub(u'[^a-zA-ZåäöÅÄÖ@]+', u' ', str)

def split_input(input):
  project = task = note = u''
  if '@' in input:
    split   = re.match(u'(.*)\s*(@\w*)\s*(.*)', input)
    task    = split.group(1)
    project = split.group(2)
    note    = split.group(3)
  else:
    task = input
  return task, project, note

def fetch_history():
  history = wf.stored_data('history') or []
  return history

def save_history(task, project):
  if len(task) and len(project[1:]):
    task    = task.lower()
    project = project.lower()
    hist    = task+project
    history = fetch_history()
    if hist not in history:
      history.append(hist)
      wf.store_data('history', history)

def trigger_ifttt(value1, value2, value3):
  json={}
  json['value1'] = value1
  json['value2'] = value2
  json['value3'] = value3
  url = ('https://maker.ifttt.com/trigger/' +
        ifttt_event + 
        '/with/key/' + 
        ifttt_key)
  response = web.post(url, data=json)
  response.raise_for_status()  

if __name__ == u"__main__":
    sys.exit(0)