# **G1 Scraper** 📰

## **Introdução**
- Raspador de dados para o site [G1](https://g1.globo.com/busca/).

## **Recursos**
- Extrai notícias do site G1 com base em critérios de pesquisa.
- Permite filtrar os artigos dentro de um intervalo de datas específico.
- Extrai vários campos de dados dos artigos, incluindo título, subtítulo, autor, data de publicação, conteúdo, região e link.
- Salva os dados coletados em um arquivo CSV.

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

## **Exemplo de uso**
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
| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| busca | Sim | A consulta de pesquisa para encontrar notícias. Por exemplo, "tecnologia", "política", "esportes", etc. |
| inicio | Sim | A data de início do intervalo de pesquisa. Deve estar no formato "dd-mm-aaaa". |
| fim | Sim | A data de término do intervalo de pesquisa. Deve estar no formato "dd-mm-aaaa". |
| delay | Não | O atraso em segundos entre cada solicitação de página. É útil para evitar sobrecarregar o servidor. O valor padrão é 0.1 segundos. |
| filepath | Não | O caminho do arquivo CSV onde os dados coletados serão salvos. O valor padrão é "data.csv" e o arquivo será criado no diretório atual. |
| retry | Não | O número máximo de tentativas de solicitação em caso de perda de conexão. O valor padrão é 3. |
| timeout | Não | O tempo máximo em segundos para aguardar uma resposta do servidor. O valor padrão é 30 segundos. |

## **Campos disponíveis**
| Campo | Descrição |
|-------|-----------|
| data | A data de publicação do artigo. |
| titulo | O título do artigo. |
| subtitulo | O subtítulo do artigo. |
| autor | O autor do artigo. |
| conteudo | O conteúdo do artigo. |
| regiao | A região associada ao artigo. |
| link | O link para o artigo. |
| busca | A consulta associada ao artigo. |
