from scraper import encontre_noticias

def main():
    encontre_noticias(busca="Protesto ambiente",
                      inicio="01-01-2019",
                      fim="10-11-2019",
                      max_results=10)

if __name__ == "__main__":
    main()
