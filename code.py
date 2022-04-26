import pyodbc

with pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:mysqlserverseaininkeenan.database.windows.net,1433;Database=MediaApiDb;Uid=seaininkeenan;Pwd=1Azurepassword;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;') as conn:
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO [dbo].[Books] (MediaId,SeriesId,CreatingPropertyId,MediaType,Title,Description,NumberofTimesSearched,Length,ReleaseDate) VALUES (NEWID(),NEWID(),NEWID(),'book','New Book','this is a description',1,100,CONVERT(DATE, '2020/07/21'))")

	#cursor.execute("SELECT * FROM [dbo].[Books]")
        #row = cursor.fetchone()
        #while row:
            #print (str(row))
            #row = cursor.fetchone()