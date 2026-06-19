import os
import json
import csv
import glob
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def convert_html_to_csv(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    pre_tag = soup.find('pre')
    if pre_tag:
        json_data = pre_tag.text.strip()
        try:
            data = json.loads(json_data)
            records = data['Data']
            if records:
                csv_headers = records[0].keys()
                return records, csv_headers
            else:
                return [], []
        except json.JSONDecodeError:
            return None, None
    else:
        return None, None


def convert_html_files_to_csv(html_directory, output_folder, Ns):
    os.makedirs(output_folder, exist_ok=True)

    for html_file in glob.glob(os.path.join(html_directory, '*.html')):
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Ns=1: los comentarios de texto libre pueden tener \n embebidos
        if Ns == 1:
            html_content = html_content.replace('\\n', ' ')

        records, csv_headers = convert_html_to_csv(html_content)

        if records and csv_headers:
            filename = os.path.splitext(os.path.basename(html_file))[0]
            csv_file = os.path.join(output_folder, f'{filename}.csv')

            with open(csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                writer.writeheader()
                writer.writerows(records)

            logger.info("CSV file '%s' has been created successfully.", csv_file)
        else:
            logger.warning("No valid JSON data found in %s. Skipping...", html_file)
