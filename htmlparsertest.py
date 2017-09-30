import html.parser

words = []
class HTMLParser(html.parser.HTMLParser):
    #def handle_starttag(self, tag, attrs):
    #    print(tag)
    #def handle_endtag(self, tag):
    #    print(tag)
    def handle_data(self, data):
        if ("".join(data.split()) != "" and "".join(data.split()).startswith("Letter") == False):
            words.append(data)

hp = HTMLParser()
with open("6Letters.html") as file:
    hp.feed(file.read())
print(words)
