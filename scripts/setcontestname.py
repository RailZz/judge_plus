import xml.etree.ElementTree as ET
from config import *

def setContestXML(contest, name, registerContest = None, name_en = 'Contest'):
    parser = ET.XMLParser(encoding='utf-8')
    tree = ET.parse('/home/judges/data/contests/' + getContestNum(contest) + ".xml", parser=parser)
    root = tree.getroot()
    for cur_name in root.iter('name'):
        cur_name.text = name
    for cur_name_en in root.iter('name_en'):
        cur_name_en.text = name_en
    
    if registerContest is not None:
        if len(list(root.iter('user_contest'))) == 0:
            child = ET.SubElement(root, 'user_contest')
        else:
            child = list(root.iter('user_contest'))[0]
        child.text = str(registerContest)
    tree.write('/home/judges/data/contests/' + getContestNum(contest) + '.xml', encoding='utf-8')

if __name__ == "__main__":
    # setContestXML(61, 'кек', 'kek')
    pass
