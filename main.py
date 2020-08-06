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

	wiki_match = fullmatch('https?://(\w+)\.wikipedia\.org/wiki/(.+)', sys.argv[1])
	if wiki_match == None:
		print('Not a valid wikipedia link', file=sys.stderr)
		print_usage()
		exit(1)
	wiki_lang = wiki_match.group(1)
	name = wiki_match.group(2)

	name_re = compile('/wiki/([^#]+)')

	visited = [name]
	for _ in range(1, URL_LIMIT):
		next_name = None
		# Determining if it's a "normal" link
		for link in fromstring(urlopen(f'https://{wiki_lang}.wikipedia.org/wiki/{name}').read()).xpath('//*[@role="main"]//p/a[starts-with(@href, "/wiki/")]'):
			parens = 0
			for sibling in chain([link], link.itersiblings()):
				if b'(' in tostring(sibling):
					parens += 1
				if b')' in tostring(sibling):
					parens -= 1
				if parens < 0:
					continue
			if parens < 0:
				continue
			next_name = name_re.match(link.attrib['href']).group(1)
			break
		if next_name == 'Philosophy':
			print(f'Found philosophy wiki! Link Path: \n{" -> ".join(visited)} -> Philosophy')
			exit(0)
		if next_name in visited:
			print(f'Loop detected: {" -> ".join(visited[visited.index(next_name):])} -> {next_name}')
			exit(0)
		visited.append(next_name)
		name = next_name
		print(f'Visiting topic {name}')
		sleep(0.5)



