## Väliplautus 1
- [x] Done.

## Välipalautus 2
- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
    - 1. Index -> Register -> Login -> Main View
    - 2. Index -> Login -> Main View
- [x] Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita.
    - 1. Lisääminen: Index -> Login -> Main View: Add New Website -> Address: e.g. example.com (keyword ei vielä käytössä) -> Add
    - 2. Muokkaamaan: Index -> Login -> Main View: Public/Hide: Toggle vaihtaa tietorakenteen näkyvyyttä muille käyttäjille
    - 3. Poistaminen: Index -> Login -> Main View: Delete: Delete poistaa käyttäjän valitaseman tietokohteen
- [x] Käyttäjä näkee sovellukseen lisätyt tietokohteet.
    - 1. Käyttäjän Omat Tietorakenteet: Index -> Login -> Main View: "Your Monitored Websites" kohdassa näytetään käyttäjän omat julkiset & yksityiset tietorakenteet
    - 2. Julkiset Tietorakenteet: Index -> Login -> Main View: "Public Websites" kohdassa näytetään käyttäjän ja muiden julkiset tietorakenteet
- [x] Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella.
    - 1. Haku: Index -> Login -> Main View: Käyttäjä pystyy filtteröimään julkisia tietorakenteita valitsemallaan hakusanalla
- [x] README.md-tiedoston tulee kuvata, millainen sovellus on ja miten sitä voi testata.
    - README.md päivitetty, toisten käyttäjien sivulle kommentointi feature-idea poistettu ja olemassa olevien featureiden ominaisuuksia tarkennettu.

Huomioitavaa:
    - Sovellus ei vielä tee health-check kutsuja tietorakenteista, mutta toimintoa testattu ensimmäisellä viikolla.


## Sovelluksen perusvaatimukset
- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen
- [x] Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita
- [x] Käyttäjä näkee sovellukseen lisätyt tietokohteet
- [x] Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella
- [ ] Käyttäjäsivu näyttää tilastoja ja käyttäjän lisäämät tietokohteet
- [ ] Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun
- [ ] Käyttäjä pystyy lisäämään tietokohteeseen toissijaisia tietokohteita
- [ ] Sovelluksen perusvaatimukset on kuvattu tarkemmin aloitussivulla

## Tekniset perusvaatimukset
- [ ] Sovellus toteutettu kurssimateriaalin mukaisesti
- [ ] Sovellus toteutettu Pythonilla käyttäen Flask-kirjastoa
- [ ] Sovellus käyttää SQLite-tietokantaa
- [ ] Kehitystyössä käytetty Gitiä ja GitHubia
- [ ] Sovelluksen käyttöliittymä muodostuu HTML-sivuista
- [ ] Sovelluksessa ei ole käytetty JavaScript-koodia
- [ ] Tietokantaa käytetään suoraan SQL-komennoilla (ei ORMia)
- [ ] Flaskin lisäksi käytössä ei muita erikseen asennettavia Python-kirjastoja
- [ ] Sovelluksen ulkoasu (HTML/CSS) on toteutettu itse ilman kirjastoja
- [ ] Sovelluksen koodi on kirjoitettu englanniksi
- [ ] Tietokannan taulut ja sarakkeet on nimetty englanniksi

## Versionhallinta
- [ ] Tiedosto README.md kertoo, millainen sovellus on ja miten sitä voi testata
- [ ] Kehitystyön aikana on tehty commiteja säännöllisesti
- [ ] Commit-viestit on kirjoitettu englanniksi

## Sovelluksen turvallisuus
- [ ] Salasanat tallennetaan tietokantaan asianmukaisesti
- [ ] Käyttäjän oikeus nähdä sivun sisältö tarkastetaan
- [ ] Käyttäjän oikeus lähettää lomake tarkastetaan
- [ ] Käyttäjän syötteet tarkastetaan ennen tietokantaan lisäämistä
- [ ] SQL-komennoissa käytetty parametreja
- [ ] Sivut muodostetaan sivupohjien kautta (render_template)
- [ ] Lomakkeissa on estetty CSRF-aukko

## Vertaisarviointi ja palaute
- [ ] Ensimmäinen vertaisarviointi annettu
- [ ] Toinen vertaisarviointi annettu
- [ ] Tarkempaa tietoa vertaisarvioinnin vaatimuksista on vertaisarviointiohjeissa

## Lisävaatimukset (arvosana 4)

### Toimivuus ja käytettävyys
- [ ] Sovellusta on helppoa ja loogista käyttää
- [ ] CSS:n avulla toteutettu ulkoasu (itse tehty, ei CSS-kirjastoa)

### Versionhallinta
- [ ] Versionhallinnassa ei ole sinne kuulumattomia tiedostoja
- [ ] Commitit ovat hyviä kokonaisuuksia ja niissä on hyvät viestit

### Ohjelmointityyli
- [ ] Muuttujat ja funktiot nimetty kuvaavasti
- [ ] Sisennyksen leveys on neljä välilyöntiä
- [ ] Koodissa ei ole liian pitkiä rivejä
- [ ] Muuttujien ja funktioiden nimet muotoa total_count (ei totalCount)
- [ ] Välit oikein =- ja ,-merkkien ympärillä
- [ ] Ei ylimääräisiä sulkeita if- ja while-rakenteissa

### Tietokanta-asiat
- [ ] Taulut ja sarakkeet on nimetty kuvaavasti
- [ ] Käytetty REFERENCES-määrettä, kun viittaus toiseen tauluun
- [ ] Ei kyselyjä muotoa SELECT * (haettavat sarakkeet listattu aina)
- [ ] Käytetty SQL:n ominaisuuksia järkevällä tavalla

### Vertaisarviointi ja palaute
- [ ] Ensimmäinen vertaisarviointi tehty kattavasti
- [ ] Toinen vertaisarviointi tehty kattavasti
- [ ] Kurssipalaute annettu

## Lisävaatimukset (arvosana 5)

### Ohjelmointityyli
- [ ] Käytetty Pylint-työkalua ja raportoitu tulokset
- [ ] Raportissa selostettu jokaisesta Pylint-ilmoituksesta, miksi sitä ei ole korjattu

### Toimivuus ja käytettävyys
- [ ] Käyttäjän lähettämässä tekstissä rivinvaihdot näkyvät selaimessa
- [ ] Kuvissa käytetty alt-attribuuttia (jos sovelluksessa kuvia)
- [ ] Lomakkeissa käytetty label-elementtiä

### Suuren tietomäärän käsittely
- [ ] Sovellusta testattu suurella tietomäärällä ja raportoitu tulokset
- [ ] Sovelluksessa käytössä tietokohteiden sivutus
- [ ] Tietokantaan lisätty indeksi, joka nopeuttaa suuren tietomäärän käsittelyä
