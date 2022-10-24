import requests
from bs4 import BeautifulSoup
import sqlite3 as sql
from flask import Flask, render_template


def database_sil():
    con = sql.connect("firstDatabase.db")
    cur = con.cursor()
    cur.execute("delete from bilgisayar")
    con.commit()


database_sil()


def hb_notebook():
    i = 0

    basliks = []
    islemcis = []
    rams = []
    isletims = []
    models = []
    islemci_models = []
    disks = []
    ekran = []
    prices = []
    imgs = []
    list1 = []
    list2 = []
    links1 = []
    sayfalar = [1,2]
    for sayfa in sayfalar:
        url = 'https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98' + '?sayfa=' + str(sayfa)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/106.0.0.0 Safari/537.36 '
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        urunler = soup.findAll("li", attrs={"class": "productListContent-zAP0Y5msy8OHn5z7T_K_"})
        ur_p = soup.find_all("div", {"data-test-id": "price-current-price"})
        ur_i = soup.find_all("div", {"data-test-id": "product-image-image"})
        for im in ur_i:
            img1 = im.img.get("src")
            imgs.append(img1)

        for urun in urunler:
            baslik = urun.a.get("title")
            # print(str(i) + " " + baslik)
            basliks.append(baslik)
            linb = "https://www.hepsiburada.com"
            lins = urun.a.get("href")
            if str(lins).startswith("https://adservice"):
                links = lins
                links1.append(links)
            else:
                links = linb + lins
                links1.append(links)
        for p in ur_p:
            price = p.text
            prices.append(price)
    # print(links1)
    # print(prices)
    # print(imgs)

    for i in range(len(links1)):
        URL = links1[i]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/106.0.0.0 Safari/537.36"}
        sayfa = requests.get(URL, headers=headers)
        icerik = BeautifulSoup(sayfa.content, 'html.parser')
        urunAdi = icerik.find("table", {"class": "data-list tech-spec"})
        urunAdi2 = urunAdi.find_all("th")
        urunAdi3 = urunAdi.find_all("td")

        for list in urunAdi2:
            list1.append(list.text)
        for list3 in urunAdi3:
            list2.append(list3.text)

    for j in range(len(list2)):
        if list1[j] == "İşlemci Tipi":
            islemcis.append(list2[j])
        elif list1[j] == "İşlemci":
            islemci_models.append(list2[j])
        elif list1[j] == "İşletim Sistemi":
            isletims.append(list2[j])
        elif list1[j] == "Ram (Sistem Belleği)":
            rams.append(list2[j])
        elif list1[j] == "SSD Kapasitesi":
            disks.append(list2[j])
        elif list1[j] == "Ekran Boyutu":
            ekran.append(list2[j])
    connection = sql.connect("FirstDatabase.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS bilgisayar (marka TEXT,model_no  TEXT,isletim_sistemi  TEXT,islemci_tipi 
   TEXT, islemci_nesli  TEXT,ram  TEXT,ekran_boyut TEXT,disk_tur TEXT,disk_boyut  TEXT,fiyat TEXT,link TEXT,resim TEXT,Site TEXT)""")
    ekle = """INSERT INTO bilgisayar (marka,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,ekran_boyut,disk_tur,disk_boyut,fiyat,link,resim,site)  VALUES(
   ?,?,?,?,?,?,?,?,?,?,?,?,?) """
    for k in range(len(links1)):
        cursor.execute(ekle, (
            basliks[k], " ", isletims[k].strip(), islemcis[k].strip(), islemci_models[k].strip(), rams[k].strip(),
            ekran[k].strip(), "SSD", disks[k].strip(),
            prices[k], links1[k], imgs[k], "Hepsiburada"))
        connection.commit()


hb_notebook()


def vt():
    names = []
    links = []
    rams = []
    isletims = []
    models = []
    islemcis = []
    islemci_models = []
    disks = []
    imgs = []
    prices = []
    markas = []
    disktur = []
    ekran = []

    for sayfa in range(3,5):
        url = 'https://www.vatanbilgisayar.com/notebook/' + "?page=" + str(sayfa)
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        list = soup.find_all("a", {"class": "product-list__link"})
        list3 = soup.find_all("div", {"class": "product-list product-list--list-page"})

        for im in list3:
            img = im.img.get("data-src")
            # print(img)
            imgs.append(img)

        for li in list:
            link = 'https://www.vatanbilgisayar.com/notebook/' + li.get("href")
            links.append(link)
            name = li.h3.text
            # print(name)
            names.append(name)
    # print(links)
    for a in links:
        url_ic = a
        html_ic = requests.get(url_ic).content
        soup_ic = BeautifulSoup(html_ic, "html.parser")
        list_ic = soup_ic.find_all("tr", {"data-count": "0"})
        list_ic1 = soup_ic.find("span", {"class": "product-list__price"})
        prices.append(list_ic1.text)

        for j in list_ic:
            prop = j.p.text
            item = j.td.text
            if item == "Ram (Sistem Belleği)":
                rams.append(prop)
            elif item == "İşlemci Teknolojisi":
                islemcis.append(prop)
            elif item == "İşlemci Numarası":
                islemci_models.append(prop)
            elif item == "Ekran Boyutu":
                ekran.append(prop)
            elif item == "Disk Kapasitesi":
                disks.append(prop)
            elif item == "Disk Türü":
                disktur.append(prop)
            elif item == "Üretici Part Numarası":
                models.append(prop)
            elif item == "İşletim Sistemi":
                isletims.append(prop)
    # print(prices)
    connection = sql.connect("FirstDatabase.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS bilgisayar (marka TEXT,model_no  TEXT,isletim_sistemi  TEXT,islemci_tipi 
         TEXT, islemci_nesli  TEXT,ram  TEXT,ekran_boyut TEXT,disk_tur TEXT, disk_boyut  TEXT,fiyat TEXT,link TEXT,resim TEXT,Site TEXT)""")

    ekle = """INSERT INTO bilgisayar (marka,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,ekran_boyut,disk_tur,disk_boyut,fiyat,link,resim,site)  VALUES(
         ?,?,?,?,?,?,?,?,?,?,?,?,?) """
    for k in range(len(links)):
        cursor.execute(ekle, (
            names[k], models[k], isletims[k], islemcis[k], islemci_models[k], rams[k], ekran[k], disktur[k], disks[k],
            prices[k], links[k], imgs[k], "Vatan"))
        connection.commit()


