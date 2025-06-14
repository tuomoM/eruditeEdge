# eruditeEdge
![erudite Edge gives you a tool for getting your vocab skills sharpened](static/Eelogo.jpg)

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

### Planned updates

- implement the before functions across the blueprint
- Implement CSRF checking
- Implement way to go from flashcard training to test directly.



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



