import uuid
from faker import Faker
import psycopg2
from dotenv import load_dotenv
import os
import json
import random

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

CONN_URL = f'postgresql://{ DATABASE_USER }:{ DATABASE_PASSWORD }@{ DATABASE_HOST }:{ DATABASE_PORT }/{ DATABASE_NAME }'

fake = Faker()

level_match = {
    'Primary 1': 1,
    'Primary 2': 2,
    'Primary 3': 3,
    'Primary 4': 4,
    'Primary 5': 5,
    'Primary 6': 6,
    'Secondary 1': 7,
    'Secondary 2': 8,
    'Secondary 3': 9,
    'Secondary 4': 10,
    'Secondary 5': 11,
    'Junior College 1': 12,
    'Junior College 2': 13,
}

if os.path.exists('tutor.json'):
    os.remove('tutor.json')
if os.path.exists('student.json'):
    os.remove('student.json')

with psycopg2.connect(CONN_URL) as conn:

    with conn.cursor() as curs:
    
        curs.execute('DROP TABLE IF EXISTS "user"')
        curs.execute('''
            CREATE TABLE "user" (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(255) NOT NULL,
                current_education VARCHAR(255),
                budget BIGINT,
                subject VARCHAR(255),
                address VARCHAR(255),
                grades VARCHAR(255),
                qualification VARCHAR(255),
                residential_zone VARCHAR(255),
                levels_taught VARCHAR(255),
                subjects_taught VARCHAR(255),
                rate_per_hour BIGINT,
                gender VARCHAR(255),
                number_of_years_of_teaching_experience VARCHAR(255),
                level BIGINT
            );
        ''')

        generated_emails = []

        def generate_unique_email():
            while True:
                email = fake.email()
                if email not in generated_emails:
                    generated_emails.append(email)
                    print(email)
                    return email

        with open('TUTOR.sql', 'r') as f:
            for line in f:
                data = line.split("'")[1::2]  # получаем данные из строк в кавычках
                print(data)
                tutor = {
                    'id': str(uuid.uuid4()),
                    'name': data[0],
                    'qualification': data[1],
                    'residential_zone': data[2],
                    'levels_taught': data[3],
                    'subjects_taught': data[4],
                    'rate_per_hour': int(data[5][1:]),
                    'gender': data[6],
                    'number_of_years_of_teaching_experience': data[7],
                    'role': 'TUTOR',
                    'email': generate_unique_email(),
                    'password': fake.password(),
                    'level': level_match[data[3]]
                }
                curs.execute(
                    '''INSERT INTO "user" (
                        id, name, qualification, residential_zone, levels_taught, subjects_taught,
                        rate_per_hour, gender, number_of_years_of_teaching_experience, role, email,
                        password, level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )''',
                    (
                        tutor['id'], tutor['name'], tutor['qualification'], tutor['residential_zone'],
                        tutor['levels_taught'], tutor['subjects_taught'], tutor['rate_per_hour'],
                        tutor['gender'], tutor['number_of_years_of_teaching_experience'], tutor['role'],
                        tutor['email'], tutor['password'], tutor['level']
                    )
                )
                with open('tutor.json', 'a') as f:
                    json.dump(tutor, f, indent=2)
                    f.write(',\n')


        with open('STUDENT.sql', 'r') as f:
            for line in f:
                data = line.split("'")[1::2]  # получаем данные из строк в кавычках
                student = {
                    'id': str(uuid.uuid4()),
                    'name': data[0],
                    'residential_zone': random.choice(["North", "South", "West", "East"]),
                    'current_education': data[1],
                    'budget': int(data[2][1:]),
                    'subject': data[3],
                    'address': data[4],
                    'grades': data[5],
                    'role': 'STUDENT',
                    'email': generate_unique_email(),
                    'password': fake.password(),
                    'level': level_match[data[1]]
                }
                curs.execute(
                    '''INSERT INTO "user" (
                        id, name, residential_zone, current_education, budget, subject, address,
                        grades, role, email,
                        password, level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )''',
                    (
                        student['id'], student['name'], student['residential_zone'], student['current_education'], student['budget'],
                        student['subject'], student['address'], student['grades'],
                        student['role'], student['email'], student['password'], student['level']
                    )
                )
                with open('student.json', 'a') as f:
                    json.dump(student, f, indent=2)
                    f.write(',\n')
