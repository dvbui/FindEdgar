import os

import requests
import xlrd
import edgar
from company import Company
import xlwt
from bs4 import BeautifulSoup

edg = edgar.Edgar()
oo = 1e9


def print_log(mess, log_file, verbose=True):
    if verbose:
        print(mess)
        if log_file is not None:
            log_file.write(mess+"\n")


def format_cik_file(input_file="cik.xlsx", output_file="cik.xlsx", verbose=True, log_file=None):
    cik_sheet = xlrd.open_workbook(input_file).sheet_by_index(0)

    if os.path.exists(output_file):
        os.remove(output_file)

    output_wb = xlwt.Workbook()
    output_sheet = output_wb.add_sheet('Sheet 1')

    cik_filter = {}
    log = None
    if verbose and (log_file is not None):
        log = open(log_file, "w")

    for i in range(0, cik_sheet.nrows):
        for j in range(0, cik_sheet.ncols):
            if str(cik_sheet.cell_value(i, j)).strip() == "":
                continue
            try:
                cik = str(int(cik_sheet.cell_value(i, j))).strip()
            except ValueError:
                mess = "{} is not a valid CIK".format(cik_sheet.cell_value(i, j))
                print_log(mess, log, verbose)

            while len(cik) < 10:
                cik = "0" + cik
            if cik in cik_filter:
                continue
            cik_filter[cik] = {}
            mess = "{} detected".format(cik)
            print_log(mess, log, verbose)

    row_cnt = 0
    for cik in cik_filter:
        output_sheet.write(row_cnt, 0, cik)
        row_cnt += 1

    output_wb.save(output_file)

    print_log("{} CIKs detected".format(len(cik_filter)), log, verbose)
    if log is not None:
        log.close()


def from_cik_to_company(cik_file="cik.xlsx", first_company=1, last_company=100, verbose=True,
                        log="from_cik_to_company_log.txt"):
    cik_sheet = xlrd.open_workbook(cik_file).sheet_by_index(0)
    companies = []
    cik_filter = {}
    log_file = None
    if verbose and not (log is None):
        log_file = open(log, "w")

    estimate_total = min(last_company - first_company + 1, cik_sheet.nrows*cik_sheet.ncols)
    company_cnt = 0
    for i in range(0, cik_sheet.nrows):
        for j in range(0, cik_sheet.ncols):
            if str(cik_sheet.cell_value(i, j)).strip() == "":
                continue
            try:
                cik = str(int(cik_sheet.cell_value(i, j))).strip()
            except ValueError:
                mess = "{} is not a valid CIK".format(cik_sheet.cell_value(i, j))
                print_log(mess, log_file, verbose)
                continue

            while len(cik) < 10:
                cik = "0"+cik
            if cik in cik_filter:
                continue
            cik_filter[cik] = {}

            company_cnt += 1
            if not (first_company <= company_cnt <= last_company):
                continue

            try:
                company_name = edg.get_company_name_by_cik(cik)
            except KeyError:
                mess = "{} is not a valid CIK".format(cik)
                print_log(mess, log_file, verbose)

            companies.append(Company(company_name, cik))
            mess = "#={}/{}, cik={}, company_name={}".format(len(companies), estimate_total, cik, company_name)
            print_log(mess, log_file, verbose)

    mess = "{} companies found".format(len(companies))
    print_log(mess, log_file, verbose)
    if log_file is not None:
        log_file.close()

    return companies


def get_bag_of_words(keyword_file="keyword.xlsx", verbose=True, log="get_bag_of_words_log.txt"):
    keyword_sheet = xlrd.open_workbook(keyword_file).sheet_by_index(0)
    keywords = []
    keywords_filter = {}
    log_file = None
    if verbose and not (log is None):
        log_file = open(log, "w")
    for i in range(keyword_sheet.nrows):
        for j in range(keyword_sheet.ncols):
            s = keyword_sheet.cell_value(i, j).strip().lower()
            if len(s) == 0:
                continue
            if s in keywords_filter:
                print_log("{} has already existed".format(s), log_file, verbose)
                continue

            keywords_filter[s] = {}
            keywords.append(s)

            print_log("\"{}\" detected".format(s), log_file, verbose)

    print_log("{} keywords found".format(len(keywords)), log_file, verbose)
    if log_file is not None:
        log_file.close()
    return keywords


