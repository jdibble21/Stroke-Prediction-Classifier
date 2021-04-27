import pandas as pd
pd.set_option('display.max_rows', None)
import numpy as np

PROBABILITY_CUTOFF = 0.70
FACTOR_IMPACT_LARGE = 0.15
FACTOR_IMPACT_SMALL = 0.04

def predict_using_decision_tree(gender,age,hp,smoke):
    if(smoke == "smokes"):
        if(age >= 55 or gender == "Male"):
            return "yes"
        if(hp == 1):
            return "yes"
        return "no"
    if(smoke == "formally smoked"):
        if(age >= 65):
            return "yes"
        if(hp == 1):
            return "yes"    
    if(smoke == "never smoked"):
        if(hp == 1):
            return "yes"
        return "no"
    return "no"
    
def predict_using_probability(gender,age,hp,hd,marry,work,residence,gluc_lvl,bmi,smoke):
    probability = 0.20
    if(gender == "male"):
        probability += 0.10
        if(age > 55):
            probability += FACTOR_IMPACT_LARGE
        if(hp == 1):
            probability += FACTOR_IMPACT_LARGE
        if(hd == 1):
            probability += FACTOR_IMPACT_LARGE
        if(marry == "No"):
            probability += FACTOR_IMPACT_SMALL
        if(residence == "Rural"):
            probability += FACTOR_IMPACT_SMALL
        if(gluc_lvl >150):
            probability += FACTOR_IMPACT_LARGE
        if(bmi > 25.0):
            probability += FACTOR_IMPACT_LARGE
        if(smoke > "smokes"):
            probability += FACTOR_IMPACT_LARGE
    elif(gender == "Female"):
        pass

def determine_probability_risk(prob):
    pass

def output_sample_case_data(num,s,p):
    smk_status = ""
    if(s.loc['smoking_status'] == "Unknown"):
        smk_status = "unknown smoking status"
    else:
        smk_status = "who "+str(s.loc['smoking_status'])
    frmt = "will not"
    if(p == "yes"):
        frmt = " will"
    hp = "no"
    if(s.loc['hypertension'] == 1):
        hp = ""
    print("Patient number",num,": Age",s.loc['age'],s.loc['gender'],"with",hp,"hypertension and",smk_status)
    print("Prediction: "+str(p)+", patient "+str(num)+" "+str(frmt)+" have a stroke")
    print("\n")
    
def predict_sample_use_cases(df):
    case_one = df.loc[4219]
    case_two = df.loc[72911]
    case_three = df.loc[27419]
    predict_one = predict_using_decision_tree(case_one.loc['gender'],case_one.loc['age'],case_one.loc['hypertension'],case_one.loc['smoking_status'])
    predict_two = predict_using_decision_tree(case_two.loc['gender'],case_two.loc['age'],case_two.loc['hypertension'],case_two.loc['smoking_status'])
    predict_three = predict_using_decision_tree(case_three.loc['gender'],case_three.loc['age'],case_three.loc['hypertension'],case_three.loc['smoking_status'])
    output_sample_case_data(1,case_one,predict_one)
    output_sample_case_data(2,case_two,predict_two)
    output_sample_case_data(3,case_three,predict_three)

    
def main():
    csv_data = pd.read_csv('data.csv',index_col ="id")
    csv_data.head()
    ex = csv_data.loc[34120]
    predict = predict_using_decision_tree(ex.loc['gender'],ex.loc['age'],ex.loc['hypertension'],ex.loc['smoking_status'])
    ids = csv_data.index
    print("\n")
    predict_sample_use_cases(csv_data)
    #print(ids[0]) save for later: loop through all ids in dataframe
    #print(ex)
    #print(predict)

if __name__ == "__main__":
    main()