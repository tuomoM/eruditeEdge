# eruditeEdge
![erudite Edge gives you a tool for getting your vocab skills sharpened](static/Eelogo.jpg)
### eruditeEdge
Solution has functionalities for adding vocabulary items, changing, deleting, publishing them to global use and possiblity to suggest changes to other users vocabs.
Training part allows the user to create training sets out of the available vocabularies. The sets can be practiced in flashcard mode and knowledge tested.






*This is a solution for helsinki university course*
### completed 
- User is able to create an userid and log in. 
- User is able to add vocabs to database. 
- User is able to maintain already added vocab, and set the visibility to either private or global 
- User is able to see and search for vocabs created by him/herself and ones marked global by other users <
- User is able to create practice sets and practice them.  
- User is able to test his knowledge on chosen set of vocabs. the statistics are saved for this particular set. 
- Application has user page that shows statistic about the user
- User is able to open a previously practiced set of vocabs and he is shown the test result from previous time he did the set
- Clean up the code in test submit to remove "[]" as the original solution did not work
- Implement handling for local / global for vocabs category handling for vocabs.
- Implement way to go from flashcard training to test directly.
- implement the before functions across the blueprint
- Implement CSRF checking
- Add possibility to suggest a change to global vocabs created by other users
- Add inbox type solution to review change suggestions and handle them.
- Possibility to cancel your own suggestion for change when its not yet approved
- Possibility to enter flashcard mode from user information / users training session view
- User and community statistics added to user info page
- Finalization of layouts and clean up of code
- Possiblity to return to flashcard mode from testmode

### Planned updates
- Visibility to rejected and accepted suggestions



### Main issues
* Due to chosen technology, ie. no Javascript, it is difficult to create a good filtering mechanism for the vocabs when choosing wich ones you want to have for your training session. Without javascript we would always have to submit the query to backend and yet retain the selection. This i have deemed to be too cumbersome to do given that it would be a snap of fingers with javascript.




## Installation 

Create database:
```
$ sqlite3 database.db < schema.sql
```
Initialize the database
```
$ sqlite3 database.db < init.sql
```
Install virtual environment
```
$ python3 -m venv venv
```
Start the virtual environment
```
$ source venv/bin/activate
```
Install `flask`-library:
```
$ pip install flask
```
Solution can be started with:
```
$ flask run
```



## Planned site structure

- 1 Home page
- Vocabs
- - Vocab List
- - -Create new vocab
- - -Edit vocab
- - - Suggest change to vocab
- - - Suggestion inbox
- Training menu
- - Create a new training set / select vocabs
- - - Flash card training
- - - Test your knowledge
- - choose old set to train with / delete training
- User statistics

