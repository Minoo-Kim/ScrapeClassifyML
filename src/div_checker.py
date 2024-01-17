import json
import requests
from bs4 import BeautifulSoup as bs

def extract_text(tag):
    return tag.get_text(strip=True)

def checkDiv(url, divtags, id):
    response = requests.get(url)

    # http request sucess
    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')
        
        # Find the element in the parsed HTML for every field
        for divtag in divtags:
            if soup.find(lambda tag: str(tag) == divtag[1]):
                print(divtag[0] + " for location ID " + id +  " is unchanged")
            else:
                # fetch new field content
                prev_attr = bs(divtag[1], 'html.parser').find().attrs
                curr_tag = soup.find(**prev_attr)
                curr_content = extract_text(curr_tag)
                if curr_content == "":
                    curr_content = "[uncommon tag identified, manually check]"
                print(divtag[0] + " for location ID " + id +  " is changed. Please update to " + curr_content)
    # http request failed
    else:
        print(f"Status code: {response.status_code}. Failed to retrieve content from {url}.")
        return None
    
def main():
    # Read data from the JSON file; loop through each clinic
    with open("./divtags.json", 'r') as file:
        data = json.load(file)
        for location in data:
            checkDiv(data[location][1], data[location][0], location)

if __name__ == "__main__":
    main()
