import pyodbc
import time
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

def connect_to_db():
    server = 'sqldatabase.cwwsgvmp21sg.us-east-1.rds.amazonaws.com'
    database = 'GamesDatabase'
    username = 'Seainin'
    password = 'password'
    cnxn = pyodbc.connect('DRIVER={ODBC DRIVER 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password+';Encrypt=yes;TrustServerCertificate=yes')
    return  cnxn.cursor()

def subscribe(topic,protocol,endpoint):
    print(f'Endpoint: {endpoint}')
    sns = boto3.client('sns')
    subscription = sns.subscribe(TopicArn=topic,Protocol=protocol,Endpoint=endpoint,ReturnSubscriptionArn=True)
    return subscription

def subscribe_for_excercise(cursor):
    subs = cursor.execute("Select * FROM userSub")

    for sub in subs:
        email,number,topicArn = sub

        if len(email)>1:
            subscribe(topicArn,'email',email)
        if not number:
            subscribe(topicArn,'sms',number)

if __name__ == "__main__":
    print('Connecting to db')
    
    cursor = connect_to_db()
    print("Connected to database")
    sql_file = open("db-schema.sql")
    print("Reading database schema from file")
    sql_as_string = sql_file.read()
    print("Writing schema to rds database")
    cursor.execute(sql_as_string)
    print("succes")

    games = cursor.execute("Select * from games")
    for game in games:
        answer = input(f"Do you want to subscribe to {game[1]}")
        if answer == "yes":
            email = input("What is the email you would like to be notified on?")
            data = (email,game[2])
            cursor.execute("Insert into [dbo].[userSub] (email,TopicArn) VALUES (?,?)"+data)

    subscribe_for_excercise(cursor)