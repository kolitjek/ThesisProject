
import pandas as pd
import csv
import numpy as np
import os, os.path
import seaborn as sns


import matplotlib.pyplot as plt

from scipy import stats
from math import sqrt
from numpy import mean
from scipy.stats import t
from scipy.stats import sem
from scipy.stats import levene


def calc_standard_deviation(sample):
	print("Standard Deviation: " + str(stats.tstd(sample)))

# function for calculating the t-test for two independent samples
def independent_ttest(data1, data2, alpha):
    # calculate means
    mean1, mean2 = mean(data1), mean(data2)

    print(("mean1:{0} T-mean1:{1}".format(mean1, mean2)))
    # calculate standard errors
    se1, se2 = sem(data1), sem(data2)
    # standard error on the difference between the samples
    sed = sqrt(se1 ** 2.0 + se2 ** 2.0)
    # calculate the t statistic
    t_stat = (mean1 - mean2) / sed
    #print(t)
    #print(t_stat)
    # degrees of freedom
    df = len(data1) + len(data2) - 2
    #print("DF")
    #print(df)

    # calculate the critical value
    cv = t.ppf(1.0 - alpha, df)

    #print("critical value")
    #print(cv)

    # calculate the p-value
    p = (1.0 - t.cdf(abs(t_stat), df)) * 2.0

    print("effect size:")
    print( sqrt (((t_stat**2)/(t_stat**2 +df))))
    # return everything
    return t_stat, df, cv, p


def normalDistributionTest(data):
    k2, p = stats.normaltest(data)
    alpha = 0.05
    print("normal Distribution ")
    #print("p = {:g}".format(p))

    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("The null hypothesis can be rejected, x does not come from the same distribution")
    else:
        print("The null hypothesis cannot be rejected, x comes from the same distribution")

if __name__ == "__main__":

    path =  os.path.abspath(__file__).rsplit("\\", 1)[0] + "\\" + "testRecords\\" + "TestScore\\" + "pure_ttest_data.csv"
    df = pd.read_csv(path, delimiter=";", decimal=".")
    list = df.values.tolist()

    conv2dCNNLSTM = list[0]
    conv1dArgDataLSTMCNN = list[1]
    conv1dCNN = list[2]
    conv1dArgDataCNNLSTM = list[3]
    conv2dArgDataCNN = list[4]
    lstm = list[5]
    lstmconv2d = list[6]

    singleModelTest = False
    modelToBeTested = conv2dArgDataCNN

    if(singleModelTest):
        print("***********************************************")
        print("Model to be evaluated: conv2dArgDataCNN")
        print("")
        normalDistributionTest(modelToBeTested)
        print("")
        print("Mean: ")
        print(mean(modelToBeTested))
        print("")
        print("Standard Deviation")
        print(np.std(modelToBeTested))
        print("***********************************************")


    t_test = True
    model1 = conv2dCNNLSTM
    model2 = conv1dArgDataLSTMCNN

    if(t_test):
        print("***********************************************")
        print("models to be evaluated: conv1dArgDataLSTMCNN & conv2dCNNLSTM")
        print("")
        stat, p3 = levene(model1, model2)
        print("p-value levene test: %d" % p3)
        print(p3)
        print("")

        # calculate the t test
        alpha = 0.05
        t_stat, df, cv, p = independent_ttest(model1, model2, alpha)
        #print(t_stat)
        ('t=%.3f, df=%d, cv=%.3f, p=%.3f' % (t_stat, df, cv, p))
         #interpret via critical value
        #if abs(t_stat) <= cv:
         #   print('Accept null hypothesis that the means are equal.')
        #else:
          #  print('Reject the null hypothesis that the means are equal.')
        print("")
        print("H_0: the mean result of model_1 is less or equal to the mean of model_2")
        tStat, pValue = stats.ttest_ind(model1, model2, equal_var=False)  #equal_var=False = welch's t-test https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
        print("P-Value:{0} T-Statistic:{1}".format(pValue, tStat))  # print the P-Value and the T-Statistic
        # interpret via p-value
        if pValue > alpha:
            print('Accept null hypothesis that the means are equal.')
        else:
            print('Reject the null hypothesis that the means are equal.')
        print("***********************************************")

    sns.kdeplot(conv2dCNNLSTM, shade=True)
    sns.kdeplot(conv1dArgDataLSTMCNN, shade=True)
    sns.kdeplot(conv1dCNN, shade=True)
    sns.kdeplot(conv2dArgDataCNN, shade=True)
    sns.kdeplot(lstm, shade=True)
    #sns.kdeplot(lstmconv2d, shade=True)
    sns.kdeplot(xlabel='common xlabel', ylabel='common ylabel')
    plt.xlabel('Prediction accuracy', fontsize=18)
    plt.ylabel('Frequency', fontsize=16)
    plt.legend(("CNN2d_LSTM","LSTM_CNN1d", "CNN1d", "CNN2d", "LSTM", "LSTM_CNN2d"), prop={'size': 16},loc='upper right')

    #tStat, pValue = stats.ttest_ind(conv2dCNNLSTM, conv1dArgDataLSTMCNN, equal_var=True)  # run independent sample T-Test
    #print("P-Value:{0} T-Statistic:{1}".format(pValue, tStat))  # print the P-Value and the T-Statistic

    #print("Paired test")
    #x,y = stats.ttest_rel(conv2dCNNLSTM, conv1dArgDataLSTMCNN)
    #print(("P-Value:{0} T-Statistic:{1}".format(x, y)))

    plt.show()
