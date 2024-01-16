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
if they're changed by an external host. This ultimately allows the interal system know whether to keep 
the old information or to request additional human supervision.





