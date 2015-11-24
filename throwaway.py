import urllib2
import json
address = "https://randomuser.me/api/"
website = urllib2.urlopen(address)
js = website.read()
print js
text = json.loads(js)
print text
print text['user']['gender']
