import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)


class StrokeDTClassifier:

    def __init__(self, csv_filename, index):
        self.dataframe = pd.read_csv(csv_filename, index_col=index)
        self.dataframe.head()
        self.index_ids = self.dataframe.index
        self.PROBABILITY_CUTOFF = 0.50
        self.FACTOR_IMPACT_LARGE = 0.37
        self.FACTOR_IMPACT_MEDIUM = 0.25
        self.FACTOR_IMPACT_SMALL = 0.10
        self.BMI_UPPER_BOUND = 27.0
        self.BMI_LOWER_BOUND = 21.75
        self.GLUCOSE_LVL_UPPER_BOUND = 210.0
        self.GLUCOSE_IMPACT_LARGE = 0.80
        self.GLUCOSE_LVL_LOWER_BOUND = 125.0
        self.K_SPLIT = 4

    def run_testing(self, id_array, df):
        # Set up subsets of array
        arr_split = np.array_split(np.array(id_array), self.K_SPLIT)
        # Save results of each run
        run_totals = []
        # Run through each split
        for i in range(0, len(arr_split)):
            k_group = arr_split[i]
            accurate_predictions = 0
            for j in range(0, len(k_group)):
                current_entry = df.loc[k_group[j]]
                accurate_predictions += self.test_k_sample(current_entry)
                run_totals.append(accurate_predictions / len(k_group))
        # Calculate total accuracy
        accuracy = (sum(run_totals) / len(run_totals)) * 100
        format_accuracy = "{:.3f}".format(accuracy)
        print("Classifier Accuracy:", str(format_accuracy + "%"))
        print("Predicted", len(id_array), "labels")

    def test_accuracy(self):
        ids = self.dataframe.index
        self.run_testing(ids, self.dataframe)

    def test_k_sample(self, x):
        k_prediction = self.predict_using_probability(x.loc['gender'], x.loc['age'], x.loc['hypertension'],
                                                      x.loc['heart_disease'], x.loc['ever_married'], x.loc['work_type'],
                                                      x.loc['Residence_type'], x.loc['avg_glucose_level'], x.loc['bmi'],
                                                      x.loc['smoking_status'])
        if k_prediction == x.loc['stroke']:
            return 1
        else:
            return 0

    def predict_using_probability(self, gender, age, hp, hd, marry, work, residence, gluc_lvl, bmi, smoke):
        probability = 0.10
        if gender == "Male":
            probability += self.FACTOR_IMPACT_MEDIUM
        if 70 > age > 55:
            probability += self.FACTOR_IMPACT_SMALL
        if 55 >= age > 40:
            probability -= self.FACTOR_IMPACT_SMALL
        if 40 >= age > 20:
            probability -= self.FACTOR_IMPACT_MEDIUM
        if age <= 20:
            probability -= self.FACTOR_IMPACT_LARGE
        if hp == 1:
            probability += self.FACTOR_IMPACT_MEDIUM
        if hd == 1:
            probability += self.FACTOR_IMPACT_MEDIUM
        if hd == 1 and hp == 0:
            probability -= self.FACTOR_IMPACT_LARGE
        if marry == "No":
            probability += self.FACTOR_IMPACT_SMALL
        if residence == "Rural":
            probability += self.FACTOR_IMPACT_SMALL
        if residence == "Urban":
            pass
        if gluc_lvl > self.GLUCOSE_LVL_UPPER_BOUND:
            probability += self.GLUCOSE_IMPACT_LARGE
        if self.GLUCOSE_LVL_UPPER_BOUND >= gluc_lvl >= self.GLUCOSE_LVL_LOWER_BOUND:
            probability += self.FACTOR_IMPACT_MEDIUM
        if gluc_lvl < self.GLUCOSE_LVL_LOWER_BOUND:
            probability -= self.FACTOR_IMPACT_SMALL
        if bmi > self.BMI_UPPER_BOUND:
            probability += self.FACTOR_IMPACT_LARGE
        if self.BMI_UPPER_BOUND >= bmi >= self.BMI_LOWER_BOUND:
            probability += self.FACTOR_IMPACT_MEDIUM
        if bmi < self.BMI_LOWER_BOUND:
            probability -= self.FACTOR_IMPACT_LARGE
        if bmi == "N/A":
            probability += self.FACTOR_IMPACT_LARGE
        if smoke == "smokes":
            probability += self.FACTOR_IMPACT_LARGE
        if smoke == "formally smoked":
            probability += self.FACTOR_IMPACT_MEDIUM
        return self.determine_probability_risk(probability)

    def determine_probability_risk(self, p):
        if p < self.PROBABILITY_CUTOFF:
            return 0
        if p >= self.PROBABILITY_CUTOFF:
            return 1
