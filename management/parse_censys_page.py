import glob
import os

from bs4 import BeautifulSoup

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
        self.parser.add_argument("--input_dir", default="input/censys")
        self.parser.add_argument("--output_dir", default="output/censys")

    def execute(self):
        for name in map(os.path.basename, glob.glob(f"{self.args.input_dir}/*.html")):
            html = open(f"{self.args.input_dir}/{name}", 'r', encoding='utf-8')

            soup = BeautifulSoup(html, 'html.parser')
            result = {}
            key = ""
            for el in soup.find_all():
                if el.name == "h3":
                    key = el.contents[0].strip()
                    result[key] = []
                elif el.name == "b":
                    result[key].append(el.get_text(strip=True))
            for key, value in result.items():
                output_file_path = f'{self.args.output_dir}/{key.split("/")[-1].lower()}.txt'
                try:
                    with open(output_file_path, 'r') as file:
                        old_lines = file.readlines()
                except FileNotFoundError:
                    old_lines = []
                with open(output_file_path, 'w') as file:
                    file.writelines(sorted(set(old_lines + [el+"\n" for el in value])))

