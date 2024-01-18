import csv
import json
import requests
from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def find_divtag(url, input_text):
    response = requests.get(url)

    # http request success
    if response.status_code == 200:
        soup = bs(response.content, "html.parser")
        # return smallest html element that contains text (div/span/etc)
        result = [tag for tag in soup.find_all() if input_text in str(tag)]
        if not result:
            return ""
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
        # exclude last index since it's URL
        field_len = len(header) - 2 # change back to - 1 later

        # extract labeled input for SVM
        field_label = []    # supervised data
        html_tag = []   # feature for raw html tags
        tag_attrs = []  # feature for tag attributes
        for row in reader:
            print("Extracting features for clinic id " + row[0])
            i = 1
            while i < field_len:
                divtag = find_divtag(row[header.index('url')], str(row[i]))
                if divtag != "":
                    field_label.append(header[i])
                    html_tag.append(divtag)
                i+=1
        
        # numeric representation of the raw html tags
        vectorizer = CountVectorizer()
        html_features = vectorizer.fit_transform(html_tag).toarray()
        # attr_features = 

        print(field_label)


if __name__ == "__main__":
    main()