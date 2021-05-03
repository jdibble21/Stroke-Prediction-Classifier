import pandas as pd
import random
import numpy as np

pd.set_option('display.max_rows', None)

PROBABILITY_CUTOFF = 0.70
FACTOR_IMPACT_LARGE = 0.18
FACTOR_IMPACT_MEDIUM = 0.10
FACTOR_IMPACT_SMALL = 0.04
K_SPLIT = 4


def predict_using_probability(gender, age, hp, hd, marry, work, residence, gluc_lvl, bmi, smoke):
    probability = 0
    if gender == "Male":
        probability += FACTOR_IMPACT_SMALL
    if age > 55:
        probability += FACTOR_IMPACT_MEDIUM
    if hp == 1:
        probability += FACTOR_IMPACT_LARGE
    if hd == 1:
        probability += FACTOR_IMPACT_LARGE
    if hd == 1 and hp == 0:
        probability -= FACTOR_IMPACT_LARGE
    if marry == "No":
        probability += FACTOR_IMPACT_SMALL
    if residence == "Rural":
        probability += FACTOR_IMPACT_SMALL
    elif residence == "Urban":
        pass
    if gluc_lvl > 200:
        probability += FACTOR_IMPACT_LARGE
    elif 199 >= gluc_lvl >= 150:
        probability += FACTOR_IMPACT_MEDIUM
    if bmi > 28.0:
        probability += FACTOR_IMPACT_LARGE
    elif 28.0 >= bmi > 25:
        probability += FACTOR_IMPACT_MEDIUM
    elif bmi < 25:
        probability -= FACTOR_IMPACT_LARGE
    if smoke == "smokes":
        probability += FACTOR_IMPACT_LARGE
    elif smoke == "formally smoked":
        probability += FACTOR_IMPACT_MEDIUM
    elif smoke == "Unknown":
        probability += FACTOR_IMPACT_SMALL
    return determine_probability_risk(probability)


def determine_probability_risk(p):
    if p < PROBABILITY_CUTOFF:
        return 0
    if p >= PROBABILITY_CUTOFF:
        return 1


def run_testing(id_array, df):
    # Set up subsets of array
    arr_split = np.array_split(np.array(id_array), K_SPLIT)
    # Save results of each run
    run_totals = []
    # Run through each split
    for i in range(0, len(arr_split)):
        k_group = arr_split[i]
        accurate_predictions = 0
        for j in range(0, len(k_group)):
            current_entry = df.loc[k_group[j]]
            accurate_predictions += test_k_sample(current_entry)
            run_totals.append(accurate_predictions/len(k_group))
    # Calculate total accuracy
    print("Accuracy:",)

def test_k_sample(x):
    k_prediction = predict_using_probability(x.loc['gender'], x.loc['age'], x.loc['hypertension'],
                                             x.loc['heart_disease'], x.loc['ever_married'], x.loc['work_type'],
                                             x.loc['Residence_type'], x.loc['avg_glucose_level'], x.loc['bmi'],
                                             x.loc['smoking_status'])
    if k_prediction == x.loc['stroke']:
        return 1
    else:
        return 0

def main():
    csv_data = pd.read_csv('data.csv', index_col="id")
    csv_data.head()
    ids = csv_data.index
    ex1 = csv_data.loc[12175]
    run_testing(ids, csv_data)


if __name__ == "__main__":
    main()
