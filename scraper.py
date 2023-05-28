import re
from time import sleep

import urllib3
import requests
from lxml import html

import utils


global BASE_URL, HEADER
BASE_URL = "https://g1.globo.com/busca/"
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
          "Accept": "*/*",
          "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
          "Accept-Encoding": "gzip, deflate, br"}


class encontre_noticias():
    def __init__(self,
                 busca,
                 inicio,
                 fim,
                 delay=0.1,
                 filepath="data.csv",
                 retry=3,
                 timeout=30):
        since = utils.convert_to_datetime(inicio)
        until = utils.convert_to_datetime(fim)
        self.busca = busca
        self.base_query = {"q": busca,
                           "page": 1,
                           "order": "recent",
                           "from": since,
                           "to": until,
                           "species":"notícias",
                           "ajax": "1"}
        self.filepath = filepath
        self.delay = delay
        self.count = 0
        self.retry = retry
        self.retry_count = 0
        self.timeout = timeout
        utils.clean_file(self.filepath)
        self.pipeline()

    def pipeline(self) -> None:
        while True:
            try:
                tree = self.load_feed()
                if self.check_end_page(tree):
                    print('Fim da coleta.')
                    break
                articles = self.find_urls(tree)
                for article in articles:
                    self.scrape_content(article)
                    sleep(self.delay)
                self.base_query['page'] += 1
                self.retry_count = 0  # Reset the retry count if the request is successful
            except requests.exceptions.RequestException:
                self.retry_count += 1
                if self.retry_count > self.retry:
                    print("Número máximo de tentativas excedido. Fechando conexão...")
                    break
                print(f"Perda de conexão... Nova tentativa em {self.timeout} segundos")
                sleep(self.timeout)
                continue

    def load_feed(self) -> html.HtmlElement:
        response = requests.request("GET", BASE_URL, params=self.base_query, headers=HEADER)
        return utils.html_parser(response)

    def load_page(self, url: str) -> html.HtmlElement:
        response = requests.request("GET", url, headers=HEADER)
        return utils.html_parser(response)

    def find_urls(self, tree: html.HtmlElement) -> list:
        urls = [utils.decode_url(a.get('href')) for a in tree.cssselect('a.widget--info__media')]
        return self.url_is_valid(urls)

    def scrape_content(self, article) -> None:
        data = {}
        # Carrega a página
        article_tree = self.load_page(article)
        if self.article_is_valid(article_tree):
            # Extrai dados (campos não fixos)
            data['subtitulo'] = self.get_data(article_tree, 'h2[class=content-head__subtitle]')
            data['autor'] = self.get_data(article_tree, 'p[class=content-publication-data__from]')
            # Extrai dados (campos fixos)
            data['data'] = self.get_data(article_tree, 'time[itemprop=datePublished]', 'datetime')
            data['titulo'] = self.get_data(article_tree, 'div[class=title] > meta[itemprop=name]', 'content')
            data['conteudo'] = self.get_media_content(article_tree, 'div.mc-column.content-text.active-extra-styles')
            data['regiao'] = utils.extract_UF_from_url(article)
            data['link'] = article
            data['busca'] = self.busca
            self.count += 1
            print(f'Coletado: {self.count} | {data["titulo"][:30]}... | {data["autor"]}')
            # Salva os dados
            utils.save_data_to_csv(data=data, filepath=self.filepath)
        else:
            return None

    def get_data(self, article_tree: html.HtmlElement, css_selector: str, attribute=None) -> str:
        try:
            if attribute:
                return article_tree.cssselect(css_selector)[0].get(attribute)
            else:
                return article_tree.cssselect(css_selector)[0].text
        except IndexError:
            return 'nan'

    def get_media_content(self, article_tree: html.HtmlElement, css_selector: str) -> str:
        try:
            text = [txt.xpath('.//text()') for txt in article_tree.cssselect(css_selector)]
            text = utils.normalize_text(text)
            return text
        except IndexError:
            return 'nan'

    def check_end_page(self, tree: html.HtmlElement) -> bool:
        element = tree.cssselect('section[id="content"]')
        if len(element) > 0:
            return True
        return False

    def article_is_valid(self, article: html.HtmlElement) -> bool:
        element = article.cssselect('div[id="page-video-wrapper"]')
        if len(element) > 0:
            return False
        return True

    def url_is_valid(self, urls: list) -> list:
        pattern = r"g1\.globo\.com\/[a-zA-Z]{2}\/"
        return [url for url in urls if re.search(pattern, url)]
