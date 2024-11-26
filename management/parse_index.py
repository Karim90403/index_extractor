from management.base.base_command import BaseCommand
import json
from typing import TextIO


class Command(BaseCommand):
    help: str = "Extract values from elastic index to files(protocols as names)"

    def add_arguments(self):
        """
        Add arguments for command(input_dir, output_dir)
        Returns:
            Nane
        """
        self.parser.add_argument("--input_dir", default="input")
        self.parser.add_argument("--output_dir", default="output/actual_index")

    @classmethod
    def extract_mappings(cls, parent: str, item: dict, output: TextIO):
        for key, value in item.items():
            if key == "properties" or key == "fields":
                cls.extract_mappings(parent, value, output)
            elif key == "type":
                output.write(f"{parent}: {value}\n")
            elif isinstance(value, dict):
                cls.extract_mappings(".".join((parent, key)) if parent else key, value, output)

    def execute(self):
        input_file_path = f'{self.args.input_dir}/actual_index.json'

        data = json.load(open(input_file_path, 'r', encoding='utf-8'))

        for key, value in data.get("mappings", {}).get("properties", {}).get("services", {}).get("properties",
                                                                                                 {}).items():
            output_file_path = f'{self.args.output_dir}/{key}.txt'
            self.extract_mappings(f"services.{key}", value, open(output_file_path, 'w'))
