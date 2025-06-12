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
- Application has user pager that shows statistic about the user
- User is able to open a previously practiced set of vocabs and he is shown the test result from previous time he did the set


### Planned updates
- Clean up the code in test submit to remove "[]" as the original solution did not work
- Restructure the blueprints to have just 3 blueprints in total
- Implement handling for local / global for vocabs. currently set as 0 local and 1 global
- Restructure the application, to have more easy to operate. ie. landing page should be the user info page and search could be elsewhere
- Implement CSRF checking





## Installation 

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

Create database:

```
$ sqlite3 database.db < schema.sql

```

Solution can be started with:

```
$ flask run
```



