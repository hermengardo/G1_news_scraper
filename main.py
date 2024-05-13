from scraper import encontre_noticias

def main():
    encontre_noticias(busca="lula",
                      inicio="01-01-2014",
                      fim="10-11-2014",
                      max_results=10)

if __name__ == "__main__":
    main()
