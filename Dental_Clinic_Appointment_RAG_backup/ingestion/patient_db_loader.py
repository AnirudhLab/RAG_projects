import mysql.connector

def connect_patient_db(config):
    return mysql.connector.connect(**config)
