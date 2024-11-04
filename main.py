import re
import requests

kategoria = input("Podaj nazwę kategorii: ").strip()
url = f'https://pl.wikipedia.org/wiki/Kategoria:{kategoria.replace(" ", "_")}'
html = requests.get(url).text

artykuly = re.findall(r'<li[^>]*>.*<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>.*</li>', html)[:3]

for link, tytul in artykuly:
    tresc_artykulu = requests.get("https://pl.wikipedia.org" + link).text

    poczatek = tresc_artykulu.find('<div id="mw-content-text"')
    koniec = tresc_artykulu.find('<div id="catlinks"')
    tresc = tresc_artykulu[poczatek:koniec] if poczatek != -1 and koniec != -1 else tresc_artykulu

    linki_wewnetrzne = re.findall(r'<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>', tresc)[:5]
    if linki_wewnetrzne:
        print(' | '.join(nazwa for _, nazwa in linki_wewnetrzne))

    obrazki = re.findall(r'<img[^>]*src=\"(//upload\.wikimedia\.org/[^"]+)\"[^>]*/>', tresc)[:3]
    if obrazki:
        print(' | '.join(obrazki))
    else:
        print('')

    poczatek_zrodel = tresc_artykulu.find('<h2 id="Przypisy">')
    if poczatek_zrodel != -1:
        koniec_zrodel = tresc_artykulu.find('<h2', poczatek_zrodel + 1)
        zrodla_html = tresc_artykulu[poczatek_zrodel:koniec_zrodel] if koniec_zrodel != -1 else tresc_artykulu[
                                                                                                poczatek_zrodel:]

        zrodla = re.findall(r'<a[^>]*class="external text"[^>]*href="([^"]+)"[^>]*>', zrodla_html)
        if zrodla:
            print(' | '.join(zrodla[:3]))
        else:
            print("")
    else:
        print("")

    kategorie = re.findall(r'<div id="catlinks"[^>]*>.*?<ul>(.*?)</ul>', tresc_artykulu, re.DOTALL)
    if kategorie:
        linki_kategorii = re.findall(r'<a[^>]*href=\"(/wiki/Kategoria:[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>',
                                     kategorie[0])[:3]
        if linki_kategorii:
            print(' | '.join(nazwa.replace('Kategoria:', '') for _, nazwa in linki_kategorii))
