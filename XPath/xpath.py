# XPath uses path expressions to select nodes or node-sets in an XML document.
# The node is selected by following a path or steps.

import requests
from lxml import etree

def show_elements_by_xpath(url, xpath):
    try:
        print()
        # Get HTML response
        response = requests.get(url)
        # Parse HTML
        # htmlTree = etree.HTML(response.raw)
        # Find elements by XPath
        # xpathResult = htmlTree.xpath(xpath)

        # Create HTML parser
        htmlparser = etree.HTMLParser()
        # Parse HTML
        #htmlTree = etree.parse(response.raw, htmlparser)
        #xpathResult = htmlTree.xpath(xpath)

        html_root   = etree.fromstring(response.text, htmlparser)
        print(html_root.findall("body"))
        xpathResult = html_root.xpath(xpath)
        #print("Items finded by XPath:")
        for item in xpathResult:
            print(f"\t{item.text}")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        print()



if __name__ == "__main__":
    # //input[@id='text-input-what']
    # //input[@id='text-input-where']
    # //*[@id='jobsearch']//button OR //button[@class='yosegi-InlineWhatWhere-primaryButton']
    
    show_elements_by_xpath("https://br.indeed.com/", "input[@id='text-input-what']")