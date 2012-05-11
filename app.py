import os
import pivotal
import settings
from busyflow.pivotal import *
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main():
	client = PivotalClient(token=settings.token, cache='')
	#projects = client.projects.all()['projects']
	data = client.iterations.current(settings.project_id)
	point_sum = sum(map(lambda x: 0 if 'estimate' not in x else x['estimate'], data['iterations'][0]['stories']))
	#print apa

	# find max and min dates for accepted stories
	for iteration in data['iterations']:
		dates = []
		for story in iteration['stories']:
			if 'accepted_at' in story:
				dates.append(story['accepted_at'])
		iteration['max_date'] = max(dates)
		iteration['min_date'] = min(dates)

	

	for iteration in data['iterations']:
		for story in iteration['stories']:
			if 'estimate' not in story:
				story['estimate'] = 0
			if story['estimate'] == 'accepted':
				point_sum -= story['estimate']
				story['burndown'] = point_sum
	data = { 'iterations':data['iterations']}
	return render_template('main.html', data=data)

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)