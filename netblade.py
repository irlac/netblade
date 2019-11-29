import os, requests, re, sys, time
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
PY3 = sys.version_info[0] >= 3
if PY3: #python3
    from urllib.parse import urlparse
else: #python2
    from urlparse import urlparse

platform = input('[i]nstagram, [v]sco, or [b]oth? ')
if platform == 'b':
	i_username = input('Enter the Instagram username: ')
	v_username = input('Enter the VSCO username: ')
else:
	username = input('Enter the username: ')

class Platform:
	def call(self, response, name):
		if not os.path.exists(save_dest):
			os.mkdir(save_dest)
		if not os.path.exists(save_dest + name):
			#print(name)
			open(save_dest + name, 'wb').write(response.content)

	def retrieve(self, uname, pform):
		print("Retrieving with username " + uname + " on platform " + pform)
		if pform == 'vsco':
			res = requests.get("https://vsco.co/" + uname + "/images/", stream = True)
			soup = bs(res.content, "html5lib")
			preval = soup.find_all('script')
			url = re.findall('responsiveUrl":"(.+?)"', str(preval))
			urls = len(url)
			print("Found " + str(urls) + " urls.")
			for x in tqdm(range(urls), unit=' files'):
				print(x,str(url[x]))
				parse = urlparse(str(url[x]))
				name = os.path.basename(parse.path)
				out = requests.get("https://" + url[x])
				self.call(out, name)
		elif pform == 'insta':
			res = requests.get("https://www.instagram.com/" + uname, stream = True)
			soup = bs(res.content, "html5lib")
			preval = soup.find_all('script')
			shortcode = re.findall('shortcode":"(.+?)"', str(preval))
			scodes = len(shortcode)
			for x in range(scodes):
				url = "https://instagram.com/p/" + shortcode[x] + "/media?size=l"
				name = re.findall('p/(.+?)/media', url)
				name = str(name[0]) + '.jpg'
				out = requests.get(url)
				self.call(out, name)

vsco = Platform()
insta = Platform()

if platform == 'i':
	save_dest = './' + username + '/'
	insta.retrieve(username, 'insta')
elif platform == 'v':
	save_dest = './' + username + '/'
	vsco.retrieve(username, 'vsco')
elif platform == 'b':
	save_dest = './' + i_username + '/'
	insta.retrieve(i_username, 'insta')
	save_dest = './' + v_username + '/'
	vsco.retrieve(v_username, 'vsco')