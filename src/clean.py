from pathlib import Path
import re

import yaml
from tqdm import tqdm

from .helpers import Report, list_json_files

########################################################################################
# helper funcs
########################################################################################


def clean_report(report: Report) -> Report:
    """
    Clean Report content

    :param report: dirty report.
    :return: clean report object.
    """
    # Remove tags
    report.content = re.sub(r"<!--.*?-->", "", report.content, flags=re.DOTALL)

    # Remove newline characters
    report.content = re.sub(r"\n", " ", report.content)

    # Replace multiple spaces with a single space
    report.content = re.sub(r"\s+", " ", report.content)

    # Strip leading and trailing whitespace
    report.content = report.content.strip()

    return report


########################################################################################
# main
########################################################################################


def main():
    cfg = yaml.safe_load(open("params.yaml"))
    path_i = Path(cfg["data"]["parsed"])
    path_o = Path(cfg["data"]["clean"])

    # parse files
    files = list_json_files(path_i)
    reports = [Report.load(f) for f in files]
    reports = [clean_report(r) for r in reports]

    # dump
    path_o.mkdir(parents=True, exist_ok=True)
    for r in tqdm(reports):
        with open(path_o / f"{r.year}_{r.company}.json", "w") as f:
            f.write(r.model_dump_json())


if __name__ == "__main__":
    main()
