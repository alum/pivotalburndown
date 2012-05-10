import settings
from busyflow.pivotal import *

def main():
	client = PivotalClient(token=settings.token, cache='')
	#projects = client.projects.all()['projects']
	iterations = client.iterations.current(settings.project_id)
	print iterations

if __name__ == '__main__':
	main()