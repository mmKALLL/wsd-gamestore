Quagmire Zone Underground Project Plan
--------------------------------------

### 1. Team

Esa, Atte and Jussi

  
### 2. Goal

Our aim on this course is to create an online store software for JavaScript games, which will allow developers to distribute their software and receive payments, and players to purchase and play games right in their browser.

Main features will include at least user authentication, global high score lists and server-side game saving. For developers we will implement functionalities such as sales statistics and a comprehensive UI for managing their games.

We want the system to be sufficiently secure and able to withstand attempts at malicious usage, as well as flexible and somewhat modular. If there is time, we also plan to make use of some external APIs (such as Google login), and are in general looking to get an excellent grade. In other words, almost all functionality detailed in the Project Description will be implemented.

  
### 3. Implementation plan

We will be using the technologies taught on this course; Django for managing the backend, and HTML/CSS/JS for handling the user's view. The games will be played in an iframe right within our site, but hosted on the developers' servers. The term "user" will be used for both types of registered users - the players and the developers - and a player will be able to upgrade their account and gain access to the developer tools at any time.

All of the pages in our service have the same header and footer. The header has our logo, with a link to the front page, and fields for logging in, while the footer will include at least some kind of disclaimer, our contact information, and an introduction page for becoming a developer on the site. An unregistered user trying to access features only available for registered users will be asked to log in.

The service should include at least the following pages and functionality:

* Front page, which will feature the latest releases and allow the users to navigate our site.
* Registration page. The required fields will include at least a username, password, password confirm, and email address.
* User page, which has the list of a registered user's owned games, profile info, and settings.
* Developer page, which has the list of a registered user's developed games - both public and those not yet published - as well as statistics and settings for each game. A developer page also has the necessary tools for adding a new game to the site.
* Game page, where the details (name, screenshot and description) of a single game are shown, and the user can either purchase the game or play it if they already own it. It will also have a list of high scores for that game as well as display the user's best score.
* A game list or search page, where users will be able to look up games by their name.

  
Since the server side architecture seems difficult to change afterwards, we should consider that as an architecturally significant requirement and model as much of it as possible on a general level before starting development. Considering that, the following should include most of the Django models needed to support all of these features:

* Users; we need to store information of users on a server, so that we can differentiate between them and know which games they have purchased. We plan on this model including developers by having a True/False attribute for whether the user has access to our developer pages.
* Games; this model has the information of a single game and any necessary references to other models.
* Owned games; for each user, we have a list of games that they have purchased, and for each owned game a list of saved game states.
* Created games; for each developer, we have a list of games that they have added to the service.
* Highscores; for each game, include a list of each user's best score (if they have played that game).

  
### 4. Project practices and schedule

Our team members have agreed to spend at least one day developing the software every two weeks, or every week if possible. We are using Skype as our main communication channel during the project.

Regarding development, we are going to employ individual branches and use Git pull requests or pair programming in order to review all code that goes into the master branch. Apart from parts where the code is self-descriptive, all functions and complex structures will be commented. Some unit tests will be used, especially for functional-style JavaScript. These practices will result in a high degree of quality in the code and make it easier to collaborate.

Roughly speaking, we have allocated two weeks for developing most of the server side functionality, three weeks for the client side functionality, one week for integration and testing, and one week for additional features, finishing up, and deployment. Of course, this plan might require some adjustment as we go, but having a general guideline will be very beneficial for estimating the workload and our pace of development.

  
### 5. Testing

To ensure that the software is secure and working as intended, we will write some automatic unit tests for the main JavaScript functions we use. This way we can be certain that the basic functionality won't be broken by updates to the source code. All new features shall be peer reviewed before committing to uphold awareness within the team and avoid mistakes due to carelessness and tunnel vision. We obviously also plan to test the software manually excessively.

Regarding security, it is important that we at least validate all incoming data from the users and make sure that it's in the correct format. This will prevent basic script injections from becoming a problem. All in all, we are going to pay close attention to the reliability of the system.
