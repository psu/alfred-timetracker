# encoding: utf-8

import sys
from workflow import Workflow3, Variables
from common import *

def main(wf):

  history = fetch_history()
  active_timer = check_timer()

  query = None
  if len(wf.args):
    query = wf.args[0]

  if not query and active_timer:
    # add incomplete stop item
    wf.add_item(title=u'.Stop timer',
                subtitle=active_timer,
                arg='',
                autocomplete=active_timer+u' ',
                valid=False,
                icon='')

  if query:
    task, project, note = split_input(query)

    # filter history by query
    history = wf.filter(query, history, key=search_friendly, min_score=20)

    # build title and subtitle
    start_title   = u'.Start: ' + task+project
    reg_title     = u'.Add: ' + task+project
    reg_subtitle  = ''
    if note:
      start_title   = u'.Start: ' + note.capitalize()
      reg_title     = u'.Add: ' + note.capitalize()
      reg_subtitle  = task+project
    
    start_valid = len(task) and len(project[1:])
    reg_valid = len(task) and len(project[1:]) and len(note)

    if active_timer:
      stop_valid = len(note)
      # add complete stop item
      stop_item = wf.add_item(title=u'.Stop timer',
                              subtitle=note.capitalize()+u' - '+active_timer,
                              arg='stop',
                              autocomplete=active_timer+u' ',
                              valid=stop_valid,
                              icon='')
      stop_item.setvar('wf_input', query)

    if (not active_timer) and (not len(note)): 
      # add start item
      start_item = wf.add_item(title=start_title,
                               subtitle='',
                               arg='start',
                               valid=start_valid,
                               icon='')
      start_item.setvar('wf_input', task+project)
  
    # add manual reg item
    reg_item = wf.add_item(title=reg_title,
                           subtitle=reg_subtitle,
                           arg='reg',
                           autocomplete=task+project+u' ',
                           valid=reg_valid,
                           icon='')
    reg_item.setvar('wf_input', query)

  # end if query

  # add history items last
  for hist in history: 
    task, project, note = split_input(hist)
    wf.add_item(title=task+project,
                subtitle='',
                arg='',
                autocomplete=task+project+u' ',
                copytext=task+project,
                valid=False,
                icon='')

  # return list to alfred
  wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))