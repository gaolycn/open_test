import requests
from requests import Request,Session

for i in range(0,2): 
    s=requests.Session()
    r1=s.get('https://haojinmis.qa.qfpay.net/adv/redirect/adv_redirect?adv_id=59/&', verify=False)
    print r1
