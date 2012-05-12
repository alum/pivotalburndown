import os
import pivotal
import settings
from busyflow.pivotal import *
from flask import Flask, render_template, request
from datetime import *
app = Flask(__name__)

@app.route('/')
def main():
	client = PivotalClient(token=settings.token, cache='')
	#projects = client.projects.all()['projects']
	data = client.iterations.current(settings.project_id)
	point_sum = sum(map(lambda x: 0 if 'estimate' not in x else x['estimate'], data['iterations'][0]['stories']))

	# make a list of story states that are counted in the burndown, i.e. seen as "done"
	#accepted_states = ['accepted']
	#if 'include_states' in request.args:
	#	accepted_states.extend(request.args['include_states'].split(','))

	# find max and min dates for accepted stories
	for iteration in data['iterations']:
		dates = []
		for story in iteration['stories']:
			if 'accepted_at' in story:
				dates.append(story['accepted_at'])
		iteration['min_date'] = min(dates).date()
		iteration['max_date'] = max(dates).date()

	dates, dates_sorted = get_dates(iteration['start'].date(), iteration['finish'].date())

	dates = get_burndown(point_sum, dates, dates_sorted, data)
	
	#sorted(dates.iteritems(), key= lambda (k,v): (v,k))
	data = { 'iterations':data['iterations'], 
			 'dates':dates, 
			 'dates_sorted':dates_sorted, 
			 'optimal_curve':get_optimal_curve(dates_sorted, point_sum) }

	return render_template('main.html', data=data)

def get_burndown(point_sum, dates, dates_sorted, data):
	burndown_sum = point_sum
	for iteration in data['iterations']:
		for date in dates_sorted:
			if date > datetime.utcnow().date():
				break
			for story in iteration['stories']:
				if u'accepted_at' in story and story['accepted_at'].date() == date and u'estimate' in story:
					burndown_sum -= story['estimate']
				dates[date] = burndown_sum
	return dates

def get_dates(start_date, finish_date):
	delta = finish_date - start_date
	dates = {}
	for x in xrange(delta.days + 1):
		dates[start_date + timedelta(days=x)] = ''
	
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
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)