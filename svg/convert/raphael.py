import xml.etree.ElementTree as etree

class Raphael:
    def __init__(self, xml):
        self.xml = xml

    def to_raphael(self):
        #dom = etree.fromstring(xml)
        #for elem in dom:
        #  logging.debug(elem.tag)
        return 'to_raphael:' + self.xml 
