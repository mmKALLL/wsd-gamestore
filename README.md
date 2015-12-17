Quagmire Zone Underground Project Plan
--------------------------------------

### 1. Team

429788 Esa Koskinen
429186 Atte Jaantila
355496 Jussi Hirvonen


### 2. Goal

Our aim on this course is to create an online store software for JavaScript games, which will allow developers to distribute their software and receive payments, and players to purchase and play games right in their browser.

Main features will include at least user authentication, global high score lists and server-side game saving. For developers we will implement functionalities such as sales statistics and a comprehensive UI for managing their games.

We want the system to be sufficiently secure and able to withstand attempts at malicious usage, as well as flexible and somewhat modular. If there is time, we also plan to make use of some external APIs (such as Google login), and are in general looking to get an excellent grade.


### 3. Implementation plan

(games are HTML files displayed within an iframe)

Using the technologies taught on this course, we shall create a web service that provides the following pages:

Front page, with login at top bar (newest game list, (widgets))
Registration page (username, password, confirm password, email)
User page (list of games, profile info, user settings, etc)
Developer page (list of games made (both public and non-published), statistics for each game (spoiler-type button), adding a game)
Game page (buy/play button, high score list)
  -> transforms to gameplay page when clicked play
  -> redirect to purchase page when not owned by user


  
jQuery, HTML/CSS/JS

etusivu, jossa esill‰ myynniss‰ olevia pelej‰ (n‰ist‰ n‰kyviss‰ kenties nimi, 1 screenshot ja teksti‰, jotka kaikki ovat m‰‰ritelt‰viss‰ developerin sivulla)
mahdollisuus kirjautua sis‰‰n (Google login? Ei ehk‰ commitata t‰h‰n koska ei viel‰ tietoa miten hankalaa voi olla) jolloin voi siirty‰ omalle sivulle (profiilisivu)
jokaisella myynniss‰ olevalla pelill‰ joka on listattu julkiseksi (Pelin voi lis‰t‰ sivuille ilman, ett‰ se on pakko laittaa heti myyntiin! Mielest‰ni t‰rke‰‰) on oma sivunsa
Pelej‰ voi etsi‰ tietokannasta (toteutetaan oma search engine? :D joka palauttaa listan peleist‰, jotka sis‰ltiv‰t jonkun stringin? onnistuuko?)
K‰ytt‰j‰n profiilisivulla n‰kyy h‰nen omistamansa pelit, joista p‰‰see myˆs linkin kautta pelin sivulle
Pelin sivulla voi joko ostaa pelin, tai jos omistaa sen jo, niin siirty‰ pelaamaan sit‰
Developerin sivulla voi tarkastella statistiikkoja (eri paneelissa kuin pelit) ja lis‰t‰/editoida/poistaa pelej‰ ja niiden tietoja (screenshot, description, ja se URL mist‰ peli haetaan!)

### 4. Project practices and schedule



### 5. Testing


