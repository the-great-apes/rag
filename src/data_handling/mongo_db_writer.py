import json
import logging
import os
from company_data import create_revenue_entry, get_company_data
from write_data import write_document

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


# Print the parsed data

COMPANY_REFS = ["ABB", "IBM", "PostFinance", "Raiffeisen", "Siemens", "UBS"]

def main():
    logging.info("Starting LLM Service")
    for company_ref in COMPANY_REFS:
        revenue = create_revenue_entry("CHF", 1000000000)
        data = get_company_data(company_ref, revenue)
        write_document(company_ref, data)

        
if __name__ == "__main__":
    main()