### INSTALLING/GETTING STARTED:

1. Created a mongo atlas free account. Project: analytics, cluster: mflix. set name and pwd, whitelist address 0.0.0.0/0


2. Installed mongo on my computer using this instructions: `https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/`
  1. `sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5`
  2. `echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list`
  3. `sudo apt-get update`
  4. `sudo apt-get install -y mongodb-org`

3. Download CSV file from the OMDB movies dataset. "It is nice because it is large enough and requires enough data cleaning to be realistic". Load it into mongo. The API changed so this worked for me (most of the info was in atlas->connect->mongo shell):

```
mongoimport --uri "mongodb+srv://<PROJECT>:<PROJECT-PWD>@mflix-d8wrg.mongodb.net/mflix?authSource=admin" --type csv --headerline  --ssl movies_initial.csv
```

4. Downloaded and installed compass. Go to atlas->connect->compass, copy string and compass will detect automatically. fill with pwd. And in favorite set: Analytics Free-Tier. Connect and explore data.

5. Connect from a python application: `pip install pymongo`. Also `pip install dnspython`