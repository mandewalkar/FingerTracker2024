"""
This code takes in monitor data and converts it to a CSV file compatible for Braille_Finger_tracter.py.
"""

import os
import pandas as pd
import numpy as np

def main(filename):
    # Read in the tab-separated text file
    current_directory = os.getcwd()
    portion_to_remove = 'CVSystem/'
    relative_path = os.path.relpath(current_directory, portion_to_remove)
    touch_path = os.path.join(relative_path, 'TouchscreenSystem', 'outputs', filename)

    df = pd.read_csv(touch_path, sep='\t')
    df = df.rename(columns={'   0.0': 'time', '{}': 'coordinate'})
    df = df[df['coordinate'] != '{}']

    # Evaluate the coordinate strings
    df['coordinate'] = df['coordinate'].apply(lambda x: eval(x))

    # Define a function to split the coordinate values in the 'coordinate' column
    def split_coordinate_value(coord_dict):
        coord_cols = {}
        for key, value in coord_dict.items():
            coord_cols[f'{key}_X'] = value[0]
            coord_cols[f'{key}_Y'] = value[1]
        return pd.Series(coord_cols)

    # Apply the function to the 'coordinate' column to create new columns for each key
    df = df.join(df['coordinate'].apply(split_coordinate_value))
    df.drop(columns=['coordinate'], inplace=True)
    df = df.rename(columns={df.columns[0]: 'Time'})
    df.head()
    # Write the DataFrame to a comma-separated CSV file
    current_directory = os.getcwd()
    destination_path = os.path.join(current_directory, 'output_logs', 'test_acc.csv')
    df.to_csv(destination_path, index=False)

if __name__ == '__main__':
    main()