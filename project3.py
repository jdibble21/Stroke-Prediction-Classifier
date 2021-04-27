import pandas as pd
pd.set_option('display.max_rows', None)
import numpy as np

PROBABILITY_CUTOFF = 0.70
FACTOR_IMPACT_LARGE = 0.15
FACTOR_IMPACT_SMALL = 0.04

def predict_using_descision_tree(gender,age,hp,smoke):
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

def main():
    csv_data = pd.read_csv('data.csv',index_col ="id")
    csv_data.head()
    print(csv_data)

if __name__ == "__main__":
    main()