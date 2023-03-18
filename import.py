import csv
import os
from colorama import init, Fore, Back, Style
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader)
    for isbn, title, author, year in reader:
        try:
            consulta = text("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)")
            db.execute(consulta, {"isbn": isbn, "title": title, "author": author, "year": year})
            print(consulta)
            print(Fore.GREEN + "successful" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "Error" + Style.RESET_ALL)
        
    db.commit()
    
if __name__ == "__main__":
    main()