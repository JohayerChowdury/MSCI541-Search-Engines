# Program to extract queries from topics.401-450.txt file

import xml.etree.ElementTree as ET
from pathlib import Path

topics_file_path = '../../../TREC_LATimes_Data/topics.401-450-xml.txt'

tree = ET.parse(topics_file_path)
root = tree.getroot()

with open('queries.txt', 'w') as f:
    for topic in root.findall('topic'):
        topic_number = topic.find('number').text
        if int(topic_number) not in [416, 423, 437, 444, 447]:
            title_text = topic.find('title').text
            title_text = title_text.replace('\n', '')
            f.write(topic_number + '||' + title_text + '\n')