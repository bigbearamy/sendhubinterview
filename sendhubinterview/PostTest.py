import httplib

def printText(txt):
    lines = txt.split('\n')
    for line in lines:
        print line.strip()

httpServ = httplib.HTTPConnection("hidden-dawn-9384.herokuapp.com", 80)
httpServ.connect()

quote = '{"message":"SendHubRocks", "recipients":["+15555555556","+15555555555","+15555555554","+15555555553","+15555555552","+15555555551"]}'

httpServ.request('POST', '/webservices/submit', '%s' % quote)

response = httpServ.getresponse()
if response.status == httplib.OK:
    print "Output from CGI request"
    print (response.read())

httpServ.close()