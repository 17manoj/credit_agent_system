import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import OneHotEncoder

# Remove duplicate rows
df = df.drop_duplicates()

# Fill missing values
for column in df.columns:
    if df[column].dtype == np.number:
        df[column].fillna(df[column].mean(), inplace=True)
    else:
        df[column].fillna(df[column].mode()[0], inplace=True)

# Standardize column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Drop columns with more than 80% missing values
missing_values = df.isnull().sum() / len(df)
df = df.drop(columns=missing_values[missing_values > 0.8].index)

# Convert date columns to datetime format
for column in df.columns:
    if 'date' in column:
        df[column] = pd.to_datetime(df[column])

# Replace outliers in numerical columns using the IQR method
for column in df.select_dtypes(include=[np.number]).columns:
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    df[column] = np.where((df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR)), df[column].median(), df[column])

# Convert categorical variables into numerical format using onehot encoding
encoder = OneHotEncoder(drop='first')
categorical_columns = df.select_dtypes(include=['object']).columns
df_encoded = pd.DataFrame(encoder.fit_transform(df[categorical_columns]).toarray(), columns=encoder.get_feature_names(categorical_columns))
df = pd.concat([df.drop(categorical_columns, axis=1), df_encoded], axis=1)