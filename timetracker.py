# encoding: utf-8

from workflow import Workflow, web
import os

def trigger_ifttt(arg):
	url = ('https://maker.ifttt.com/trigger/' +
			ifttt_trigger + 
			'/with/key/' + 
			ifttt_key )
	r = web.post( url, data=arg )
	r.raise_for_status()

# # # # # # # # # # #
# init
wf = Workflow()

ifttt_trigger  = os.getenv('ifttt_trigger')
ifttt_key = os.getenv('ifttt_key')
wf_action  = os.getenv('action')
wf_project = os.getenv('project')
wf_timestamp = os.getenv('timestamp')

values = {}
values['value1'] = wf_timestamp
values['value2'] = wf_action
values['value3'] = wf_project

trigger_ifttt(values)

#print('query')