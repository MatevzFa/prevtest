import xml.etree.ElementTree as ET
import logging
import os


class XmlTree():

    def __init__(self):
        self.logger = logging.getLogger('xml_compare')
        self.logger.setLevel(logging.DEBUG)
        self.hdlr = logging.FileHandler('xml-comparison.log')
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s- %(message)s')
        self.hdlr.setLevel(logging.DEBUG)
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)

    @staticmethod
    def convert_string_to_tree(xmlString):
        return ET.fromstring(xmlString)

    def xml_compare(self, x1, x2, excludes=[]):
        """
        Compares two xml etrees
        :param x1: the first tree
        :param x2: the second tree
        :param excludes: list of string of attributes to exclude from comparison
        :return:
            True if both files match
        """

        if x1.tag != x2.tag:
            self.logger.debug('Tags do not match: %s and %s' % (x1.tag, x2.tag))
            return False
        for name, value in x1.attrib.items():
            if name not in excludes:
                if x2.attrib.get(name) != value:
                    self.logger.debug('Attributes do not match: %s=%r, %s=%r'
                                      % (name, value, name, x2.attrib.get(name)))
                    return False
        for name in x2.attrib.keys():
            if name not in excludes:
                if name not in x1.attrib:
                    self.logger.debug('x2 has an attribute x1 is missing: %s'
                                      % name)
                    return False
        if not self.text_compare(x1.text, x2.text):
            self.logger.debug('text: %r != %r' % (x1.text, x2.text))
            return False
        if not self.text_compare(x1.tail, x2.tail):
            self.logger.debug('tail: %r != %r' % (x1.tail, x2.tail))
            return False
        cl1 = x1.getchildren()
        cl2 = x2.getchildren()
        if len(cl1) != len(cl2):
            self.logger.debug('children length differs, %i != %i'
                              % (len(cl1), len(cl2)))
            return False
        i = 0
        for c1, c2 in zip(cl1, cl2):
            i += 1
            if c1.tag not in excludes:
                if not self.xml_compare(c1, c2, excludes):
                    self.logger.debug('children %i do not match: %s'
                                      % (i, c1.tag))
                    return False
        return True

    def text_compare(self, t1, t2):
        """
        Compare two text strings
        :param t1: text one
        :param t2: text two
        :return:
            True if a match
        """
        if not t1 and not t2:
            return True
        if t1 == '*' or t2 == '*':
            return True
        return (t1 or '').strip() == (t2 or '').strip()

    def xml_files_compare(self, f1, f2, excludes=[]):
        """
        Compare two xml files
        :param f1: file one
        :param f2: file two
        :param excludes: list of string of attributes to exclude from comparison
        :return:
            True if a match
        """
        xml1 = self.convert_string_to_tree(open(f1).read())
        xml2 = self.convert_string_to_tree(open(f2).read())
        return self.xml_compare(xml1, xml2, excludes=excludes)
