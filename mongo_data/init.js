// init.js - MongoDB Initialization Script
db = db.getSiblingDB('cases_db');
db.createCollection("cases");
db.createUser({
  user: "admin",
  pwd: "password",
  roles: [
    {
      role: "readWrite",
      db: "cases_db"
    }
  ]
});
