import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_with_retry(url):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1)
    s.mount('http://', HTTPAdapter(max_retries=retries))
    return s.get(url)
