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
- ```input_file``` (string): the path to the input file
- ```output_file``` (string): the path to the output file)
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
