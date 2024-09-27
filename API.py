import requests
import psycopg2
from psycopg2 import sql

def insert(data):
    conn = psycopg2.connect(dbname="fullstack", user="postgres", password="12345", host="localhost")
    cursor = conn.cursor()
    insert_query = sql.SQL("INSERT INTO jokes (id, type, setup, punchline) VALUES (%s, %s, %s,%s) ON CONFLICT (id) DO NOTHING")
    cursor.execute(insert_query, (data['id'], data['type'], data['setup'], data['punchline']))
    conn.commit()
    cursor.close()
    conn.close()

def get_data():
    conn = psycopg2.connect(dbname="fullstack", user="postgres", password="12345", host="localhost")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jokes")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def api():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)

    if response.ok: 
        data = response.json()
        return data
    


def main():
   choice = input("Choose an action:\n1. Show a joke\n2. Show saved jokes\n")

   match choice:
    case '1':
       joke = api()
       print(f"Id: {joke['id']} Type: {joke['type']} \nJoke: {joke['setup']} - {joke['punchline']}")
       insert(joke) 

    case '2':
      jokes = get_data()
      if jokes:  
        for joke in jokes:
            print(f"ID: {joke[0]}\nType: {joke[1]}\nSetup: {joke[2]}\nPunchline: {joke[3]}\n")
    case _:
        print("There is no such option. try 1 or 2")

if __name__ == "__main__":
    main()