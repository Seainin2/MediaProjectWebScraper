import json
import pyodbc
from datetime import datetime

DB_CONNECTION = ''


def connect_to_db():
    cnxn = pyodbc.connect(DB_CONNECTION)
    return cnxn.cursor()
    
def publish_message(topic,message):
    sns = boto3.client('sns')
    response = sns.publish(TopicArn=topic,Message=message)
    messageId = response['MessageId']
    return messageId
    

def lambda_handler(event, context):
    
    thedate = datetime.today().strftime('%Y-%m-%d')
    print(thedate)
    
    cursor = connect_to_db()
    
    cursor.execute('SELECT * FROM [dbo].[games]')
    games = cursor.fetchall()
    
    for game in games:
        print('Title: '+game[4]+' Date: '+str(game[8]))
        if thedate == str(game[8]):
            print('arn:aws:sns:us-east-1:389076917675:'+game[4].replace(' ',''),f'{game[4]} released Today!!!')
            #publish_message('arn:aws:sns:us-east-1:389076917675:'+game[4].replace(' ',''),f'{game[4]} released Today!!!')
            
    cursor.execute('SELECT * FROM [dbo].[movies]')
    movies = cursor.fetchall()
    
    for movie in movies:
        print('Title: '+movie[4]+' Date: '+str(movie[8]))
        if thedate == str(movie[8]):
            print('arn:aws:sns:us-east-1:389076917675:'+movie[4].replace(' ',''),f'{gmovie[4]} released Today!!!')
            #publish_message('arn:aws:sns:us-east-1:389076917675:'+movie[4].replace(' ',''),f'{movie[4]} released Today!!!')
            
    cursor.execute('SELECT * FROM [dbo].[books]')
    books = cursor.fetchall()
    
    for book in books:
        print('Title: '+book[4]+' Date: '+str(book[8]))
        if thedate == str(book[8]):
            print('arn:aws:sns:us-east-1:389076917675:'+book[4].replace(' ',''),f'{book[4]} released Today!!!')
            #publish_message('arn:aws:sns:us-east-1:389076917675:'+book[4].replace(' ',''),f'{book[4]} released Today!!!')
            
    cursor.execute('SELECT * FROM [dbo].[shows]')
    shows = cursor.fetchall()
    
    for show in shows:
        print('Title: '+show[4]+' Date: '+str(show[8]))
        if thedate == str(show[8]):
            print('arn:aws:sns:us-east-1:389076917675:'+show[4].replace(' ',''),f'{show[4]} released Today!!!')
            #publish_message('arn:aws:sns:us-east-1:389076917675:'+game[4].replace(' ',''),f'{game[4]} released Today!!!')
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
