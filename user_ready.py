import sqlite3
from datetime import datetime, timedelta
import pandas as pd


#userId=input("Whats your userId? ")
def check_how_ready(userId):
    conn=sqlite3.connect("trainingHistory.db")
    date_end=datetime.today().date()
    date_start=date_end -timedelta(days=3)
    #df=pd.read_sql_query("SELECT addictional_notes FROM training_history", conn)
    wait="""SELECT intensity,addictional_notes FROM training_history WHERE userId=? AND date BETWEEN ? AND ? ORDER BY date ASC"""
    wait1="""SELECT soreness_level,stress_level FROM training_history WHERE userId=? AND date=?"""
    df= pd.read_sql_query(wait,conn,params=(userId,date_start,date_end))
    df1=pd.read_sql_query(wait1,conn,params=(userId,date_end-timedelta(days=1)))
    conn.close()
    print(df.head())
    print(df1.head(1))
    avg_intensity=df["intensity"].sum()/len(df["intensity"])
    sore=df1.loc[0,"soreness_level"]
    stress=df1.loc[0,"stress_level"]
    print(sore,stress,avg_intensity)
check_how_ready(1)