def whats_goal(goal):
    goal=goal.lower()
    if "bulk" in goal and "strength" in goal:
        return "bulk_strength"
    elif "bulk" in goal and "hypertrophy" in goal:
        return "bulk_hypertrophy"
    elif "cut" in goal and "hypertrophy" in goal:
        return "cut_hypertrophy"
    elif "cut" in goal and "strength" in goal:
        return "cut_strength"
    elif "maintain" in goal and "strength" in goal:
        return "maintain_strength"
    elif "maintain" in goal and "hypertrophy" in goal:
        return "maintain_hypertrophy"
    
def level(years_experience,bench=None,squat=None,deadlift=None, body_weight=None):
    if bench==None and squat==None and deadlift==None:
        if years_experience<1:
            return "beginner"
        elif 1 <=years_experience<5:
            return "intermediate"
        else:
            return "advanced"
    elif bench/body_weight>=2 or squat/body_weight>=3 or deadlift/body_weight>=4:
        return "advanced"    


def generate_plan(user_level, goal):
    plans= {
        "FBW" : ["FBW 3x/week mid volume ", "FBW with progression"],
        "Push Pull Legs": ["PPL x2/week", "PPL with few strenght days"],
        "Upper Lower": ["Upper Lower x2/week","Upper Lower x3/week"],
        "Cardio": ["HIIT + LISS","Addictional short cardio after workout"],
        "Strength": ["5x5", "SBD split"],
        "Hypertrophy": ["x2/week every muscle with being close to failure","x2/week one hard training one lighter"]
    }  
    plan=[]

    if goal=="bulk_strength":
        if user_level == "beginner":
            plan = [plans["FBW"][1], plans["Push Pull Legs"][1]]
        elif user_level == "intermediate":
            plan = [plans["Upper Lower"][1], plans["Strength"][0], plans["Strength"][1]]
        else:
            plan = [plans["Upper Lower"][1], plans["Strength"][1]]
    elif goal=="bulk_hypertrophy":
        if user_level == "beginner":
            plan = [plans["FBW"][1], plans["Push Pull Legs"][1]]
        elif user_level == "intermediate":
            plan = [plans["Upper Lower"][1], plans["Strength"][0], plans["Strength"][1]]
        else:
            plan = [plans["Upper Lower"][1], plans["Strength"][1]]
    elif goal=="cut_hypertrophy":
        if user_level == "beginner":
            plan = [plans["FBW"][1], plans["Push Pull Legs"][1]]
        elif user_level == "intermediate":
            plan = [plans["Upper Lower"][1], plans["Strength"][0], plans["Strength"][1]]
        else:
            plan = [plans["Upper Lower"][1], plans["Strength"][1]]
    elif goal=="cut_strength":
        if user_level == "beginner":
            plan = [plans["FBW"][1], plans["Push Pull Legs"][1]]
        elif user_level == "intermediate":
            plan = [plans["Upper Lower"][1], plans["Strength"][0], plans["Strength"][1]]
        else:
            plan = [plans["Upper Lower"][1], plans["Strength"][1]]
    
    elif goal=="maintain_strength":
        if user_level == "beginner":
            plan = [plans["FBW"][1], plans["Push Pull Legs"][1]]
        elif user_level == "intermediate":
            plan = [plans["Upper Lower"][1], plans["Strength"][0], plans["Strength"][1]]
        else:
            plan = [plans["Upper Lower"][1], plans["Strength"][1]]
    elif goal=="maintain_hypertrophy":
        if user_level == "beginner":
            plan = [plans["FBW"][1], plans["Push Pull Legs"][1]]
        elif user_level == "intermediate":
            plan = [plans["Upper Lower"][1], plans["Strength"][0], plans["Strength"][1]]
        else:
            plan = [plans["Upper Lower"][1], plans["Strength"][1]]
    return plan

