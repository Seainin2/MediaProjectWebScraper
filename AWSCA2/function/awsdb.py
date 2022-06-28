import pyodbc
import time
import boto3
from botocore.exceptions import ClientError
from datetime import datetime



def connect_to_db(key):
    #server = ' 'key
    server = 'tcp:'+key+',3306'
    database = 'GamesDatabase'
    #port = '3306'
    username = 'Seainin'
    password = 'password'
    #cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:mysqlserverseaininkeenan.database.windows.net,1433;Database=MediaApiDb;Uid=seaininkeenan;Pwd=;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server='+server+';Database='+database+';Uid='+username+';Pwd='+password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=15;')
    return  cnxn.cursor()

def subscribe(topic,protocol,endpoint):
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

def create_topic(name):
    sns = boto3.resource("sns")
    topic = sns.create_topic(Name=name)
    return topic
    
def list_topics():
    sns = boto3.resource("sns")
    topics_iter = sns.topics.all()
    return topics_iter
    

#if __name__ == "__main__":
def main_function(event, context):
    print(event)

    key = event['server']
    
    cursor = connect_to_db(key)
    Name = 'Witcher'
    
    topic1 = create_topic(Name)
    print(topic1.arn)
    cursor.execute("Insert into [dbo].[games](Title,TopicArn) Values (?,?)",Name,topic1.arn)
    cursor.commit()
    
    Name = 'Zelda'
    topic2 = create_topic(Name)
    cursor.execute("Insert into [dbo].[games] (Title,TopicArn) Values (?,?)",Name,topic2.arn)
    cursor.commit()
    

    cursor.execute('SELECT * FROM [dbo].[games]')
    rows = cursor.fetchall()

    for row in rows:
        
        
        subscribe(row[2],'email',event['email'])

        
    time.sleep(60)
    
    for row in rows:
        publish_message(row[2],f"You will be notified when {row[0]} Releases!!!!!!! YYYAAAAYYY")
        
    cursor.execute("Delete from games")

            