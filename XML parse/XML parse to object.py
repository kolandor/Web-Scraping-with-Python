# XML Parse lib
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

# Entry point
if __name__ == '__main__':
    xml_parse_sample()
    xml_parse_sample2()