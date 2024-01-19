import csv
import json
import requests
from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import accuracy_score
import pandas as pd

def find_divtag(url, input_text):
    try: 
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
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
def clean_csv():
    # read in largest scraping dataset
    df = pd.read_csv('resources_large.csv', sep=";")
    columns_to_keep = ['resource_id', 'name', 'address_1', "zip", "Phone Number", "Website where info found"]  # Replace with your actual column names

    # create a new df with only the essential fields
    df_filtered = df[columns_to_keep]
    df_cleaned = df_filtered.rename(columns={"Website where info found": "url", "address_1": "address"}).dropna(subset=["url"])
    print("Sample dataset size: " + str(df_cleaned.shape))

    # option to export small subset temporarily only for testing
    df_small = df_cleaned.head(300)
    df_small.to_csv('resources_cleaned.csv', sep=";", index=False)

def train_svm_model(x, y):
    # Manually split the data into 70% training and 30% testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Create an SVM classifier
    svm_classifier = svm.SVC(kernel='linear', C=1)

    # Define the stratified k-fold cross-validator with 5 folds
    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Perform cross-validation on the training set and get accuracy scores
    accuracy_scores = cross_val_score(svm_classifier, X_train, y_train, cv=kf)

    # Print the accuracy scores for each fold
    for fold, accuracy in enumerate(accuracy_scores, start=1):
        print(f'Fold {fold}: Accuracy = {accuracy:.2f}')

    # Calculate and print the average accuracy across all folds
    average_accuracy = accuracy_scores.mean()
    print(f'Average Accuracy: {average_accuracy:.2f}')

    # Now you can train and evaluate the model on the test set
    svm_classifier.fit(X_train, y_train)
    test_accuracy = svm_classifier.score(X_test, y_test)
    print(f'Test Accuracy: {test_accuracy:.2f}')

def main():
    clean_csv()
    data = {}
    file_input = input("Enter a CSV containing clinic data: ")
    with open(file_input, mode='r') as file:
        reader = csv.reader(file, delimiter=";")
        # print field types
        header = next(reader, None)
        if header:
            print(f"Fields: {header}") 
        # exclude last index since it's URL
        field_len = len(header) - 1 

        # extract labeled input for SVM
        field_label = []    # supervised data
        html_tag = []   # feature for raw html tags
        tag_attrs = []  # feature for tag attributes
        for row in reader:
            print("Extracting features for clinic id " + row[0])
            i = 1
            while i < field_len:
                divtag = find_divtag(row[header.index('url')], str(row[i]))
                if divtag is None:
                    break
                elif divtag != "":           
                    field_label.append(header[i])
                    html_tag.append(divtag)
                    tag_attrs.append(bs(divtag, 'html.parser').find().attrs)
                i+=1
        
        # convert labels to numbers
        labels = []
        for i in range(len(field_label)):
            field = field_label[i]
            if field == "name":
                labels.append(0)   
            elif field == "address":
                labels.append(1)   
            elif field == "zip":
                labels.append(2)   
            else:
                labels.append(3)
                       
        # numeric representation of the raw html tags
        vectorizer = CountVectorizer()
        html_features = vectorizer.fit_transform(html_tag).toarray()

        # extract relevant attribute features that's indicative of field classification
        df = pd.DataFrame(tag_attrs)
        print(field_label)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        # sort by most avail entries
        nan_counts = df.isna().sum()
        count_sort_col = nan_counts.sort_values().index
        df_ordered = df[count_sort_col]
        print(df_ordered.iloc[:, :5])

        # add both feature matrices
        feature_matrix = []
        for i in range(len(html_features)):
            feature_matrix.append(html_features[i] + df_ordered[i])

        train_svm_model(feature_matrix, field_label)




if __name__ == "__main__":
    main()