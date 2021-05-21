import pandas as pd
import random
import numpy as np

pd.set_option('display.max_rows', None)
strokes = 0
PROBABILITY_CUTOFF = 0.50
FACTOR_IMPACT_LARGE = 0.37
FACTOR_IMPACT_MEDIUM = 0.25
FACTOR_IMPACT_SMALL = 0.10
BMI_UPPER_BOUND = 27.0
BMI_LOWER_BOUND = 21.75
GLUCOSE_LVL_UPPER_BOUND = 200.0
GLUCOSE_IMPACT_LARGE = 0.80
GLUCOSE_LVL_LOWER_BOUND = 130.0
K_SPLIT = 4


def predict_using_probability(gender, age, hp, hd, marry, work, residence, gluc_lvl, bmi, smoke):
    probability = 0.10
    if gender == "Male":
        probability += FACTOR_IMPACT_MEDIUM
    if 70 > age > 55:
        probability += FACTOR_IMPACT_SMALL
    if 55 >= age > 40:
        probability -= FACTOR_IMPACT_SMALL
    if 40 >= age > 20:
        probability -= FACTOR_IMPACT_MEDIUM
    if age <= 20:
        probability -= FACTOR_IMPACT_LARGE
    if hp == 1:
        probability += FACTOR_IMPACT_MEDIUM
    if hd == 1:
        probability += FACTOR_IMPACT_MEDIUM
    if hd == 1 and hp == 0:
        probability -= FACTOR_IMPACT_LARGE
    if marry == "No":
        probability += FACTOR_IMPACT_SMALL
    if residence == "Rural":
        probability += FACTOR_IMPACT_SMALL
    if residence == "Urban":
        pass
    if gluc_lvl > GLUCOSE_LVL_UPPER_BOUND:
        probability += GLUCOSE_IMPACT_LARGE
    if GLUCOSE_LVL_UPPER_BOUND >= gluc_lvl >= GLUCOSE_LVL_LOWER_BOUND:
        probability += FACTOR_IMPACT_MEDIUM
    if gluc_lvl < GLUCOSE_LVL_LOWER_BOUND:
        probability -= FACTOR_IMPACT_SMALL
    if bmi > BMI_UPPER_BOUND:
        probability += FACTOR_IMPACT_LARGE
    if BMI_UPPER_BOUND >= bmi >= BMI_LOWER_BOUND:
        probability += FACTOR_IMPACT_MEDIUM
    if bmi < BMI_LOWER_BOUND:
        probability -= FACTOR_IMPACT_LARGE
    if bmi == "N/A":
        probability += FACTOR_IMPACT_LARGE
    if smoke == "smokes":
        probability += FACTOR_IMPACT_LARGE
    if smoke == "formally smoked":
        probability += FACTOR_IMPACT_MEDIUM
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
            run_totals.append(accurate_predictions / len(k_group))
    # Calculate total accuracy
    accuracy = (sum(run_totals) / len(run_totals)) * 100
    format_accuracy = "{:.3f}".format(accuracy)
    print("Accuracy:", str(format_accuracy + "%"))


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
    run_testing(ids, csv_data)


if __name__ == "__main__":
    main()
