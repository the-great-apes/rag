import json
from pathlib import Path

import yaml
from tqdm import tqdm

from .helpers import Report, list_json_files

########################################################################################
# helper funcs
########################################################################################


def parse_report(file_path: Path) -> Report:
    """
    Parse JSON Object into Report.

    :param file_path: The path to a json report.
    :return: Report object.
    """
    path = Path(file_path)
    year = int(path.stem)
    company = path.parent.name
    with open(path) as f:
        content = json.load(f)["analyzeResult"]["content"]
        return Report(company=company, year=year, content=content)


########################################################################################
# main
########################################################################################


def main():
    cfg = yaml.safe_load(open("params.yaml"))
    path_i = Path(cfg["data"]["raw"])
    path_o = Path(cfg["data"]["parsed"])

    # parse files
    files = list_json_files(path_i)
    reports = [parse_report(f) for f in files]

    # dump
    path_o.mkdir(parents=True, exist_ok=True)
    for r in tqdm(reports):
        with open(path_o / f"{r.year}_{r.company}.json", "w") as f:
            f.write(r.model_dump_json())


if __name__ == "__main__":
    main()