vt()


def n_11():
    items = []
    props = []
    rams = []
    isletims = []
    models = []
    islemcis = []
    islemci_models = []
    disks = []
    links = []
    imgs = []
    names = []
    prices = []
    markas = []
    disktur = []
    ekran = []
    i = 0
    for sayfa in range(1, 5):
        url = 'https://www.n11.com/bilgisayar/dizustu-bilgisayar' + "?pg=" + str(sayfa)
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        list = soup.find_all("li", {"class": "column"})
        list1 = soup.find_all("span", {"class": "newPrice cPoint priceEventClick"})
        for p in list1:
            prce = p.ins.text
            prices.append(prce)
            # print(prce)

        for li in list:
            name = li.div.a.h3.text
            link = li.div.a.get("href")
            links.append(link)
            names.append(name)
            # print(str(i) + name)
            # print(link)
            i += 1
            url_ic = link
            html_ic = requests.get(url_ic).content
            soup_ic = BeautifulSoup(html_ic, "html.parser")

            list_ic = soup_ic.find("div", {"class": "unf-prop-context"})
            list_ic1 = list_ic.find_all("p", {"class": "unf-prop-list-title"})
            list_ic2 = list_ic.find_all("p", {"class": "unf-prop-list-prop"})
            list_ic3 = soup_ic.find_all("div", {"class": "imgObj"})

            for h in list_ic3:
                img = h.a.get("href")
                imgs.append(img)
                # print(img)

            for a in range(len(list_ic2)):
                # print(list_ic1[a].text+":"+list_ic2[a].text)
                if list_ic1[a].text == "Bellek Kapasitesi":
                    rams.append(list_ic2[a].text)
                elif list_ic1[a].text == "İşlemci":
                    islemcis.append(list_ic2[a].text)
                elif list_ic1[a].text == "İşlemci Modeli":
                    islemci_models.append(list_ic2[a].text)
                elif list_ic1[a].text == "Disk Kapasitesi":
                    disks.append(list_ic2[a].text)
                elif list_ic1[a].text == "Model":
                    models.append(list_ic2[a].text)
                elif list_ic1[a].text == "İşletim Sistemi":
                    isletims.append(list_ic2[a].text)
                elif list_ic1[a].text == "Marka":
                    markas.append(list_ic2[a].text)
                elif list_ic1[a].text == "Disk Türü":
                    disktur.append(list_ic2[a].text)
                elif list_ic1[a].text == "Ekran Boyutu":
                    ekran.append(list_ic2[a].text)

    connection = sql.connect("firstDatabase.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS bilgisayar (marka TEXT,model_no  TEXT,isletim_sistemi  TEXT,islemci_tipi 
    TEXT, islemci_nesli  TEXT,ram  TEXT,ekran_boyut TEXT,disk_tur TEXT, disk_boyut  TEXT,fiyat TEXT,link TEXT,resim TEXT,Site TEXT)""")

    ekle = """INSERT INTO bilgisayar (marka,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,ekran_boyut,disk_tur,disk_boyut,fiyat,link,resim,site)  VALUES(
    ?,?,?,?,?,?,?,?,?,?,?,?,?) """
    for k in range(len(links)):
        cursor.execute(ekle, (
            names[k], models[k], isletims[k], islemcis[k], islemci_models[k], rams[k], ekran[k], disktur[k], disks[k],
            prices[k], links[k], imgs[k], "N11"))
        connection.commit()


n_11()

def trendyol():
    links = []
    rams = []
    isletims = []
    models = []
    islemcis = []
    islemci_models = []
    disks = []
    imgs = []
    names = []
    prices = []
    markas = []
    disktur = []
    ekran = []

    for sayfa in range(1, 5):
        url = 'https://www.trendyol.com/laptop-x-c103108' + '?pi=' + str(sayfa)
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        list = soup.find_all("div", {"class": "p-card-chldrn-cntnr card-border"})

        for li in list:
            link = li.a.get("href")
            links.append(link)
    for i in range(len(links)-2):
        url_ic = 'https://www.trendyol.com' + links[i]
        html_ic = requests.get(url_ic).content
        soup_ic = BeautifulSoup(html_ic, "html.parser")
        list_ic = soup_ic.find_all("li", {"class": "detail-attr-item"})
        list_ic2 = soup_ic.find_all("h3", {"class": "detail-name"})
        list_ic3 = soup_ic.find_all("div", {"class": "flex-container"})
        list_ic4 = soup_ic.find("span", {"class": "prc-dsc"})
        for d in range(0, len(list_ic3), 2):
            img = list_ic3[d].img.get("src")
            imgs.append(img)

            # print("\n"+img)
        for p in list_ic4:
            price = p.text
            prices.append(price)
        for c in list_ic2:
            names.append(c.text)
            # print(c.text)

        for a in range(len(list_ic)):
            if list_ic[a].span.text == "İşlemci Tipi":
                islemcis.append(list_ic[a].b.text)
            elif list_ic[a].span.text == "İşletim Sistemi":
                isletims.append(list_ic[a].b.text)
            elif list_ic[a].span.text == "Ram (Sistem Belleği)":
                rams.append(list_ic[a].b.text)
            elif list_ic[a].span.text == "Ekran Boyutu":
                ekran.append(list_ic[a].b.text)
            elif list_ic[a].span.text == "SSD Kapasitesi":
                disks.append(list_ic[a].b.text)
            elif list_ic[a].span.text == "İşlemci Modeli":
                islemci_models.append(list_ic[a].b.text)
            elif list_ic[a].span.text == "İşlemci Tipi":
                islemcis.append(list_ic[a].b.text)
    connection = sql.connect("FirstDatabase.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS bilgisayar (marka TEXT,model_no  TEXT,isletim_sistemi  TEXT,islemci_tipi 
      TEXT, islemci_nesli  TEXT,ram  TEXT,ekran_boyut TEXT,disk_tur TEXT, disk_boyut  TEXT,fiyat TEXT,link TEXT,resim TEXT,Site TEXT)""")

    ekle = """INSERT INTO bilgisayar (marka,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,ekran_boyut,disk_tur,disk_boyut,fiyat,link,resim,site)  VALUES(
      ?,?,?,?,?,?,?,?,?,?,?,?,?) """
    for k in range(len(islemcis)):
        cursor.execute(ekle, (
            names[k], names[k].split(" ")[1], isletims[k], islemcis[k], islemci_models[k], rams[k], ekran[k], "SSD",
            disks[k],
            prices[k], "https://www.trendyol.com" + links[k], imgs[k], "Trendyol"))
        connection.commit()


