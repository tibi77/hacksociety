import xml.etree.ElementTree as ET
import json
tree = ET.parse('test.xml')
root = tree.getroot()

formula = {}

for kid in root:
    for eu in kid:
        for child in eu:
            print(child.attrib)