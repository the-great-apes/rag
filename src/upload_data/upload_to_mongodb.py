import json
import logging
import os
from write_data import write_document
from collections import defaultdict
from helpers import Summary, list_json_files

try:
    log_level = os.environ['LOG_LEVEL'].upper()
except KeyError:
    log_level = 'INFO'

log_level_mapping = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

logging.basicConfig(level=log_level_mapping.get(log_level, logging.WARNING))

DATA_PATH = "/app/data"
# Print the parsed data

COMPANY_REFS = ["ABB", "IBM", "PostFinance", "Raiffeisen", "Siemens", "UBS"]


def write_companies():
    write_document("companies", {"companies": list(data.keys())})

def write_years(comp: str):
    write_document(f"{comp}-years", {"years": list(data[comp].keys())})

def write_report(comp: str, year: str):
    write_document(f"{comp}-{year}", {"report": data[comp][int(year)].model_dump_json()})


def main():
    data = defaultdict(defaultdict)

    json_files = list_json_files(Path("data/summary"))

    for s in [Summary.load(f) for f in json_files]:
        data[s.company][s.year] = s

    write_companies()
    for c in data.keys():
        write_years(c)
        for y in data['c'].keys():
            write_report(c, y)
    

        
if __name__ == "__main__":
    main()