# Patient Management API with Flask and SQLite

This is a simple Flask API to manage patients, using SQLite as the database. 

## How to Run

1. Clone the repository:

  
   `git clone https://github.com/Lemar00/docker-lab.git`
   
   `cd flask-patient-sqlite-app`

3. Build and run the app with Docker Compose:
   
	`docker-compose up --build`

5. Access the API at http://127.0.0.1:8080. 



## API Endpoints

GET /patients/: List all patients.
POST /patients/: Create a new patient.
GET /patients/{id}: Get a patient by ID.
PUT /patients/{id}: Update a patient by ID.
DELETE /patients/{id}: Delete a patient by ID.
