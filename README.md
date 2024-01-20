# Web-scrape tracker

## Functionality
The package is divided into two scripts: `extract_divtag.py` and `div_checker.py`. The general purpose is to
track which search fields need human supervision to gradually reduce manual interference when running a crawler.
Below is a detailed breakdown of each script.

## extract_divtag.py

Input: a CSV file that contains desired fields (e.g. phone, address) with each row being a different entity.
Additionally, the last column must be a "special field" that contains the name of fields that were modified 
by a human. This should be saved after running the crawler & human inspection as it allows `extract_divtag.py`
to keep track of which fields need monitoring. `Resources.csv` is an example of such input file.

Output: a JSON file that contains a set of tuples per each location ID. 
A tuple contains:
1) The desired field 
2) The HTML element corresponding to the field
3) The content of the field

This JSON file can ultimately be used at a future date to quickly check if the tracked fields have changed.

## div_checker.py

Input: a JSON file formatted as detailed above.

Output: command line output(s) determining whether the content of the tracked fields remain the same or 
if they're changed by an external host. If the content is changed, the script automaitcally outputs the 
new content which can be integrated with a crawler to reduce human supervision in "refresh updates".

Note: all entities should be mapped through an ID

## tag_svm.ipynb

This file contains all the code for the main support vector machine ML model. The model takes labeled
input generated in a similar matter to `extract_divtag.py`. Features are extracted from the raw HTML
tag (raw text, tag attributes, text content) and vectorized approporiately. Large features like count-vectorized
HTML tags are ran through PCA to reduce runtime. After hyperparameter tuning, the model reaches ~90% classification
accruacy.