trendyol()


def vatan():
    names = []
    links = []
    rams = []
    isletims = []
    models = []
    islemcis = []
    islemci_models = []
    disks = []
    imgs = []
    prices = []
    markas = []
    disktur = []
    ekran = []

    for sayfa in range(1, 3):
        url = 'https://www.vatanbilgisayar.com/notebook/' + "?page=" + str(sayfa)
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        list = soup.find_all("a", {"class": "product-list__link"})
        list3 = soup.find_all("div", {"class": "product-list product-list--list-page"})

        for im in list3:
            img = im.img.get("data-src")
            # print(img)
            imgs.append(img)

        for li in list:
            link = 'https://www.vatanbilgisayar.com/notebook/' + li.get("href")
            links.append(link)
            name = li.h3.text
            # print(name)
            names.append(name)
    # print(links)
    for a in links:
        url_ic = a
        html_ic = requests.get(url_ic).content
        soup_ic = BeautifulSoup(html_ic, "html.parser")
        list_ic = soup_ic.find_all("tr", {"data-count": "0"})
        list_ic1 = soup_ic.find("span", {"class": "product-list__price"})
        prices.append(list_ic1.text)

        for j in list_ic:
            prop = j.p.text
            item = j.td.text
            if item == "Ram (Sistem Belleği)":
                rams.append(prop)
            elif item == "İşlemci Teknolojisi":
                islemcis.append(prop)
            elif item == "İşlemci Numarası":
                islemci_models.append(prop)
            elif item == "Ekran Boyutu":
                ekran.append(prop)
            elif item == "Disk Kapasitesi":
                disks.append(prop)
            elif item == "Disk Türü":
                disktur.append(prop)
            elif item == "Üretici Part Numarası":
                models.append(prop)
            elif item == "İşletim Sistemi":
                isletims.append(prop)
    # print(prices)
    connection = sql.connect("FirstDatabase.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS bilgisayar (marka TEXT,model_no  TEXT,isletim_sistemi  TEXT,islemci_tipi 
         TEXT, islemci_nesli  TEXT,ram  TEXT,ekran_boyut TEXT,disk_tur TEXT, disk_boyut  TEXT,fiyat TEXT,link TEXT,resim TEXT,Site TEXT)""")

    ekle = """INSERT INTO bilgisayar (marka,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,ekran_boyut,disk_tur,disk_boyut,fiyat,link,resim,site)  VALUES(
         ?,?,?,?,?,?,?,?,?,?,?,?,?) """
    for k in range(len(links)):
        cursor.execute(ekle, (
            names[k], models[k], isletims[k], islemcis[k], islemci_models[k], rams[k], ekran[k], disktur[k], disks[k],
            prices[k], links[k], imgs[k], "Vatan"))
        connection.commit()


vatan()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/view.html")
def view():
    con = sql.connect("firstDatabase.db")

    con.row_factory = sql.Row

    cur = con.cursor()

    cur.execute("select * from bilgisayar")

    rows = cur.fetchall()
    return render_template("view.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