row_num = 0


def check_string(string, keywords, verbose, sheet, url, log_file, company, fiscal_year):
    global row_num
    for word in keywords:
        if word in string.lower():
            if verbose:
                print_log("{}\n{}".format(word, string), log_file)
            sheet.write(row_num, 0, str(company.cik))
            sheet.write(row_num, 1, str(company.name))
            sheet.write(row_num, 2, fiscal_year)
            sheet.write(row_num, 3, str(url))
            sheet.write(row_num, 4, string[0:32767])
            row_num += 1
            return True
    return False


def find_fiscal_year(text):
    soup = BeautifulSoup(text)
    elements = soup.descendants
    fiscal_year = ""
    for element in elements:
        if hasattr(element, "extract"):
            element = element.extract()

        if hasattr(element, "get_text"):
            strings = element.get_text()
        else:
            strings = element.string
        if strings is None:
            continue
        strings = strings.split("\n\n")
        for string in strings:
            string = ' '.join(string.split('\n'))
            string = ' '.join(string.split()).strip()
            test_string = string.lower().split()
            string = string.split()
            for i in range(0, len(test_string)):
                test_string[i] = test_string[i].lower().strip()

            for i in range(max(0, len(test_string)-5)):
                if test_string[i:(i+3)] == ["fiscal", "year", "ended"]:
                    fiscal_year = ' '.join(string[(i+3):(i+6)])
                    while (len(fiscal_year) > 0) and (not (fiscal_year[-1].isdigit())):
                        fiscal_year = fiscal_year[:-1]
                    if fiscal_year != "":
                        break
            if fiscal_year != "":
                break

    return fiscal_year


def find_word(cik_file="cik.xlsx", keyword_file="keyword.xlsx",
              output_file="output.xlsx", first_company=1, last_company=100,
              verbose=True, log="find_word_log.txt",
              company_log_file="from_cik_to_company_log.txt",
              keyword_log_file="get_bag_of_words_log.txt"):

    if os.path.exists(output_file):
        os.remove(output_file)

    companies = from_cik_to_company(cik_file=cik_file, first_company=first_company,
                                    last_company=last_company, verbose=verbose, log=company_log_file)
    keywords = get_bag_of_words(keyword_file=keyword_file, verbose=verbose, log=keyword_log_file)

    log_file = None
    if verbose and (log is not None):
        log_file = open(log, "w")

    wb = xlwt.Workbook()
    sheet = wb.add_sheet("Sheet 1")

    global row_num
    row_num = 0

    current_company_id = 0
    for company in companies:
        current_company_id += 1

        print_log("#={}/{}, name={}".format(current_company_id, len(companies), company.name), log_file, verbose)
        tree = company.get_all_filings(filing_type="10-K")
        docs = Company.get_documents(tree, no_of_documents=100)

        current_document_num = 0
        for url in docs:
            current_document_num += 1
            print_log("doc={}/{}, url={}".format(current_document_num, len(docs), url), log_file, verbose)

            r = requests.get(url)
            soup = BeautifulSoup(r.text)
            elements = soup.descendants

            string_filter = {}

            fiscal_year = find_fiscal_year(r.text, verbose, log_file)

            if verbose:
                print_log("fiscal_year={}".format(fiscal_year), log_file)

            for element in elements:
                strings = element.string
                if strings is None:
                    continue
                strings = strings.split("\n\n")
                for string in strings:
                    string = ' '.join(string.split('\n'))
                    string = ' '.join(string.split()).strip()
                    if not (string in string_filter) and check_string(string, keywords, verbose, sheet, url,
                                                                      log_file, company, fiscal_year):
                        string_filter[string] = {}


    print_log("{} paragraphs matched".format(row_num), log_file, verbose)
    if log_file is not None:
        log_file.close()

    wb.save("{}".format(output_file))






