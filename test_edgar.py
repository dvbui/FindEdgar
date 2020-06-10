from find_edgar import find_fiscal_year
import requests


def test_find_fiscal_year():
    r = requests.get("https://www.sec.gov/Archives/edgar/data/6201/000095013401002483/d84957e10-k405.txt")
    log_file = open("testing.txt","w")
    result = find_fiscal_year(r.text, True, log_file)
    log_file.close()
    if result == "":
        print("Test failed")
    else:
        print("Accepted")