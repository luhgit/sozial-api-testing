import codecs
def parse():
	content_file = codecs.open('posts.json', 'r', 'utf-8')
	content = content_file.read()
	print(content)
	content_file.close()
parse()