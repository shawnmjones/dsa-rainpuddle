import sys

from bs4 import BeautifulSoup

inputfile = sys.argv[1]
outputfile = sys.argv[2]


with open(inputfile) as f:

    html = f.read()


soup = BeautifulSoup(html, 'html5lib')

links = soup.find_all('a')

uri_img = []


for link in links:
    uri = link.get('href')

    img = link.find_all('img')[0]

    uri_img.append( ( uri, img.get('src') ) )



thumbcounter = 0

table_output = ''
table_output += '<table style="border-width: 0px">\n'
table_output += '<tr>\n'

for thumb in uri_img:

    uri = thumb[0]
    img = thumb[1]

    if thumbcounter % 4 == 0 and thumbcounter != 0:
        table_output += '</tr><tr>\n'

    table_output += '<td>\n<a href="{}">\n<img src="{}" />\n</a>\n</td>\n'.format(uri, img)

    thumbcounter += 1

if table_output[-4:] == '<tr>':
    table_output = table_output[:-4]

if table_output[-5:] != '</tr>':
    table_output += '</tr>\n'

table_output += '</table>'

html_top = """<html>
<head>
<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<meta content="utf-8" http-equiv="encoding">
</head>
<body>
"""

html_bottom = "</html>"

with open(outputfile, 'w') as f:

    f.write('\n'.join( [ html_top, table_output, html_bottom ] ) )
