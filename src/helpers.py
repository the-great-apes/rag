from pydantic import BaseModel
from pathlib import Path
from openai import AzureOpenAI
from groq import Groq
import os
import yaml


cfg = yaml.safe_load(open("params.yaml"))
PROMPTS = cfg["extraction"]["templates"]

if cfg['use_openai']:
    LLM = cfg['models']['openai']
    client = AzureOpenAI(
    api_key = LLM["api_key"],  
    api_version = LLM['api_version'],
    azure_endpoint = LLM['azure_endpoint']
    )
else:
    LLM = cfg['models']['groq']    
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )




########################################################################################
# pydantic classes
########################################################################################
class Chunk(BaseModel):
    id: str
    content: str


class Report(BaseModel):
    company: str
    year: int
    content: str
    chunks: list[Chunk] = []

    def save(self, dir_path: Path) -> None:
        dir_path.mkdir(parents=True, exist_ok=True)
        with open(dir_path / f"{self.year}_{self.company}.json", "w") as f:
            f.write(self.model_dump_json())

    @classmethod
    def load(cls, file_path: Path) -> "Report":
        """
        Parse JSON Object into Report.

        :param file_path: The path to a json report.
        :return: Report object.
        """
        with open(file_path, "r") as f:
            return Report.model_validate_json(f.read())


class Driver(BaseModel):
    """Data model for revenue drivers."""

    content: str
    context: list[str]


class KPI(BaseModel):
    """Data model for a KPI."""

    name: str
    value: float
    currency: str
    context: str
    driver: Driver


class Summary(BaseModel):
    """Data model for a Summary."""

    company: str
    year: int
    kpis: list[KPI]
    overall_summary: str = ""


    def create_summary(self):
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": PROMPTS['summary'].format(
                    company=self.company,  year=self.year, kpis=self.kpis,)}
            ],
            model=LLM['deployment_name'],
            max_tokens=512
        )
        self.overall_summary = response.choices[0].message.content.strip()


    def save(self, dir_path: Path) -> None:
        dir_path.mkdir(parents=True, exist_ok=True)
        with open(dir_path / f"{self.year}_{self.company}.json", "w") as f:
            f.write(self.model_dump_json())

    @classmethod
    def load(cls, file_path: Path) -> "Summary":
        """
        Parse JSON Object into Summary.

        :param file_path: The path to a json summary.
        :return: Summary object.
        """
        with open(file_path, "r") as f:
            return Summary.model_validate_json(f.read())


########################################################################################
# helper funcs
########################################################################################
def list_json_files(directory: Path) -> list:
    """
    Lists all JSON files in the specified directory.

    :param directory: The directory to search for JSON files.
    :return: A list of JSON file paths.
    """
    path = Path(directory)
    json_files = [file for file in path.rglob("*.json")]
    return json_files
