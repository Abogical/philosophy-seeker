import sys
from re import fullmatch, compile
from urllib.request import urlopen
from lxml.html import fromstring, tostring
from itertools import chain
from time import sleep

def print_usage():
	print("""Usage:
./main.py <Wikipedia URL>""")

URL_LIMIT = 500

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('ERROR: URL argument missing', file=sys.stderr)
		print_usage()
		exit(1)

	wiki_re = compile('https?://(\w+)\.wikipedia\.org/wiki/(.+)')
	wiki_match = wiki_re.fullmatch(sys.argv[1])
	if wiki_match == None:
		print('Not a valid wikipedia link', file=sys.stderr)
		print_usage()
		exit(1)
	wiki_lang = wiki_match.group(1)
	name = wiki_match.group(2)

	if name == 'Philosophy':
		print('Already entered the philosophy URL')
		exit(0)

	name_re = compile('/wiki/([^#]+)')

	visited = []

	def detect_loop(name):
		if name in visited:
			print(f'Loop detected: {" -> ".join(visited[visited.index(name):])} -> {name}')
			exit(0)

	def detect_philosophy(name):
		if name == 'Philosophy':
			print(f'Found philosophy wiki! Link Path: \n{" -> ".join(visited)} -> Philosophy'
				if len(visited) > 0 else 'Already entered a URL that redirected to philosophy')
			exit(0)


	for _ in range(1, URL_LIMIT):
		next_name = None
		response = urlopen(f'https://{wiki_lang}.wikipedia.org/wiki/{name}')
		# Redirect may change the name of the loop
		name = wiki_re.fullmatch(response.geturl()).group(2)
		detect_philosophy(name)
		detect_loop(name)
		visited.append(name)
		# Determining if it's a "normal" link
		for link in fromstring(response.read()).xpath('//*[@role="main"]//p/a[starts-with(@href, "/wiki/")]'):
			parens = 0
			# Check if it is inside a paranthesis
			for token in reversed(link.xpath('./preceding-sibling::text()')):
				if ')' in token:
					parens += 1
				if '(' in token:
					parens -= 1
				if parens < 0:
					break
			if parens < 0:
				continue
			next_name = name_re.match(link.attrib['href']).group(1)
			break
		detect_philosophy(next_name)
		detect_loop(next_name)
		name = next_name
		sleep(0.5)
		print(f'Visiting topic {name}')



