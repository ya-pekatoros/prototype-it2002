from sqlalchemy import create_engine
import uuid
from faker import Faker
import uuid
from dotenv import load_dotenv
from app import db, create_app, User

import os

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

engine = create_engine(f'postgresql://{ DATABASE_USER }:{ DATABASE_PASSWORD }@{ DATABASE_HOST }:{ DATABASE_PORT }/{ DATABASE_NAME }')

fake = Faker()

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

with engine.connect() as conn:

    # создаем список уже сгенерированных email-адресов
    generated_emails = []

    # генерируем новый email и проверяем, что он уникальный
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
            tutor = User(id=str(uuid.uuid4()), name=data[0], qualification=data[1], residential_zone=data[2],
                         levels_taught=data[3], subjects_taught=data[4], rate_per_hour=data[5], gender=data[6],
                         number_of_years_of_teaching_experience=data[7], role='TUTOR',
                         email=generate_unique_email(), password=fake.password())
            conn.execute(tutor.__table__.insert(), tutor.__dict__)
            conn.commit()

    # открываем файл STUDENT и загружаем данные в базу
    with open('STUDENT.sql', 'r') as f:
        for line in f:
            data = line.split("'")[1::2]  # получаем данные из строк в кавычках
            student = User(id=str(uuid.uuid4()), name=data[0], current_education=data[1], budget=data[2],
                            subject=data[3], address=data[4], grades=data[5], role='STUDENT',
                            email=generate_unique_email(), password=fake.password())
            conn.execute(student.__table__.insert(), student.__dict__)
            conn.commit()
