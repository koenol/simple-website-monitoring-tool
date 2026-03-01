## Lopullinen Palautus

Suurella tietomäärällä testaus:
[https://github.com/koenol/simple-website-monitoring-tool/blob/main/docs/testaus-report.md](https://github.com/koenol/simple-website-monitoring-tool/blob/main/docs/testaus-report.md)

Loppupalaute:
Kurssin kaikki kohdat tuli omasta mielestäni toteutettua. Paranneltavaa koodin luettavuuden suhteen kyllä jäi. website_manager.py ja reports_manager.py lisääminen ja niihin kuuluvien toimintojen enkapsulointi paransi app.py luettavuutta huomattavasti, mutta parannettavaa jäi vielä itse olio-luokkiin. Toiminnot olisi ollut syytä suunnitella tarkemmin jo ennen toista välipalautusta, jotta refaktorointiin ei olisi ollut tarve käyttää lopussa liikaa aikaa. 

## Sovelluksen perusvaatimukset
- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen
- [x] Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita
- [x] Käyttäjä näkee sovellukseen lisätyt tietokohteet
- [x] Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella
- [x] Käyttäjäsivu näyttää tilastoja ja käyttäjän lisäämät tietokohteet
- [x] Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun
- [x] Käyttäjä pystyy lisäämään tietokohteeseen toissijaisia tietokohteita
- [x] Sovelluksen perusvaatimukset on kuvattu tarkemmin aloitussivulla

## Tekniset perusvaatimukset
- [x] Sovellus toteutettu kurssimateriaalin mukaisesti
- [x] Sovellus toteutettu Pythonilla käyttäen Flask-kirjastoa
- [x] Sovellus käyttää SQLite-tietokantaa
- [x] Kehitystyössä käytetty Gitiä ja GitHubia
- [x] Sovelluksen käyttöliittymä muodostuu HTML-sivuista
- [x] Sovelluksessa ei ole käytetty JavaScript-koodia
- [x] Tietokantaa käytetään suoraan SQL-komennoilla (ei ORMia)
- [x] Flaskin lisäksi käytössä ei muita erikseen asennettavia Python-kirjastoja
- [x] Sovelluksen ulkoasu (HTML/CSS) on toteutettu itse ilman kirjastoja
- [x] Sovelluksen koodi on kirjoitettu englanniksi
- [x] Tietokannan taulut ja sarakkeet on nimetty englanniksi

## Versionhallinta
- [x] Tiedosto README.md kertoo, millainen sovellus on ja miten sitä voi testata
- [x] Kehitystyön aikana on tehty commiteja säännöllisesti
- [x] Commit-viestit on kirjoitettu englanniksi

## Sovelluksen turvallisuus
- [x] Salasanat tallennetaan tietokantaan asianmukaisesti
- [x] Käyttäjän oikeus nähdä sivun sisältö tarkastetaan
- [x] Käyttäjän oikeus lähettää lomake tarkastetaan
- [x] Käyttäjän syötteet tarkastetaan ennen tietokantaan lisäämistä
- [x] SQL-komennoissa käytetty parametreja
- [x] Sivut muodostetaan sivupohjien kautta (render_template)
- [x] Lomakkeissa on estetty CSRF-aukko

## Vertaisarviointi ja palaute
- [x] Ensimmäinen vertaisarviointi annettu
- [x] Toinen vertaisarviointi annettu
- [x] Tarkempaa tietoa vertaisarvioinnin vaatimuksista on vertaisarviointiohjeissa

## Lisävaatimukset (arvosana 4)

### Toimivuus ja käytettävyys
- [x] Sovellusta on helppoa ja loogista käyttää
- [x] CSS:n avulla toteutettu ulkoasu (itse tehty, ei CSS-kirjastoa)

### Versionhallinta
- [x] Versionhallinnassa ei ole sinne kuulumattomia tiedostoja
- [x] Commitit ovat hyviä kokonaisuuksia ja niissä on hyvät viestit

### Ohjelmointityyli
- [x] Muuttujat ja funktiot nimetty kuvaavasti
- [x] Sisennyksen leveys on neljä välilyöntiä
- [x] Koodissa ei ole liian pitkiä rivejä
- [x] Muuttujien ja funktioiden nimet muotoa total_count (ei totalCount)
- [x] Välit oikein =- ja ,-merkkien ympärillä
- [x] Ei ylimääräisiä sulkeita if- ja while-rakenteissa

### Tietokanta-asiat
- [x] Taulut ja sarakkeet on nimetty kuvaavasti
- [x] Käytetty REFERENCES-määrettä, kun viittaus toiseen tauluun
- [x] Ei kyselyjä muotoa SELECT * (haettavat sarakkeet listattu aina)
- [x] Käytetty SQL:n ominaisuuksia järkevällä tavalla

### Vertaisarviointi ja palaute
- [x] Ensimmäinen vertaisarviointi tehty kattavasti
- [x] Toinen vertaisarviointi tehty kattavasti
- [x] Kurssipalaute annettu

## Lisävaatimukset (arvosana 5)

### Ohjelmointityyli
- [x] Käytetty Pylint-työkalua ja raportoitu tulokset
- [x] Raportissa selostettu jokaisesta Pylint-ilmoituksesta, miksi sitä ei ole korjattu

### Toimivuus ja käytettävyys
- [x] Käyttäjän lähettämässä tekstissä rivinvaihdot näkyvät selaimessa -- Ei käytössä
- [x] Kuvissa käytetty alt-attribuuttia (jos sovelluksessa kuvia) -- Ei käytössä
- [x] Lomakkeissa käytetty label-elementtiä

### Suuren tietomäärän käsittely
- [x] Sovellusta testattu suurella tietomäärällä ja raportoitu tulokset
- [x] Sovelluksessa käytössä tietokohteiden sivutus
- [x] Tietokantaan lisätty indeksi, joka nopeuttaa suuren tietomäärän käsittelyä
