# ### Data Preparation and Analysis
# 1. Load the dataset containing control and test group data from "ab_testing.xlsx" and assign them to separate
# variables.
# 2. Analyze the control and test group data.

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 1500)

control_df = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")
test_df = pd.read_excel("ab_testing.xlsx", sheet_name="Test Group")


def check_df(dataframe, head=5):
    print("#################### Shape ####################")
    print(dataframe.shape)
    print("#################### Types ####################")
    print(dataframe.dtypes)
    print("#################### Num of Unique ####################")
    print(dataframe.nunique())  # "dataframe.nunique(dropna=False)" yazarsak null'larıda veriyor.
    print("#################### Head ####################")
    print(dataframe.head(head))
    print("#################### Tail ####################")
    print(dataframe.tail(head))
    print("#################### NA ####################")
    print(dataframe.isnull().sum())
    print("#################### Quantiles ####################")
    print(dataframe.describe([0.01, 0.05, 0.75, 0.90, 0.95, 0.99]).T)


check_df(control_df)
check_df(test_df)


def grab_col_names(dataframe, cat_th=16, car_th=20):
    """

    Veri setindeki kategorik, numerik ve kategorik fakat kardinal değişkenlerin isimlerini verir.
    Not: Kategorik değişkenlerin içerisine numerik görünümlü kategorik değişkenler de dahildir.

    Parameters
    ------
        dataframe: dataframe
                Değişken isimleri alınmak istenilen dataframe
        cat_th: int, optional
                numerik fakat kategorik olan değişkenler için sınıf eşik değeri
        car_th: int, optinal
                kategorik fakat kardinal değişkenler için sınıf eşik değeri

    Returns
    ------
        cat_cols: list
                Kategorik değişken listesi
        num_cols: list
                Numerik değişken listesi
        cat_but_car: list
                Kategorik görünümlü kardinal değişken listesi

    Examples
    ------
        import seaborn as sns
        df = sns.load_dataset("iris")
        print(grab_col_names(df))


    Notes
    ------
        cat_cols + num_cols + cat_but_car = toplam değişken sayısı
        num_but_cat cat_cols'un içerisinde.
        Return olan 3 liste toplamı toplam değişken sayısına eşittir: cat_cols + num_cols + cat_but_car = değişken
        sayısı

    """

    # cat_cols, cat_but_car
    cat_cols = [col for col in dataframe.columns if dataframe[col].dtypes == "O"]
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and
                   dataframe[col].dtypes != "O"]
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and
                   dataframe[col].dtypes == "O"]
    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    # num_cols
    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes != "O"]
    num_cols = [col for col in num_cols if col not in num_but_cat]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f'cat_cols: {len(cat_cols)}')
    print(f'num_cols: {len(num_cols)}')
    print(f'cat_but_car: {len(cat_but_car)}')
    print(f'num_but_cat: {len(num_but_cat)}')
    return cat_cols, num_cols, cat_but_car


cat_cols, num_cols, cat_but_car = grab_col_names(control_df)
cat_cols, num_cols, cat_but_car = grab_col_names(test_df)


def num_summary(dataframe):
    num_cols = dataframe.select_dtypes(include=['int', 'float']).columns
    num_count = len(num_cols)

    # Her bir sayısal değişken için bir satır ve iki sütunlu subplotlar oluşturun
    fig, axes = plt.subplots(num_count, 2, figsize=(12, 4 * num_count))
    plt.subplots_adjust(left=0.1, right=0.9, hspace=0.5)

    for i, col in enumerate(num_cols):
        sns.histplot(data=dataframe, x=col, kde=True, ax=axes[i, 0])
        axes[i, 0].set_title(f'{col} Histogram')

        sns.boxplot(x=dataframe[col], ax=axes[i, 1])
        axes[i, 1].set_title(f'{col} Boxplot')

    plt.show(block=True)


num_summary(control_df)

# ### Defining the Hypothesis for A/B Testing
# 1. Define the null and alternative hypotheses for the A/B test.
# 2. Analyze the purchase (earnings) means for the control and test groups.

"""
H0: M1 = M2 (There is no significant difference in the average purchases between the control and test groups.)
H1: M1 ≠ M2 (There is a significant difference in the average purchases between the control and test groups.)
"""

control_df["Earning"].mean()  # 1908.57
control_df["Purchase"].mean()  # 550.89

test_df["Earning"].mean()  # 2514.90
test_df["Purchase"].mean()  # 582.11

"""
test_df["Purchase"] > control_df["Purchase"]
test_df["Earning"] > control_df["Earning"]
"""

# ### Performing the Hypothesis Test
# 1. Conduct assumption checks before the hypothesis test, including normality assumption and homogeneity of variances.
# 2. Select the appropriate test based on the assumption results.
# 3. Interpret the test results and determine if there is a statistically significant difference in purchase means
# between the control and test groups.

"""
Normality Assumption:
H0: The data follows a normal distribution.
H1: The data does not follow a normal distribution.

---> Use the Shapiro-Wilk test to check normality for both control and test groups.

p > 0.05: The data follows a normal distribution.
p < 0.05: The data does not follow a normal distribution.


Homogeneity of Variance:
H0: The variances are equal.
H1: The variances are not equal.

---> Use the Levene test to check homogeneity of variance for both groups.

p > 0.05: The variances are equal.
p < 0.05: The variances are not equal.
"""

test_stat, pvalue = shapiro(control_df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9773, p-value = 0.5891 - p > 0.05: The data follows a normal distribution.

test_stat, pvalue = levene(control_df["Purchase"],
                           test_df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 2.6393, p-value = 0.1083 - p > 0.05: The variances are equal.


"""
Since the assumptions are met, perform an independent two-sample t-test (parametric test).
H0: M1 = M2 (There is no significant difference in average purchases between the control and test groups.)
H1: M1 ≠ M2 (There is a significant difference in average purchases between the control and test groups.)
"""

test_stat, pvalue = ttest_ind(control_df["Purchase"],
                              test_df["Purchase"],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = -0.9416, p-value = 0.3493 - p > 0.05: There is no significant difference in average purchases between the
# control and test groups.


# ### Analysis of Results
"""
Based on the results of this A/B test:

1- First, we examined the average purchase amounts for the control group and the test group. The average purchase amount 
for the control group was found to be 550.89, while the average purchase amount for the test group was 582.11.

2- Next, we checked the assumptions before conducting the hypothesis test. The first assumption, the "normal 
distribution assumption," was tested using the Shapiro-Wilk test. The p-value for both groups was greater than 0.05, 
indicating that the data followed a normal distribution.

3- The second assumption, the "homogeneity of variances assumption," was tested using the Levene test. The p-value for 
this test was also greater than 0.05, indicating that the variances were homogeneous.

4- Since the assumptions were met, we used an independent two-sample t-test (parametric test). The null hypothesis (H0) 
stated that there was no significant difference in the average purchases between the control and test groups, while 
the alternative hypothesis (H1) stated that there was a significant difference.

5- The t-test resulted in a p-value of 0.3493. With a p-value greater than 0.05, we conclude that there is no 
significant difference in average purchases between the control and test groups.

In conclusion, based on the data at hand, transitioning to the test group did not have a significant impact on purchase 
amounts compared to the control group.
"""