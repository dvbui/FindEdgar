# FindEdgar
## Input
- Header row should not be included in the input files.
### CIK file: ```cik.xlsx```
- The CIK file should have one column; each cell in the column contains exactly one CIK number.
- CIK numbers do not need to be distinct.
- Open ```cik.xlsx``` to see an example of a correct ```cik.xlsx``` file
### Keyword file ```keyword.xlsx```
- The keyword file should have one column; each cell in the column contains exactly one keyword.
- The keywords can contain spaces and do not need to be distinct
- Open ```keyword.xlsx``` to see an example of a correct ```keyword.xlsx``` file 
## Output
### ```output.xlsx```
- ```output.xlsx``` has multiple rows, each row has 6 cells
    - Cell 1: CIK number
    - Cell 2: Company name
    - Cell 3: Fiscal year-end
        - If this cell is empty, you need to open the K-10 form to find the fiscal year-end.
    - Cell 4: List of matched words
    - Cell 5: HTTPS link to the K-10 form
    - Cell 6: The paragraph that has one of the keywords (case-insensitive)
## Usage
### Start Edgar
```python3 -i find_edgar.py```
### Standardize ```cik.xlsx```
```def format_cik_file(input_file="cik.xlsx", output_file="cik.xlsx", verbose=True, log_file=None)```
#### Parameters
- ```input_file``` (string): the path to the original CI file
- ```output_file``` (string): the path to the new CIK file
- ```verbose``` (boolean): ```True``` if you want the method to print its progress, otherwise ```False```
- ```log_file``` (string): the path to the log file. 
    - This file contains what is printed to the screen during the method's execution.
#### Sample Usage
```
# create a new, standardized cik.xlsx and delete the old cik.xlsx
format_cik_file()

# the new, standardized cik file should be cik_formatted.xlsx and keep the old cik.xlsx
format_cik_file(output_file="cik_formatted.txt")

# the original cik file is input.xlsx, the new cik file is cik_formatted, and you do not want to see the method's progress
format_cik_file(input_file="input.xlsx", output_file="cik_formatted.xlsx", verbose=False)
```
### Find paragraphs
```def find_word(cik_file="cik.xlsx", keyword_file="keyword.xlsx", output_file="output.xlsx", first_company=1, last_company=100, verbose=True, log="find_word_log.txt", company_log_file="from_cik_to_company_log.txt", keyword_log_file="get_bag_of_words_log.txt")```
#### Parameters
- ```cik_file``` (string): the path to the CIK file
- ```keyword_file``` (string): the path to the keyword file
- ```output_file``` (string): the path to the output file
- ```first_company``` (int): the index of the first company
- ```last_company``` (int): the index of the last company
    - The companies are numbered from 1 according to the order they appear in the CIK file. If **the CIK are distinct**, the i-th company will be on row i-th of the file 
- ```verbose``` (boolean): ```True``` if you want the method to print its progress, otherwise ```False```
- ```log``` (string): the path to the log file of ```find_word()```
- ```company_log_file``` (string): the path to the log file of ```from_cik_to_company()```
- ```keyword_log_file``` (string): the path to the log file of ```get_bag_of_words()```
#### Sample Usage
```
# find the paragraphs in the K-10s of the first 100 companies in the cik file
find_word()

# find the paragraphs in the K-10s of the companies whose index is between 101 and 200
find_word(first_company=101, last_company=200)

# find the paragraphs in the K-10s of the companies whose index is between 101 and 200, and the cik file is "cik_formatted.clsx"
find_word(cik_file="cik_formatted.clsx", first_company=101, last_company=200)
```
