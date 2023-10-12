import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import optuna
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score)
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import pickle

np.random.seed(42)

df = pd.read_csv("data.csv")
df.columns = df.columns.map(str.strip)

vars_high_correlation = ['ROA(A) before interest and % after tax',
                        'ROA(B) before interest and depreciation after tax',
                        'Net Value Per Share (A)', 'Net Value Per Share (C)']

vars_low_variance = ['Net Income Flag',
                    'Working capitcal Turnover Rate',
                    'Cash Flow to Sales',
                    'Total Asset Return Growth Rate Ratio',
                    'Continuous Net Profit Growth Rate',
                    'Inventory/Working Capital',
                    'Operating Profit Growth Rate',
                    'Non-industry income and expenditure/revenue',
                    'Interest Expense Ratio',
                    'Working Capital/Equity',
                    'Realized Sales Gross Profit Growth Rate',
                    'Total income/Total expense',
                    'Contingent liabilities/Net worth',
                    'No-credit Interval',
                    'Continuous interest rate (after tax)',
                    'Pre-tax net Interest Rate',
                    'Cash Flow to Equity',
                    'Operating Profit Rate',
                    'Interest Coverage Ratio (Interest expense to EBIT)',
                    'Inventory and accounts receivable/Net value',
                    'Current Liabilities/Equity',
                    'Current Liability to Equity',
                    'After-tax net Interest Rate',
                    'After-tax Net Profit Growth Rate',
                    'Regular Net Profit Growth Rate']

df = df[df.columns.drop(vars_high_correlation + vars_low_variance)]

# Здесь используем random_state
X_train, X_test, y_train, y_test = train_test_split(df.drop('Bankrupt?', axis = 1), df["Bankrupt?"], test_size=0.3, random_state=42)

# Scaling
scaler = MinMaxScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# SMOTE
sm = SMOTE(random_state=42)
X_train, y_train = sm.fit_resample(X_train, y_train)

#PCA
pca = PCA(n_components=31)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)
with open('pca.pkl', 'wb') as f:
    pickle.dump(pca, f)

# Logreg training
logreg = LogisticRegression(solver='liblinear')
logreg.fit(X_train,y_train)
with open('logreg.pkl', 'wb') as file:
    pickle.dump(logreg, file)

# f1 = f1_score(y_test, y_pred, average='macro')
# recall= recall_score(y_test, y_pred, average='macro')

# print("F1 Score on test data:", f1)
# print("Recall core on test data:", recall)
