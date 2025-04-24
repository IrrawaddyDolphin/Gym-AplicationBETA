import sqlite3
def image():
    info=sqlite3.connect("daneUzytkownika.db")
    cursor=info.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_info(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        weight REAL NOT NULL,
        height REAL NOT NULL,
        goal TEXT NOT NULL,
        years_experience INTEGER NOT NULL,
        sport_type TEXT NOT NULL       
                   )
""")
    info.commit()
    info.close()
def no_empty_input(question):
    while True:
        answer=input(question)
        if answer.strip()=="":
            print("To pole musi zostać uzupełnione")
        else:
            return answer
def addUser():
    image()
    name=no_empty_input("What's your name? ")
    age=int(input("What's your age? "))
    weight=float(input("What's your weight? (kg) "))
    height=float(input("What's your height? (cm) "))
    goal=no_empty_input("What's your goal? ")
    years_experience=float(input("How long do you train? (number_years) "))
    sport_type=no_empty_input("What's your discipline? ")
    info=sqlite3.connect("daneUzytkownika.db")
    cursor=info.cursor()
    cursor.execute("""
    INSERT INTO user_info(name,age,weight,height,goal,years_experience,sport_type)
    VALUES(?,?,?,?,?,?,?)
                   """,(name,age,weight,height,goal,years_experience,sport_type))
    info.commit()
    info.close()

def image_trainings():
    training_info=sqlite3.connect("trainingHistory.db")
    cursor=training_info.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS training_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER NOT NULL,
        date TEXT,
        sport_type TEXT,
        duration INTEGER,
        intensity INTEGER,
        addictional_notes TEXT,
        FOREIGN KEY(userId) REFERENCES user_info(id)
                   )
""")
    training_info.commit()
    training_info.close()

def addTraining(userId):
    image_trainings()
    date=input("Date of the training [RRRR-MM-DD]: ")
    sport_type=input("Type of the training day: ")
    duration=input("Duration of the session: [hh:mm] ")
    intensity=float(input("Training intensity [lowest:1-10:highest]: "))
    addictional_notes=input("Notes about training/feeling/life: ")
    training_info=sqlite3.connect("trainingHistory.db")
    cursor=training_info.cursor()
    cursor.execute("""
    INSERT INTO training_history(userId,date,sport_type,duration,intensity,addictional_notes)
    VALUES(?,?,?,?,?,?)
                   """,(userId,date,sport_type,duration,intensity,addictional_notes))
    training_info.commit()
    training_info.close()

addTraining(1)