import sqlite3
from beta_plan_generator import whats_goal,level,generate_plan
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

def get_info_about_user_years(userId):
    info=sqlite3.connect("daneUzytkownika.db")
    cursor=info.cursor()
    query="SELECT * FROM user_info WHERE id = ?"
    cursor.execute(query, (userId,))
    result = cursor.fetchone()
    result=result[6]
    info.close()

    return result
def get_info_about_user_goal(userId):
    info=sqlite3.connect("daneUzytkownika.db")
    cursor=info.cursor()
    query="SELECT * FROM user_info WHERE id = ?"
    cursor.execute(query, (userId,))
    result = cursor.fetchone()
    result= result[5]
    info.close()

    return result

print("1. Add user")
print("2. Add training")
print("3. Generate plan for me")
choice=input("What would you like to do? (type number) ")
if choice=="1":
    addUser()
elif choice=="2":
    id=int(input("What's your id? "))
    addTraining(id)
elif choice=="3":
    id=int(input("What's your id? "))
    number=get_info_about_user_years(id)
    users_lvl=level(number)
    goal1=get_info_about_user_goal(id)
    goal=whats_goal(goal1)
    print(generate_plan(users_lvl,goal))