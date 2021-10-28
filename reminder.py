# encoding: utf-8

import time
from workflow import Workflow3
from workflow.notify import notify
from common import *

def main(wf):
  time.sleep(calc_interval())
  if check_workhours():
    notify(u'Time tracker', u'Remember to track time ⏱')
    start_reminder()

# end main

if __name__ == u"__main__":
    wf = Workflow3()
    wf.run(main)