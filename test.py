import xmltodict, xml.dom.minidom
with open("feed.rss",'r') as xml:
    lines = xml.read()
    print(type(xml.lines))
    print(xml.dom.minidom.parse(lines))
    print(xmltodict.parse(lines))