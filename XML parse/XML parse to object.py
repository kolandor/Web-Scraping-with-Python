# XML Parse lib
import json
import xml.etree.ElementTree as ET

#Parsing XML Function
#pass through all children
def xml_parse_sample():
    # ElementTree represents the whole XML document as a tree and
    # Element represents a single node in this tree.
    xmlTree = ET.parse('XML parse/XML sample.xml')
    
    # Get root
    root = xmlTree.getroot()
    
    # Store result
    result = []
    
    for child in root:# Get childs from root
        for subChild in child:# Get sub childs
            if subChild.tag == 'fact':# Get specified node
                result.append(subChild.text)
    
    # Write result to file
    with open('xml facts result.txt', 'wt') as file:
        # Concatenate any number of strings.
        file.write('\n'.join(result))

#Parsing XML Function
#By finding current nodes
def xml_parse_sample2():
    tree = ET.parse('XML parse/XML sample.xml')
    
    # Get root
    root = tree.getroot()
    infos = root.findall('info')
    
    # Store result
    result = []
    
    for info in infos:
        #Find current node
        fact = info.find('fact')
        result.append(fact.text)
    
    # Write result to file
    with open('xml facts result 2.txt', 'wt') as file:
        # Concatenate any number of strings.
        file.write('\n'.join(result))

def xml_to_json_file():
    tree = ET.parse('XML parse/XML sample.xml')
    
    # Get root
    root = tree.getroot()
    infos = root.findall('info')
    
    # Store result
    result_dict = {}
    
    # Dictionary objects must have unique keys, 
    # and since uniqueness is not required in XML, 
    # I add a number to the name of each tag
    for i, info in enumerate(infos):
        sub_dict = {}
        for j, subNode in enumerate(info):#iterating over sub nodes
            sub_dict[f"{subNode.tag}{j}"] = subNode.text
        result_dict[f"{info.tag}{i}"] = sub_dict
    
    with open('JSON form XML result.json', 'w') as file:
        json.dump(result_dict, file)#Save to JSON file
        
    with open('JSON form XML result.json', 'r') as file:
        result_from_json = json.load(file)#Load from JSON file

    print(result_from_json, type(result_from_json))

    print(result_dict == result_from_json)

# Entry point
if __name__ == '__main__':
    # xml_parse_sample()
    # xml_parse_sample2()
    xml_to_json_file()