# Comparing Conversion of Bidding Methods with AB Testing

## Project Overview
This project involves comparing the effectiveness of two bidding methods, "maximum bidding" and "average bidding," through an A/B test. The goal is to determine whether the "average bidding" method yields more conversions than the existing "maximum bidding" method. The A/B test has been ongoing for one month, and the results need to be analyzed to provide insights to bombabomba.com.

## Dataset
The dataset contains information about a company's website, including the number of ad views, ad clicks, purchases, and earnings generated from these purchases. There are two separate datasets: the control group with "Maximum Bidding" and the test group with "Average Bidding."
The dataset used for this project contains information about user interactions with online ads and their resulting earnings. There are two separate datasets for the control and test groups, each stored in separate sheets of an Excel file named "ab_testing.xlsx." The control group was exposed to "Maximum Bidding," while the test group experienced "Average Bidding."

- `Impression`: Number of ad impressions
- `Click`: Number of clicks on the displayed ads
- `Purchase`: Number of products purchased after clicking on the ads
- `Earning`: Earnings generated from the purchased products

## Tasks

### Data Preparation and Analysis
1. Load the dataset containing control and test group data from "ab_testing.xlsx" and assign them to separate variables.
2. Analyze the control and test group data.

### Defining the Hypothesis for A/B Testing
1. Define the null and alternative hypotheses for the A/B test.
2. Analyze the purchase (earnings) means for the control and test groups.

### Performing the Hypothesis Test
1. Conduct assumption checks before the hypothesis test, including normality assumption and homogeneity of variances.
2. Select the appropriate test based on the assumption results and perform an independent two-sample t-test.
3. Interpret the test results and determine if there is a statistically significant difference in purchase means between the control and test groups.

### Analysis of Results
1. Discuss the test used and explain the reasons behind the choice.
2. Provide recommendations to the client based on the test results.

## How to Use
1. Clone this repository to your local machine.
2. Ensure you have Python and the required libraries (pandas, numpy, matplotlib, scipy) installed.
3. Run the provided Jupyter Notebook or Python script to execute the analysis and get insights.
