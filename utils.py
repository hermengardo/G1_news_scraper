import csv
import re

from datetime import datetime
from os import path, remove
from urllib.parse import unquote

from lxml import html
from requests import models


def convert_to_datetime(date_string: str) -> str:
    datetime_object = datetime.strptime(date_string, "%d-%m-%Y")
    formatted_datetime = datetime_object.strftime("%Y-%m-%dT%H:%M:%S%z-0300")
    return formatted_datetime


def html_parser(response: models.Response) -> html.HtmlElement:
    return html.fromstring(response.content.decode('utf-8'))


def decode_url(url: str) -> str:
    transformed_url = re.search(r'(?<=u=)(.*?)(?=&syn)', url).group(0)
    decoded_url = unquote(transformed_url)
    return decoded_url


def extract_UF_from_url(url: str) -> str:
    pattern = r"\/([a-z]{2})\/([a-z\-]+)\/"
    match = re.search(pattern, url)
    if match:
        state_code = match.group(1).upper()
        state_name = match.group(2).replace("-", " ").title()
        return f"{state_code} - {state_name}"
    else:
        return "nan"


def normalize_text(news: list) -> str:
    normalized = ' '.join([item for sublist in news for item in sublist]).strip()
    return normalized


def clean_file(file: str) -> None:
    if path.exists(file):
        remove(file)


def save_data_to_csv(data: dict, filepath: str) -> None:
    csv_file_exists = path.isfile(filepath)

    with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['titulo',
                      'subtitulo',
                      'conteudo',
                      'tópicos',
                      'autor',
                      'regiao',
                      'data',
                      'link',
                      'busca']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not csv_file_exists:
            writer.writeheader()

        writer.writerow(data)
