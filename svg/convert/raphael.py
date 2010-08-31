import xml.etree.ElementTree as etree
import re

class Raphael:
    def __init__(self, xml):
        self.xml = xml
        self.rows = []

    def to_raphael(self):
        tree = etree.fromstring(self.xml)

        self.__set_init_code(tree)

        for elem in tree:
            self.__parse_elem(elem)

        return '\n'.join(self.rows)

    def __set_init_code(self, tree):
        target = 'raphael_canvas'
        width  = tree.get('width')  or 0
        height = tree.get('height') or 0
        code = "var paper = Raphael('%(target)s', '%(width)s', '%(height)s');\n"

        self.rows.append(code % locals())

    def __parse_elem(self, elem, attrs = {}):
        if not attrs: attrs = {}
        row = Row()

        tag_name = re.sub('^{.+}', '', elem.tag)
        methods = ['path', 'circle', 'rect', 'ellipse', 'image', 'text']
        if tag_name in methods:
            row.method = tag_name
            if tag_name == 'path':
                row.d = elem.get('d')
        elif tag_name == 'a':
            for _elem in elem:
                self.__parse_elem(_elem)
            return
        elif tag_name == 'g':
            attrs.update(self.__fill_attr(elem, attrs))
            for _elem in elem:
                self.__parse_elem(_elem, attrs)
            return

        if row.write_able():
            attrs.update(self.__fill_attr(elem, attrs))
            if attrs:
                row.attrs = attrs
            self.rows.append(row.to_string())

    @staticmethod
    def __fill_attr(elem, inherit_attrs):
        target_attrs = [
            'clip-rect', 'cx', 'cy', 'fill', 'fill-opacity', 'font',
            'font-family', 'font-size', 'font-weight', 'height',
            'opacity', 'path', 'r', 'rotation', 'rx', 'ry', 'scale',
            'src', 'stroke', 'stroke-dasharray', 'stroke-linecap',
            'stroke-linejoin', 'stroke-miterlimit', 'stroke-opacity',
            'stroke-width', 'translation', 'width', 'x', 'y'
        ]

        attrs = dict() 
        for key in target_attrs:
            val = elem.get(key)
            if val:
                if not re.match('^\d+$', val):
                    val = "'%s'" % val
                attrs[key] = val
            elif key == 'stroke' and not inherit_attrs.get('stroke'):
                attrs[key] = "'none'"

        return attrs

class Row:
    def __init__(self):
        self.__method = ''
        self.__attrs  = dict()
        self.__d      = ''

    def get_method(self):
        return self.__method
    def set_method(self, value):
        self.__method = value
    method = property(get_method, set_method)

    def get_attrs(self):
        return self.__attrs
    def set_attrs(self, value):
        self.__attrs = value
    attrs = property(get_attrs, set_attrs)

    def get_d(self):
        return self.__d
    def set_d(self, value):
        self.__d = value
    d = property(get_d, set_d)

    def write_able(self):
        return self.method

    def to_string(self):
        if not self.method:
            raise 'ParseError: method is not set'

        param = "'%s'" % self.d if self.method == 'path' else ''
        ret = "paper.%s(%s)" % (self.method, param)

        attr_list = list()
        for key in self.attrs:
            val = self.attrs[key]
            attr_list.append("'%(key)s':%(val)s" % locals())
        attr_str = ', '.join(attr_list)
        if attr_str:
            ret += '.attr({%s})' % attr_str

        return ret + ';'
