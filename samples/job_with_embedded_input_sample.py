import sys
import os
import logging
import dotenv
sys.path.insert(0, '..')
from modzy import ApiClient
from modzy._util import file_to_bytes


# Basic configuration of logger (level setted in debug)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# dotenv variables

dotenv.load_dotenv()

BASE_URL = os.getenv('MODZY_BASE_URL')
API_KEY = os.getenv('MODZY_API_KEY')


# Client initialization
client = ApiClient(base_url=BASE_URL, api_key=API_KEY)

# Create a Job with a text input, wait and retrieve results

image_bytes = file_to_bytes('../samples/image.png')
job = client.jobs.submit_bytes('f7e252e26a', '0.0.1', {'image': image_bytes})
logger.info("job: %s", job)
job.block_until_complete(timeout=None)
logger.info("job: %s", job)
result = job.get_result()
logger.info("result: %s", result)
results_json = result.get_first_outputs()['results.json']
logger.info("results_json: %s", results_json)

# Create a job with more than one input

job = client.jobs.submit_bytes_bulk('f7e252e26a', '0.0.1', {
        'image-1': {'image': image_bytes},
        'other-id': {'image': image_bytes},
})
logger.info("job: %s", job)
job.block_until_complete(timeout=None)
logger.info("job: %s", job)
result = job.get_result()
logger.info("result: %s", result)
results_json = result.get_first_outputs()['results.json']
logger.info("results_json: %s", results_json)
