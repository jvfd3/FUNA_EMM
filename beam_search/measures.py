import numpy as np
import pandas as pd

def calculate_mean(df=None, column=None):

    qm_mean = df[column].mean()

    return np.round(qm_mean, 4)

def calculate_mean_se(df=None, column=None):

    qm_se = df[column].std() / np.sqrt(df.shape[0])

    return np.round(qm_se, 4)
