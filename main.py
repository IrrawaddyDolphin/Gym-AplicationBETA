import sqlite3
from beta_plan_generator import whats_goal,level,generate_plan
from smart_goal import get_true_goal
from user_ready import check_how_ready
from datetime import datetime, timedelta
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
        soreness_level INTEGER,
        stress_level INTEGER,
        hours_sleep INTEGER,
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
def input_soreness_and_stress_lvl(date):
    image_trainings()
    #soreness=float(input("What's your soreness for today? (1-10): "))
    #stress=float(input("How would you describe your stress levels thruout last 3 days: (1-10): "))
    sorenessstress=sqlite3.connect("trainingHistory.db")
    cursor=sorenessstress.cursor()
    #userId=int(input("Whats your user ID? "))
    cursor.execute("SELECT * FROM training_history WHERE date = ? AND userId=?",(date,userId))
    wynik=cursor.fetchone()
    if wynik:
        #userId=int(input("Whats your user ID? "))
        soreness=float(input("What's your soreness for today? (1-10): "))
        stress=float(input("How would you describe your stress levels thruout last 3 days: (1-10): "))
        cursor.execute("""UPDATE training_history SET soreness_level = ?, stress_level = ?
                    WHERE date = ? AND userId = ?
        """,(soreness,stress,date,userId))
    else:
        #userId=int(input("What's your user's ID? "))
        soreness=float(input("What's your soreness for today? (1-10): "))
        stress=float(input("How would you describe your stress levels thruout last 3 days: (1-10): "))
        cursor.execute("""INSERT INTO training_history(userId,date,soreness_level, stress_level)
        VALUES(?,?,?,?)
                   """,(userId,date,soreness,stress))
    sorenessstress.commit()
    sorenessstress.close()
def input_sleep(data):
    #userId=int(input("What's your user ID? "))
    image_trainings()
    conn=sqlite3.connect("trainingHistory.db")
    cursor=conn.cursor()
    sleep=float(input("How much hours of sleep did you get this night? "))
    cursor.execute("""UPDATE training_history SET hours_sleep = ? WHERE date =? AND userId=?""",(sleep,date,userId))
    conn.commit()
    conn.close()
prawda=True
while prawda:
    print("1. Add user")
    print("2. Add training")
    print("3. Generate plan for me")
    print("4. At the morning: Input hours of sleep and update your soreness and stress levels")
    print("5. Check how hard should I train today")
    print("X. Bye: type anything")
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
        print(goal1)
        #goal=whats_goal(goal1)
        goal2=get_true_goal(goal1)
        print(generate_plan(users_lvl,goal2))
    #For now lets start with 3 levels of "being ready" fatiqued/mid ready/ready
    #generate_plan should return training for each lvl [streching/from main sets -1 set/go full in]
    #input=h of sleep, fatique, stress, kcal from previous day x/2600(for example)
    elif choice=="4":
        if input("Do you want to input other date then yesterdays? Y/N ")=="Y":
            date=input("Date: ")
        else:
            date=(datetime.today()-timedelta(days=1)).strftime("%Y-%m-%d")
        userId=int(input("What's your user ID? "))
        input_soreness_and_stress_lvl(date)
        input_sleep(date)
    elif choice=="5":
        userId=int(input("What's your user ID? "))
        sore,stress,sleep,avg_intensity=check_how_ready(userId)
        print(sore,stress,sleep,avg_intensity)
        if None in (sore, stress, sleep, avg_intensity):
            print("Brakuje wprowadzenia danych do oceny")
        else:
            if sleep*0.6-sore*0.4-stress*0.3-avg_intensity*0.2<-7:
                print("GO TO SLEEP")
            elif sleep*0.6-sore*0.4-stress*0.3-avg_intensity*0.2<-3:
                print("Light")
            elif -3<=sleep*0.6-sore*0.4-stress*0.3-avg_intensity*0.2<3:
                print("Medium")
            elif 3<=sleep*0.6-sore*0.4-stress*0.3-avg_intensity*0.2<=10:
                print("Hard")
    else:
        prawda=False

    #BTW I SHOULD INSERT INFO ABOUT SORENESS ETC. TO TODAYS DATE
    #AND AFTER THAT I SHOULD UPDATE TRAINING INFO
    #BUT FOR NOW LETS KEEP IT THAT WAY