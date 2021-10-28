# encoding: utf-8

import sys, os
from workflow import Workflow3
from common import *

reminder_autostart = os.getenv('reminder_autostart') or 'true'

def main(wf):

  # init
  history         = fetch_history()
  active_timer    = check_timer()
  query           = None
  if reminder_autostart == 'true': start_reminder()

  # input
  if len(wf.args):
    query               = wf.args[0]
    task, project, note = split_input(query)
    history             = wf.filter(query, history, key=search_friendly, min_score=20)

  # add stop timer
  if active_timer and (len(note)==0 or active_timer==task+project):
    it = wf.add_item(
      title         = u"Stop timer '"+active_timer+u"'",
      subtitle      = note.capitalize(),
      arg           = 'stop',
      autocomplete  = active_timer+u' ',
      valid         = len(note),
      icon          = ''
    )
    if query: it.setvar('wf_input', query)

  # add start timer
  if query and (not active_timer) and (not len(note)): 
    it = wf.add_item(
      title     = u"Start timer '"+task+project+u"'",
      subtitle  = note.capitalize(),
      arg       = 'start',
      valid     = len(task) and len(project[1:]),
      icon      = ''
    )
    it.setvar('wf_input', query)

  # add reg time
  if query and len(note) and active_timer!=task+project:
    it = wf.add_item(
      title         = u"Add 1h for '"+task+project+u"'",
      subtitle      = note.capitalize(),
      arg           = 'reg',
      autocomplete  = task+project+u' ',
      valid         = len(task) and len(project[1:]) and len(note),
      icon          = ''
    )
    it.setvar('wf_input', query)

  # add history items
  for hist in history: 
    task, project, note = split_input(hist)
    wf.add_item(
      title         = task+project,
      subtitle      = '',
      arg           = '',
      autocomplete  = task+project+u' ',
      copytext      = task+project,
      valid         = False,
      icon          = ''
    )

  # return list to alfred
  wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))