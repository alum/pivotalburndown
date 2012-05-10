import os
import pivotal
import settings

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main():
	data = { 'test':'test', 'apa':'apan' }
	return render_template('main.html', data=data)

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)