from collections import defaultdict
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .helpers import Summary, list_json_files

# --------------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------------

data = defaultdict(defaultdict)

json_files = list_json_files(Path("data/summary"))

for s in [Summary.load(f) for f in json_files]:
    data[s.company][s.year] = s

# --------------------------------------------------------------------------------
# app
# --------------------------------------------------------------------------------

app = FastAPI()

# --------------------------------------------------------------------------------
# rest services
# --------------------------------------------------------------------------------

# this is a bad idea
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/companies")
def get_companies():
    return {"companies": list(data.keys())}


@app.get("/api/{comp}/years")
def get_years(comp: str):
    return {"years": list(data[comp].keys())}


@app.get("/api/{comp}/{year}")
def get_report(comp: str, year: str):
    return {"report": data[comp][int(year)].model_dump_json()}


# --------------------------------------------------------------------------------
# start service
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
