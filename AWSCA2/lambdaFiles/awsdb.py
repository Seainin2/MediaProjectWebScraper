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

def publish_message(topic,message):
    sns = boto3.client('sns')
    response = sns.publish(TopicArn=topic,Message=message)
    messageId = response['MessageId']
    return messageId

def delete_subscription(subscription):
    subscription.delete()

def delete_topic(topic):
    topic.delete()
    
def subscribe_for_excercise(cursor):
    subs = cursor.execute("Select * FROM userSub")

    for sub in subs:
        email,number,topicArn = sub

        if len(email)>1:
            subscribe(topicArn,'email',email)
        if not number:
            subscribe(topicArn,'sms',number)
        

#if __name__ == "__main__":
def main_function(event, context):

    cursor.execute('SELECT * FROM games')
    rows = cursor.fetchall()

    for row in rows:
        
        ReleaseDate = row[1].strftime("%d %b %Y")

        if ReleaseDate == '10 May 2022':
            publish_message(row[2],f"{row[0]} has released today: {ReleaseDate}")

            