# eruditeEdge
![erudite Edge gives you a tool for getting your vocab skills sharpened](static/Eelogo.jpg)

*This is a solution for helsinki university course*
###completed 
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. <font color="green">(Done)</font>
- Käyttäjä pystyy lisäämään sovellukseen sanastokortteja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään sanastokortteja ja merkitsemään kortteja julkisiksi tai yksityisiksi. <font color="green">(Done)</font>
- Käyttäjä näkee sovellukseen lisätyt sanastokortit. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien julkisiksi merkitsemät sanastokortit. <font color="green">(Done)</font>

- Käyttäjä pystyy etsimään sanastokortteja hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä sanastokortteja.


### not yet completed
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät sanastokortit.
- Käyttäjä pystyy rakentamaaan sovelluksessa sanastokorteista harjoitussettejä ja tallentamaan ne kantaan. Käytettävissä tulee olla sekä omat että muiden julkiset sanakortit.
- Käyttäjä pystyy harjoittelemaan valittujen sanakorttien sanastoa. Harjoitusessio lopetetaan eksplisiittisesti ja sovellus näyttää statistiikan harjoituksesta. Statistiikka tallennetaan ja sen voi katsoa jälkeenpäin.
- Käyttäjä voi avata kantaan tallennetun oman harjoitussetin ja hänelle näytetään edellisen harjoituksen tulos, eli kuinka monta edellisellä kerralla meni oikein.

### functionalities done, but not in original plan
- Searched vocabs can be practiced using flashcards


## Installation 
T
Install `flask`-library:

```
$ pip install flask
```

Create database:

```
$ sqlite3 database.db < schema.sql

```

Solution can be started with:

```
$ flask run
```



