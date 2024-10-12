#import packages
import mysql.connector as sql
import pandas as pd

#sql connection
mydb=sql.connect(host="localhost",user="root",password="root",database= "github",port = "3306")
cursor=mydb.cursor(buffered=True)

#load dataset
df = pd.read_csv(r"C:\Users\HP\Downloads\github_repositories1.csv")

#function insert table
def insert_repositories_data():
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS repositories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Repository_Name VARCHAR(255),
            Owner VARCHAR(255), Description TEXT,
            URL VARCHAR(255),
            Programming_Language VARCHAR(100),
            Creation_Date DATETIME,
            Last_Updated_Date DATETIME,
            Number_of_Stars INT,
            Number_of_Forks INT,
            Number_of_Open_Issues INT,
            License_Type VARCHAR(100)
            
        )
    """)
    
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO repositories (
                Repository_Name, Owner, Description, URL, Programming_Language, Creation_Date,
                Last_Updated_Date, Number_of_Stars, Number_of_Forks, Number_of_Open_Issues, License_Type
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Repository_Name'], row['Owner'], row['Description'] , row['URL'],
            row['Programming_Language'] , row['Creation_Date'], row['Last_Updated_Date'],
            row['Number_of_Stars'], row['Number_of_Forks'], row['Number_of_Open_Issues'], row['License_Type'] 
        ))
    
    
    mydb.commit()
    
insert_repositories_data()