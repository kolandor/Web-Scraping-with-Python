# A RegEx, or Regular Expression, is a sequence of characters that forms a search pattern.
# RegEx can be used to check if a string contains the specified search pattern.

# Python has a built-in package called re, which can be used to work with Regular Expressions
# Import the re module:
import re



def show_and_count_re(targetFile, regexPattern):
    try:
        print()
        with open(targetFile, "rt") as file:
            textFileData = file.read()
            
        result = re.findall(f"({regexPattern})", textFileData)
        
        if result:
            print(f"Result by pattern: {regexPattern}")
            print(f"Result count: {result.count}")
            print(f"Result items:")
            for item in result:
                print(f"\t{item[0]}")
        else:
            print(f"NO RESULT BY PATTERN: {regexPattern}")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        print()

if __name__ == '__main__':
    # Email validation
    # https://knowledge.validity.com/s/articles/What-are-the-rules-for-email-address-syntax?language=en_US
    #The recipient name may be a maximum of 64 characters long and consist of:
    #Uppercase and lowercase letters in English (A-Z, a-z)
    #Digits from 0 to 9
    #Special characters such as ! # $ % & ' * + - / = ? ^ _ ` { |
    fullEmailUsernamePattrern = r"[a-zA-Z\d][\w\.\!\#\$\%\&\'\*\+\/\=\?\^\-\`\{\}\|]+[a-zA-Z\d]"
    commonEmailUsernamePattrern = r"[a-zA-Z\d][\w\.\+\-]*[a-zA-Z\d]"

    #The domain name is a string of letters and digits that defines a space on the Internet owned and controlled by a specific mailbox provider or organization.
    #Domain names may be a maximum of 253 characters and consist of:
    #Uppercase and lowercase letters in English (A-Z, a-z)
    #Digits from 0 to 9 
    #A hyphen (-)
    #A period (.)  (used to identify a sub-domain; for example,  email.domainsample)
    domainPattrern = r"(([a-zA-Z\d][a-zA-Z\d\-]*[a-zA-Z\d]\.)+[a-zA-Z\d][a-zA-Z\d\-]*[a-zA-Z\d])"

    show_and_count_re("RegEx/regex training.txt", f"{commonEmailUsernamePattrern}@{domainPattrern}")

    # Date validation
    datePattern = r"(([0123]\d[\/\.\-][0123]\d[\/\.\-][012]\d\d\d)|([012]\d\d\d[\/\.\-][0123]\d[\/\.\-][0123]\d)|((January|February|March|April|May|June|July|August|September|October|November|December) [0123]\d, [012]\d\d\d))"

    show_and_count_re("RegEx/regex training.txt", datePattern)