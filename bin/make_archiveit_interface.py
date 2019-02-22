import sys
import json

from datetime import datetime
from urllib.parse import quote_plus, quote

from aiu import convert_LinkTimeMap_to_dict

from bs4 import BeautifulSoup

import requests

inputfilename = sys.argv[1]
metadatafilename = sys.argv[2]
outputfilename = sys.argv[3]

metadata_map = {
    "group": "?fc=websiteGroup%3A",
    "subject": "?fc=meta_Subject%3A",
    "coverage": "?fc=meta_Coverage%3A",
    "creator": "?fc=meta_Creator%3A",
    "publisher": "?fc=meta_Publisher%3A",
    "source": "?fc=meta_Source%3A",
    "language": "?fc=meta_Language%3A",
    "format": "?fc=meta_Format%3A",
    "type": "?fc=meta_Type%3A",
    "date": "?fc=meta_Date%3A",
    "relation": "?fc=meta_Relation%3A",
    "collector": "?fc=meta_Collector%3A"
}

with open(inputfilename) as f:
    data = f.read()

with open(metadatafilename) as f:
    metadata = json.load(f)

soup = BeautifulSoup(data, "html.parser")

entries = []

for tag in soup.find_all('blockquote'):
    entry = {}

    entry["collectionid"] = ""

    try:
        entry["collectionid"] = tag['data-archive-collection-id']
    except KeyError as e:
        entry["collectionid"] = None
    
    print("collection ID is {}".format(entry['collectionid']))

    entry['urim'] = tag['data-versionurl']
    entry["urir"] = tag['data-originalurl']
    # entry["title"] = tag.find_all('p')[0].text
    # entry["description"] = tag.find_all('p')[1].text
    entry["more_metadata"] = {}
    entry['memento_count'] = 1
    entry['first_memento_dt'] = ""
    entry['first_memento_uri'] = entry['urim']
    entry['last_memento_dt'] = ""
    entry['last_memento_uri'] = ""
    entry['timegate'] = ""

    r = requests.get(entry['urim'])

    links = r.links
    urit = links['timemap']['url']

    entry['first_memento_dt'] = datetime.strptime( r.headers['memento-datetime'], '%a, %d %b %Y %H:%M:%S GMT' ).strftime('%B %d, %Y')

    try:
        timegate = links['timegate']['url']
    except KeyError as e:
        print("failed to find the URI-G for URI-M {}".format(entry['urim']))
        entries.append(entry)
        continue

    r = requests.get(urit)

    timemap = convert_LinkTimeMap_to_dict( r.text )

    try:
        entry['memento_count'] = len(timemap['mementos']['list'])
    except KeyError as e:
        print("failed to count mementos in TimeMap at {}".format(urit))
        entries.append(entry)
        continue

    try:
        mementos = timemap['mementos']['list']
    except KeyError as e:
        print("failed to find mementos in TimeMap at {}".format(urit))
        entries.append(entry)
        continue

    memento_list = []

    for memento in mementos:
        memento_list.append( ( memento['datetime'], memento['uri'] ) )

    memento_list.sort()

    entry['first_memento_dt'] = memento_list[0][0].strftime('%B %d, %Y')
    entry['first_memento_uri'] = memento_list[0][1]

    entry['last_memento_dt'] = memento_list[-1][0].strftime("%B %d, %Y")
    entry['last_memento_uri'] = memento_list[-1][1]
    entry['timegate'] = timegate

    try:
        all_metadata = metadata['seed_metadata']['seeds'][ entry['urir'] ]['collection_web_pages']

        for item in all_metadata[0]:
            if item == "title":
                entry['title'] = all_metadata[0][item]
            elif item == "description":
                entry['description'] = all_metadata[0][item][0]
            else:
                entry["more_metadata"][item] = all_metadata[0][item][0]

    except TypeError:
        print("working on URI-R {}".format(entry["urir"]))
        print(all_metadata['seed_metadata']['seeds'][entry['urir']])
        print('exiting on error')
        sys.exit(255)
    except KeyError:
        print("no metadata for {}".format(entry['urir']))

    entries.append(entry)

with open(outputfilename, 'w') as g:

    g.write("""<html>
    <head>
    <link type="text/css" rel="stylesheet" href="https://archive-it.org/static/css/global2.css">
    <link type="text/css" rel="stylesheet" href="https://archive-it.org/static/css/960_12_col.css">
    <link type="text/css" rel="stylesheet" href="https://archive-it.org/static/css/thirdparty/ui-lightness/jquery-ui-1.11.4.custom.min.css">
    </head>    
    <body>

    <div class="highlight-box" id="entity-results">
""")

    for entry in entries:
        output = '<div class="result-item">\n'

        if "title" in entry:
            output += '<h3 class="url">Title: {}</h3>\n'.format(entry["title"])

        if entry['collectionid'] is not None:
            print("collection ID {} is set".format(entry['collectionid']))
            output += '<h3 class="url">URL: <a title="{}" href="https://wayback.archive-it.org/{}/*/{}">{}</a></h3>\n'.format(entry["urir"], entry["collectionid"], entry["urir"], entry["urir"])
        else:
            output += '<h3 class="url">URL: <a title="{}" href="https://web.archive.org/web/*/{}">{}</a></h3>\n'.format(entry["urir"], entry["urir"], entry["urir"])

        if "description" in entry:
            output += '<p><b>Description:</b> {}</p>\n'.format(entry["description"])

        if entry['memento_count'] == 1:
            output += '<p url="{}" prefix="https://wayback.archive-it.org/{}" class="waybackCaptureInfo"> Captured <a href="https://wayback.archive-it.org/{}/*/{}">once</a> on <a href="{}">{}</a></p>\n'.format(
                quote(entry["urir"]), 
                entry["collectionid"],
                entry["collectionid"],
                entry["urir"],
                entry['first_memento_uri'], 
                entry['first_memento_dt']
                )
        else:
            output += '<p url="{}" prefix="https://wayback.archive-it.org/{}" class="waybackCaptureInfo"> Captured <a href="https://wayback.archive-it.org/{}/*/{}">{}</a> times between <a href="{}">{}</a> and <a href="{}">{}</a></p>\n'.format(
                quote(entry["urir"]), 
                entry["collectionid"],
                entry["collectionid"],
                entry["urir"],
                entry['memento_count'],
                entry['first_memento_uri'],
                entry['first_memento_dt'],
                entry['last_memento_uri'],
                entry['last_memento_dt']
                )

        output += '<div sytle="display: inherit;" class="moreMetadata">\n'

        for item in entry['more_metadata']:

            if item in metadata_map:
                output += '<p><b>{}:&nbsp;&nbsp;</b>\n'.format(item.title())
#                output += '<a href="#" class="add-facet-link">{}</a>'.format(entry['more_metadata'][item])
                output += '<a href="https://archive-it.org/collections/{}{}{}" class="add-facet-link">{}</a>'.format(
                    entry['collectionid'],
                    metadata_map[ item ],
                    quote_plus( entry['more_metadata'][item] ),
                    entry['more_metadata'][item]
                    )

        output += '</div>\n'

        output += '</div>\n'
        g.write(output)

    g.write('</div>\n</body>\n</html>')
