import psycopg2
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

CONN_URL = f'postgresql://{ DATABASE_USER }:{ DATABASE_PASSWORD }@{ DATABASE_HOST }:{ DATABASE_PORT }/{ DATABASE_NAME }'

def get_user(email):

    with psycopg2.connect(CONN_URL) as conn:

        with conn.cursor() as curs:
            curs.execute('SELECT * from "user" WHERE email=%s', (email,))
            try:
                result = curs.fetchall()[0]
            except:
                return None

        user_attr = serialize_user_data(result)

        return user_attr


def serialize_user_data(result):
    return {
        "id": result[0],
        "name": result[1],
        "email": result[2],
        "role": result[4],
        "current_education": result[5],
        "budget": int(result[6]) if result[6] else None,
        "subject": result[7],
        "address": result[8],
        "grades": result[9],
        "qualification": result[10],
        "residential_zone": result[11],
        "levels_taught": result[12],
        "subjects_taught": result[13],
        "rate_per_hour": int(result[14]) if result[14] else None,
        "gender": result[15],
        "number_of_years_of_teaching_experience": result[16],
        "level": int(result[17]),
    }

def get_user_password(email):

    with psycopg2.connect(CONN_URL) as conn:

        with conn.cursor() as curs:
            curs.execute('SELECT password from "user" WHERE email=%s', (email,))
            try:
                result = curs.fetchall()[0][0]
            except:
                return None

            return result

def create_user(email, name, password):

    with psycopg2.connect(CONN_URL) as conn:

        with conn.cursor() as curs:
            curs.execute(
                '''INSERT INTO "user" (
                    id, name, email, password) VALUES (%s, %s, %s,)
                ''',
                (str(uuid.uuid4()), name, email, password)
            )

def get_matches(email: str=None, preferred_zones: list=None, preferred_qualification: list=None, preferred_gender: str=None):

    user_attr = get_user(email)

    with psycopg2.connect(CONN_URL) as conn:
        with conn.cursor() as curs:
            if preferred_zones:
                curs.execute('SELECT * FROM "user" WHERE role=%s AND level <= %s AND residential_zone = ANY(%s) AND budget >= %s AND subject = %s ORDER BY residential_zone',
             ("STUDENT", user_attr['level'], preferred_zones, user_attr["rate_per_hour"], user_attr["subjects_taught"]))
                try:
                    result = curs.fetchall()
                except:
                    return None
            if preferred_qualification:
                if preferred_gender == "No preference":
                    preferred_gender = ["Male", "Female"]
                else:
                    preferred_gender = [preferred_gender,]
                curs.execute('SELECT * FROM "user" WHERE role=%s AND level >= %s AND rate_per_hour <= %s AND subjects_taught = %s AND qualification = ANY(%s) AND gender = ANY(%s) ORDER BY residential_zone ASC, rate_per_hour ASC',
             ("TUTOR", user_attr['level'], user_attr["budget"], user_attr["subject"], preferred_qualification, preferred_gender))
                try:
                    result = curs.fetchall()
                except:
                    return None
            else:
                return None
    users_match = []
    for user in result:
        user_data = serialize_user_data(user)
        del user_data["id"]
        del user_data["level"]
        del user_data["role"]
        del user_data["budget"]
        users_match.append(user_data)
    return users_match
