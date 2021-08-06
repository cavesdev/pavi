import os

from dotenv import load_dotenv
load_dotenv()

# set variables
os.environ['PYTHONPATH'] = os.getcwd()
os.environ['PROJECT_PATH'] = os.getcwd()
os.environ['PROJECT_MODULE_NAME'] = 'pavi'
os.environ['PROJECT_MODULE_PATH'] = os.path.join(os.getcwd(), os.getenv('PROJECT_MODULE_NAME'))

from pavi.app import app

app.run()