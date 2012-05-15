pivotalburndown
===============

A small burndown chart that gets data from the Pivotal Tracker API. Uses busyflow.pivotal for getting stories.

Installation
------------

This app has been prepared to run on Heroku.

(Assuming you are on OS X)

1. Get an account on Heroku.com if you don't already have one. Install the heroku toolbelt.

2. Clone into a dir of your liking "git clone git://github.com/alum/pivotalburndown.git"

3. Create a virtualenv "virtualenv venv --distribute"

4. Activate virtualenv "source venv/bin/activate"

5. Install dependencies: "pip install -r requirements.txt"

6. Rename settings_example.py to settings.py and enter your project details.

7. Remove 'settings.py' from .gitignore: "vi .gitignore"

8. Commit: "git commit -am 'settings'"

9. You are now able to run the app locally with "python app.py" and try it out on http://localhost:5000/

10. Create app on heroku: "heroku create --stack cedar"

11. Push code to heroku: "git push heroku master"

12. Scale the web worker to one process (free!): "heroku ps:scale web=1". DONE!

Heroku has an excellent guide to deployment: https://devcenter.heroku.com/articles/python