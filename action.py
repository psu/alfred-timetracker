# encoding: utf-8

import sys, os
from workflow import Workflow3
from workflow.notify import notify
from common import *

def main(wf):
  
  # a valid call has two arguments
  if len(wf.args) == 2:

    # input
    action = wf.args[0]
    input  = wf.args[1]  
    task, project, note = split_input(input)
    
    # actions
    if action == 'reminder':
      start_reminder()

    if action == 'start':
      start_timer(task, project)
      notify('Timer started', task+project)

    if action == 'stop':
      stop_timer(task, project, note)
      notify('Timer stopped', output_string(task, project, note))
    
    if action == 'reg':
      reg_timer(task, project, note)
      notify('Time added', output_string(task, project, note))

# end main

if __name__ == u"__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))