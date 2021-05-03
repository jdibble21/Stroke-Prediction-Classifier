import pandas as pd

pd.set_option('display.max_rows', None)

PROBABILITY_CUTOFF = 0.70
FACTOR_IMPACT_LARGE = 0.18
FACTOR_IMPACT_MEDIUM = 0.10
FACTOR_IMPACT_SMALL = 0.04


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
    return probability


def determine_probability_risk(p):
    if p < PROBABILITY_CUTOFF:
        return "No"
    if p >= PROBABILITY_CUTOFF:
        return "Yes"


def main():
    csv_data = pd.read_csv('data.csv', index_col="id")
    csv_data.head()
    ids = csv_data.index
    ex1 = csv_data.loc[12175]
    pred1 = predict_using_probability(ex1.loc['gender'], ex1.loc['age'], ex1.loc['hypertension'],
                                      ex1.loc['heart_disease'], ex1.loc['ever_married'], ex1.loc['work_type'],
                                      ex1.loc['Residence_type'], ex1.loc['avg_glucose_level'], ex1.loc['bmi'],
                                      ex1.loc['smoking_status'])
    print(ex1)
    print("\n")
    print(pred1)
    print(determine_probability_risk(pred1))
    # print(ids[0]) save for later: loop through all ids in dataframe
    # print(ex)
    # print(predict)


if __name__ == "__main__":
    main()
