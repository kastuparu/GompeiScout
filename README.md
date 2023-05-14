# GompeiScout

GompeiScout, named after [WPI's](https://www.wpi.edu/) mascot Gompei the Goat, is a scouting software for [FRC 190](https://wp.wpi.edu/frc190/).
Developed by Katy Stuparu, 2023.

## What it does

GompeiScout 2023 allows scouters and drivers to easily enter match data.
* Autonomous
  * Number of cubes and cones scored low, mid, and high
  * Mobility?
  * Docked?
  * Engaged?
  * Comments
* Teleoperation
  * Number of cubes and cones scored low, mid, and high
  * Floor pickup?
  * Human player station pickup?
* Match/Robot Analysis
  * Short summary
  * Analysis
    * Describe the robot's collecting/scoring mechanism. How does it affect the team's ability to score points? 
    * Describe the driver's ability. How does it affect the team's ability to score points? 
    * What is slowing them down? (ex. collecting cubes from floor, lining up to score high, defended)
    * What is their strategy (offensive, defensive, nothing) and how effective is it in scoring points? 
    * How well do they work with their alliance? Discuss endgame here.
* Driver Input
  * How successful was communication with this team?

GompeiScout 2023 also can display a detailed summary of these results for each team, including average values for all 
quantitative data and a list of all analysis collected.

Additionally, a summary of data for the teams playing in an upcoming match can be displayed. This includes average 
cones and cubes scored in teleop and auto as well as auto balancing data and short summaries.

The rankings for all teams based on quantitative data can be displayed. The quantitative data rankings are calculated 
based on how many points the team would have scored for their alliance on average during a match. See the
[FRC 2023 game manual](https://firstfrc.blob.core.windows.net/frc2023/Manual/2023FRCGameManual.pdf) for all point 
values. These rankings help scouters compare teams who perform similarly in terms of autos and scoring in teleop. This 
is not intended to be a pick list; the qualitative data gathered should be used in conjunction with this to make a pick 
list.

## How it works

GompeiScout has two components: the web server/application and the database.

The web server/application uses [Gunicorn](https://gunicorn.org) and [Flask](https://flask.palletsprojects.com). 
Gunicorn is a Python WSGI (Web Server Gateway Interface) server. Flask is a Python WSGI application.

The database is [MongoDB](https://www.mongodb.com), which stores data in the form of BSON (similar to JSON) documents. 
MongoDB can be run on a local machine to store data locally, or data can be stored in the cloud. Match data and driver 
feedback data are each stored in a collection. The advantage of using MongoDB for this project is to have a flexible
data model that integrates easily with Python and Flask.

Both the web server and the database can be run in [Docker](https://www.docker.com) containers. Docker is similar to 
a mini-virtual machine. It provides an environment for applications to run independently. This means that applications 
can be easily run the same way across various machines.

Scouters can access GompeiScout via a web browser with a wired or wireless connection to a machine where GompeiScout is 
running.

## To run GompeiScout on your machine:
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop). You will be able to manage or stop Docker
containers with Docker Desktop.
2. Download the GompeiScout code, and ```cd``` into the GompeiScout directory.
3. If you would like to use existing images from Docker Hub, pull the images and run them.
```
docker-compose up
```
4. If you would like to start from scratch, build the Docker containers.
```
docker-compose up -d --build
```
5. Now, you will need to configure the database to work with GompeiScout.
   1. Start an interactive shell on the ```mongodb``` container. Then, log in as ```root``` (the password is in 
   ```docker-compose.yml``` under ```MONGO_INITDB_ROOT_PASSWORD```).
   ```
   $ docker exec -it mongodb bin/bash
   root@c84d9a66f7e3:/ mongo -u root -p
   ```
   2. Create a Mongo user that Flask can use. 
   ```
   mongodb> db.createUser({user: 'flaskuser', pwd: 'fire23', roles: [{role: 'readWrite', db: 'flaskdb'}]})
   ```
   3. Create the ```matches``` and ```driver_feedback``` collections.
   ```
   mongodb> db.createCollection('matches')
   mongodb> db.createCollection('driver_feedback')
   ```
   4. Create search indices for the keyword ```team_number``` in the ```matches``` and ```driver_feedback``` 
   collections. This allows for search queries by team number to be executed faster and more efficiently.
   ```
   mongodb> db.matches.createIndex({'team_number': -1})
   mongodb> db.driver_feedback.createIndex({'team_number': -1})
   ```
   5. Log out of ```root``` and try logging into ```flaskuser``` to make sure it is working.
   ```
   mongodb> exit
   root@c84d9a66f7e3:/ mongo -u flaskuser -p fire23 --authenticationDatabase flaskdb
   ```
6. You can access the website from [localhost:5000](localhost:5000).
