# **G1 News Scraper**

## **INTRODUÇÃO**
- Scraper para extrair dados do site G1 (https://g1.globo.com/busca/).

## **Recursos**
- Extrai notícias do site G1 com base em critérios de pesquisa.
- Permite filtrar os artigos dentro de um intervalo de datas específico.
- Extrai vários campos de dados dos artigos, incluindo título, subtítulo, autor, data de publicação, conteúdo, região e link.
- Salva os dados coletados em um arquivo CSV.

## Dependências

O script requer as seguintes dependências:

- Python 3.x
- Biblioteca `requests`
- Biblioteca `lxml`



## **Instalação**
1. Clone o repositório:
```sh
git clone https://github.com/hermengardo/G1_news_scraper.git
```

2. Instale as dependências:
```sh
pip install -r requirements.txt
```

3. Edite e execute o arquivo `main.py`.

## Exemplo de uso
- Neste exemplo, o script irá procurar por notícias relacionadas à tecnologia no período de 1º a 31 de maio de 2023. Será adicionado um atraso de 0.5 segundos entre cada solicitação, e os dados coletados serão salvos no arquivo "dados.csv". Se ocorrerem erros de conexão, o script fará até 5 tentativas de solicitação e aguardará no máximo 60 segundos para uma resposta do servidor.

```python
from scraper import encontre_noticias


def main():
    encontre_noticias(busca="<campo de busca>",
                      inicio="01-01-2020",
                      fim="02-01-2020")


if __name__ == "__main__":
    main()
```

## **Parâmetros**
- A classe `encontre_noticias` aceita os seguintes parâmetros:
| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| busca | Sim | A consulta de pesquisa para encontrar notícias. Por exemplo, "tecnologia", "política", "esportes", etc. |
| inicio | Sim | A data de início do intervalo de pesquisa. Deve estar no formato "dd/mm/aaaa". |
| fim | Sim | A data de término do intervalo de pesquisa. Deve estar no formato "dd/mm/aaaa". |
| delay | Não | O atraso em segundos entre cada solicitação de página. É útil para evitar sobrecarregar o servidor. O valor padrão é 0.1 segundos. |
| filepath | Não | O caminho do arquivo CSV onde os dados coletados serão salvos. O valor padrão é "data.csv" e o arquivo será criado no diretório atual. |
| retry | Não | O número máximo de tentativas de solicitação em caso de perda de conexão. O valor padrão é 3. |
| timeout | Não | O tempo máximo em segundos para aguardar uma resposta do servidor. O valor padrão é 30 segundos. |
