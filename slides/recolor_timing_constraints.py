"""Recolor the CC BY-SA timing-window SVG for the Nord slide theme."""

from pathlib import Path
from lxml import etree

here = Path(__file__).resolve().parent
source = here / 'images/cts/timing_constraints_original.svg'
output = here / 'images/cts/timing_constraints_nord.svg'
svg_ns = 'http://www.w3.org/2000/svg'
tree = etree.parse(str(source))
root = tree.getroot()

colors = {
    '#7a401a': '#5E81AC',  # diagram lines -> Nord blue
    '#5d0e07': '#4C566A',  # caption / lettering -> Nord body
    '#fae38a': '#EBCB8B',  # timing window -> Nord yellow
    '#d1d1d1': '#ECEFF4',  # secondary shading -> Nord panel
    '#000000': '#4C566A',  # text -> Nord body
}

for element in root.iter():
    for key, value in list(element.attrib.items()):
        new_value = value
        for old, new in colors.items():
            new_value = new_value.replace(old, new)
        new_value = new_value.replace('Noto Serif SC', 'Latin Modern Sans')
        new_value = new_value.replace('Noto Sans SC', 'Latin Modern Sans')
        element.set(key, new_value)

for element in root.xpath('//svg:text', namespaces={'svg': svg_ns}):
    if element.get('systemLanguage') == 'zh' or element.get('id') == 'text1-8-7':
        element.getparent().remove(element)

root.set('height', '76mm')
root.set('viewBox', '0 0 160 76')
root.insert(0, etree.Comment(
    'Adapted from Timing constraints mechanism.svg by 思考的苇丛, '
    'CC BY-SA 4.0. Colors/fonts changed to Nord; duplicate Chinese '
    'labels and bottom caption removed. '
    'https://commons.wikimedia.org/wiki/File:Timing_constraints_mechanism.svg'
))
background = etree.Element(f'{{{svg_ns}}}rect', x='0', y='0',
                           width='160', height='76', fill='#ffffff')
root.insert(1, background)
tree.write(str(output), encoding='utf-8', xml_declaration=True)
print(output)
