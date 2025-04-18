import pandas as pd
import glob

def create_dataframe():
    # Build file paths for all csv files
    file_paths = glob.glob('data/*.csv')

    dfs = []
    # Combine all csv files in a single data frame
    for file_path in file_paths:
        df = pd.read_csv(file_path)

        file_name = file_path.split('/')[-1].split('.')[0]
        city_name = file_name.split('_')[0]
        day_type = file_name.split('_')[1]

        # Add city and day_type (weekday or weekend) as new columns
        df['city'] = city_name
        df['day_type'] = day_type

        dfs.append(df)

    # Concatenate data frames from all csv files
    df = pd.concat(dfs, ignore_index=True)
    return df

def clean_dataframe(df):
    # Remove first column with row index and drop all rows with missing values
    df = df.iloc[:, 1:].dropna()
    # removing outliners with realSum > 1000
    # this operation set our MEAN from 123 to 79
    df = df[df['realSum'] <= 300]
    return df

def encode_variables(df):
    # Use one-hot encoding for room_type, city and day type because they are categorical data
    df = pd.get_dummies(df, columns=["room_type"], drop_first=False, dtype=int)
    df = pd.get_dummies(df, columns=["city"], drop_first=False, dtype=int)
    df = pd.get_dummies(df, columns=["day_type"], drop_first=False, dtype=int)
    # Convert columns with true or false values to 1 or 0
    binary_cols = ["room_shared", "room_private", "host_is_superhost"]
    df[binary_cols] = df[binary_cols].astype(int)
    # Rounding decimals to 3 for realSum, 3 numbers after comma 
    df['realSum'] = df['realSum'].round(decimals=3)
    return df

def split_input_target(df):
    # Split data into input (x) and target (y)
    x = df.drop('realSum', axis=1)
    y = df['realSum']
    return x, y

def process_data():
    df = create_dataframe()
    df = clean_dataframe(df)
    df = encode_variables(df)
    print(df.info())
    print(df.describe())
    return df