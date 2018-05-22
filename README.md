# CareDash coding assignment

## Setup
Execute the following terminal commands

First, cd to src/doctor_model/__init__.py and modify the user, password, host, and database fields to connect to a mysql database of your choice.

Then, cd back to the root directory and execute the following command.

```bash
python3 src/main.py
```

## Design
Scalability: this app uses flask's builtin testing server, which is not designed for a production workload. In order to scale up this app, one should deploy to a proper web server such as Apache or Nginx.

Error Handling: The server will respond with an error message in the event that a doctor/review doesn't exist, or in the event that the JSON field attached to a POST request is not properly formatted. When a post request successfully completes, a copy of the post request as well as a newly generated id field are returned.

Data Model: I replicated the data model as described in the assignment. The name field is not unique for doctors since there are doctors that share the same name.

## Libraries used
- mysqlclient
- flask
- flask_sqlalchemy
