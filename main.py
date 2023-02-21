import xml.etree.ElementTree as ET
import os
from pathlib import Path

src_folder = Path('.')
out_folder = Path('output')
src_dat_name = 'bigdat.xml'
allowed_categories = ['Games', 'Educational', 'Bonus Discs', 'Multimedia', 'Video']
extra_folder_name = '~extra'

games = {}
others = {}
header = None
prolog = None

def read_prolog():
    with open(src_folder / src_dat_name) as file:
        global prolog
        # prolog is just the first 2 lines
        prolog = file.readline() + file.readline()

def parse():
    tree = ET.parse(src_folder / src_dat_name)
    root = tree.getroot()
    # get header
    if root[0].tag != 'header':
        raise ValueError('First tag is not header')
    global header
    header = root[0]
    # get content
    for child in root[1:]:
        if child.tag != 'game':
            raise ValueError(f'Found unexpected "{child.tag}" tag')
        # find the category
        category = None
        for grandchild in child:
            if grandchild.tag == 'category':
                category = grandchild.text
        if category not in allowed_categories:
            raise ValueError(f'Found unexpected "{category}" category')

        # first category is games
        if category == allowed_categories[0]:
            first_char = child.attrib['name'][0]
            if(first_char.isalpha()):
                first_char = first_char.upper()
            else:
                first_char = '#'
            # first time create the list
            if first_char not in games:
                games[first_char] = list()
            games[first_char].append(child)
        # handle others
        else:
            # first time create the list
            if category not in others:
                others[category] = list()
            others[category].append(child)

def test():
    pass

def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)

def create_xml(folder, file_name, elements):
    # create file
    with open(folder / (file_name + '.dat'), 'w') as file:
        # write header
        file.write(prolog)
        file.write('<datafile>\n\t')
        file.write(ET.tostring(header, encoding='unicode'))
        # write elements
        for element in elements[:-1]:
            file.write(ET.tostring(element, encoding='unicode'))

        # last line, remove extra space
        to_write = ET.tostring(elements[-1], encoding='unicode')    
        last_newline = to_write.rfind('\n')
        file.write(to_write[:last_newline+1])
        file.write('</datafile>')
        
        
def main():
    read_prolog()
    parse()
    # handle games
    for letter in games:
        folder = out_folder / letter
        create_folder(folder)
        create_xml(folder, letter, games[letter])
    # handle other
    for category in others:
        folder = out_folder / extra_folder_name / category
        create_folder(folder)
        create_xml(folder, category, others[category])

if __name__ == '__main__':
    main()
#    test()

