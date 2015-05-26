import requests
import time
def make_request(str):
    """
    Makes a requests.get call.  If return code is 429, pause for 10
    seconds and try again. If return code is not 200 after that, raises a
    generic exception.
    """
    r = requests.get(str)
    if r.status_code == 429:
        print('-- Rate Limit Exceeded. Pausing for 10 seconds...')
        time.sleep(10)
        r = make_request(str)
    if r.status_code != 200:
        raise Exception('Return status code {}'.format(r.status_code))
    return r
