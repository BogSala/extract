from bs4 import BeautifulSoup
import yaml
import sys

from config import *

def toYaml(data): 
    with open(YAML_FILE_NAME + ".yaml", "w") as f:
        yaml.dump(data, f, default_flow_style=False)

def extractYamlFrom(file_path):
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

    replased = {}

    for tagSearch in TAGS_TO_EXTRACT:
        replased[tagSearch] = {}
        for tag in soup.find_all(tagSearch, string=True):
            tagType = tag.name
            previousString = tag.string.strip()
            previousStringLower = previousString.lower()
            tagText = previousStringLower.replace(" ", "_")
            newString = tagType + "." + tagText;
            tag.string = f'{{{newString}}}'

            if previousString:
                replased[tagSearch].update({tagText : previousString})

        if replased[tagSearch] == {}:
            replased.pop(tagSearch, None)

    toYaml(replased)

    if COPY_TWIG:
        file_path = file_path + '.copy' 

    with open(file_path, 'w') as f:
        f.write(soup.prettify())

extractYamlFrom(TWIG_FILE_NAME + '.twig')