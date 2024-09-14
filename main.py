from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from os import environ
import datetime

app = Flask(__name__)

# Utilisation de SQLite comme base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api(app, version='1.0', title='Patient API', description='A simple Patient Management API')

ns = api.namespace('patients', description='Patient operations')

# Définition du modèle Patient pour la documentation Swagger
patient_model = api.model('Patient', {
    'id': fields.Integer(readonly=True, description="L'identifiant unique du patient"),
    'first_name': fields.String(required=True, description="Le prénom du patient"),
    'last_name': fields.String(required=True, description="Le nom du patient"),
    'birth_date': fields.String(required=True, description="La date de naissance du patient"),
    'residence': fields.String(required=True, description="Le lieu de résidence du patient"),
    'blood_group': fields.String(required=True, description="Le groupe sanguin du patient (A, B, AB, O)"),
    'rhesus_factor': fields.String(required=True, description="Le facteur rhésus du patient (+ ou -)"),
    'created_at': fields.DateTime(readonly=True, description="La date de création de l'enregistrement")
})

# Modèle SQLAlchemy pour la table des patients
class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False)
    residence = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(3), nullable=False)
    rhesus_factor = db.Column(db.String(1), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'residence': self.residence,
            'blood_group': self.blood_group,
            'rhesus_factor': self.rhesus_factor,
            'created_at': self.created_at
        }

# Crée la base de données
def init_db():
    with app.app_context():
        db.create_all()

# Routes CRUD pour l'API

@ns.route('/')
class PatientList(Resource):
    @ns.doc('list_patients')
    @ns.marshal_list_with(patient_model)
    def get(self):
        '''Lister tous les malades'''
        return Patient.query.all()

    @ns.doc('create_patient')
    @ns.expect(patient_model)
    @ns.marshal_with(patient_model, code=201)
    def post(self):
        '''Créer un nouveau patient'''
        data = api.payload
        new_patient = Patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=data['birth_date'],
            residence=data['residence'],
            blood_group=data['blood_group'],
            rhesus_factor=data['rhesus_factor'],
        )
        db.session.add(new_patient)
        db.session.commit()
        return new_patient, 201

@ns.route('/<int:id>')
@ns.response(404, 'Patient non trouvé')
@ns.param('id', "L'identifiant du patient")
class PatientResource(Resource):
    @ns.doc('get_patient')
    @ns.marshal_with(patient_model)
    def get(self, id):
        '''Récupérer un patient par son id'''
        return Patient.query.get_or_404(id)

    @ns.doc('update_patient')
    @ns.expect(patient_model)
    @ns.marshal_with(patient_model)
    def put(self, id):
        '''Màj un patient par son idd'''
        patient = Patient.query.get_or_404(id)
        data = api.payload
        patient.first_name = data['first_name']
        patient.last_name = data['last_name']
        patient.birth_date = data['birth_date']
        patient.residence = data['residence']
        patient.blood_group = data['blood_group']
        patient.rhesus_factor = data['rhesus_factor']
        db.session.commit()
        return patient

    @ns.doc('delete_patient')
    @ns.response(204, 'Patient supprimé')
    def delete(self, id):
        '''Supprimer un patient par son identifiant'''
        patient = Patient.query.get_or_404(id)
        db.session.delete(patient)
        db.session.commit()
        return '', 204

# Lancer l'application
if __name__ == '__main__':
    init_db()  # Initialisation de la bd
    app.run(debug=True, host='0.0.0.0', port=8080)
