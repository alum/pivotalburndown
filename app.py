import os
import sys
import pivotal
import settings
from auth import requires_auth
from busyflow.pivotal import *
from flask import Flask, render_template, request, Response
from functools import wraps
from datetime import *
app = Flask(__name__)


client = PivotalClient(token=settings.token, cache='')

@app.route('/')
@requires_auth
def main():
	global client
	#data = ((proj['name'], proj['id']) for proj in client.projects.all()['projects'])
	data = client.projects.all()['projects']
	return render_template('main.html', data=data)

@app.route('/project/<int:project_id>')
@requires_auth
def project(project_id):
	global client
	data = client.iterations.current(project_id) # get the current iteration
	data['iterations'].append(client.iterations.done(project_id, offset=-1)['iterations'][0]	) # get the last iteration
	
	dates = {}
	dates_sorted = {}
	optimal_curve = {}
	k = 0
	for iteration in data['iterations']:

		#k = iteration['number']
		point_sum = get_point_sum(iteration) # sum all points for iteration

		dates[k] = []
		dates_sorted[k] = []
		# finish date is always start date of the next iteration, so we must remove the last day
		dates[k], dates_sorted[k] = get_dates(iteration['start'].date(), (iteration['finish'].date() + timedelta(days=-1)))

		dates[k] = get_burndown(point_sum, dates[k], dates_sorted[k], iteration)

		optimal_curve[k] = get_optimal_curve(dates_sorted[k], point_sum)
		k += 1
	
	data = { 'iterations':data['iterations'], 
			 'dates':dates, 
			 'dates_sorted':dates_sorted, 
			 'optimal_curve': optimal_curve }

	return render_template('project.html', data=data)

def get_point_sum(iteration):
	return sum(map(lambda x: 0 if 'estimate' not in x else x['estimate'], iteration['stories']))

def get_burndown(point_sum, dates, dates_sorted, iteration):
	burndown_sum = point_sum
	for date in dates_sorted:
		if date > datetime.utcnow().date():
			break
		for story in iteration['stories']:
			if 'accepted_at' in story and (story['accepted_at'].date() + timedelta(days=1)) == date and 'estimate' in story:
				burndown_sum -= story['estimate']
			dates[date] = burndown_sum
	return dates

def get_dates(start_date, finish_date):
	delta = finish_date - start_date
	dates = {}
	for x in xrange(delta.days + 1):
		date = start_date + timedelta(days=x)
		if date.isoweekday() != 6 and date.isoweekday() != 7: # remove weekends
			dates[date] = ''
	
	dates_sorted = dates.keys()
	dates_sorted.sort()
	return dates, dates_sorted

def get_optimal_curve(dates_sorted, total_points):
	optimal_curve = {}
	num_dates = len(dates_sorted)
	for x in xrange(num_dates):
		optimal_curve[dates_sorted[x]] = total_points -  (x * float(total_points) / float(num_dates-1))
	return optimal_curve


if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	if 'debug' in sys.argv:
		app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)