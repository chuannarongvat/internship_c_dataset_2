import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def missing_value(df):
    missing_values = df.isna().sum()
    
    if missing_values.sum() == 0:
        print('There are no missing values in the DataFrame.')
    else:
        missing_percentage = (df.isna().mean() * 100).round(2)

        missing_data = pd.DataFrame({
            'Column': missing_values.index,
            'Missing Values': missing_values.values,
            'Missing Percentage': missing_percentage.values
        })

        missing_data = missing_data[missing_data['Missing Values'] > 0]
        missing_data = missing_data.sort_values(by='Missing Percentage', ascending=False)

        print('Columns with missing values:')
        print(missing_data)


def duplicate_value(df):
    duplicate_rows = df[df.duplicated(keep=False)]
    
    if duplicate_rows.empty:
        print('There are no duplicated rows in the DataFrame.')
    else:
        duplicated_percentage = (len(duplicate_rows) / len(df)) * 100
        
        duplicated_data = pd.DataFrame({
            'Column': duplicate_rows.columns,
            'Duplicated Rows': duplicate_rows.apply(lambda x: x.duplicated().sum()),
            'Duplicated Percentage': duplicated_percentage
        })
        
        duplicated_data = duplicated_data[duplicated_data['Duplicated Rows'] > 0]
        duplicated_data = duplicated_data.sort_values(by='Duplicated Percentage', ascending=False)
        
        print('Columns with duplicated rows:')
        print(duplicated_data)

        
def cat_num_split(df):
    cat_cols = [feature for feature in df.columns if df[feature].dtypes=='O']
    num_cols = [feature for feature in df.columns if df[feature].dtypes!='O']
    return cat_cols, num_cols


def count_nuniques(df, cat_cols):
    for col in cat_cols:
        n_unique = df[col].nunique()
        print(f'Columns {col}: {n_unique} unique values')

def plot_cat_cols(df, cat_cols, target_col):
    palette = 'ch:.25'
    
    ax = sns.countplot(x=cat_cols, data=df, hue=target_col, palette=palette)
    
    total = len(df)
    for p in ax.patches:
        percentage = '{:.1f}%'.format(100 * p.get_height() / total)
        x = p.get_x() + p.get_width() / 2
        y = p.get_height()
        ax.annotate(percentage, (x, y), ha='center')
    
    plt.xticks(rotation=90)
    plt.title(cat_cols)
    plt.show()
    

    