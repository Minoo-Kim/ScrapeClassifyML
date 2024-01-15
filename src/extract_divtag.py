import csv
import json
import requests
from bs4 import BeautifulSoup as bs

def find_divtag(url, input_text):
    response = requests.get(url)

    # http request success
    if response.status_code == 200:
        soup = bs(response.content, "html.parser")
        # return smallest html element that contains text (div/span/etc)
        result = [tag for tag in soup.find_all() if input_text in str(tag)]
        if not result:
            return "No such element exists"
        else: 
            return str(min(result, key=lambda element: len(str(element.get_text(strip=True)))))
    # http request failed
    else:
        print(f"Status code: {response.status_code}. Failed to retrieve content from {url}.")
        return None
    
def main():
    data = {}
    file_input = input("Enter a CSV containing clinic data: ")
    with open(file_input, mode='r') as file:
        reader = csv.reader(file, delimiter=";")
        # print field types
        header = next(reader, None)
        if header:
            print(f"Fields: {header}")  

        # return divtag(s) for each "human-modified" field(s)      
        for row in reader:
            print('\n\nProcessing clinic id ' + row[0])
            divtag_list = []

            if row[-1] == "":
                print("No fields need to be manually checked\n")
            else:
                modified_fields = row[-1]
                for field in modified_fields.split(","):
                    modified_str = row[header.index(field)]
                    print('\nreturning divtag of: ' + field)

                    divtag = find_divtag(row[header.index('url')], str(modified_str))
                    divtag_list.append((field, divtag))
                    print(divtag)
            data[row[0]] = [divtag_list, row[header.index('url')]]

    # output JSON containing extracted div tags  
    json_object = json.dumps(data, indent=4)
 
    # Writing to sample.json
    with open("divtags.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    main()