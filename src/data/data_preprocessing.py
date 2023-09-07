import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataPreprocessing:
    def __init__(self, df, palette='ch:.25'):
        self.df = df
        self.palette = palette

    def missing_values(self):
        missing_values = self.df.isna().sum()
    
        if missing_values.sum() == 0:
            print('There are no missing values in the DataFrame.')
        else:
            missing_percentage = (self.df.isna().mean() * 100).round(2)

            missing_data = pd.DataFrame({
                'Column': missing_values.index,
                'Missing Values': missing_values.values,
                'Missing Percentage': missing_percentage.values
            })

            missing_data = missing_data[missing_data['Missing Values'] > 0]
            missing_data = missing_data.sort_values(by='Missing Percentage', ascending=False)

            print('Columns with missing values:')
            print(missing_data)

    def duplicate_values(self):
        duplicate_rows = self.df[self.df.duplicated(keep=False)]
    
        if duplicate_rows.empty:
            print('There are no duplicated rows in the DataFrame.')
        else:
            duplicated_percentage = (len(duplicate_rows) / len(self.df)) * 100
        
            duplicated_data = pd.DataFrame({
                'Column': duplicate_rows.columns,
                'Duplicated Rows': duplicate_rows.apply(lambda x: x.duplicated().sum()),
                'Duplicated Percentage': duplicated_percentage
                })
        
            duplicated_data = duplicated_data[duplicated_data['Duplicated Rows'] > 0]
            duplicated_data = duplicated_data.sort_values(by='Duplicated Percentage', ascending=False)
        
            print('Columns with duplicated rows:')
            print(duplicated_data)

    @staticmethod
    def cat_num_split(df):
        cat_cols = [feature for feature in df.columns if df[feature].dtypes=='O']
        num_cols = [feature for feature in df.columns if df[feature].dtypes!='O']
        return cat_cols, num_cols

    def count_uniques(self, cat_cols):
        for col in cat_cols:
            n_unique = self.df[col].nunique()
            print(f'Column {col}: {n_unique} unique values')

    def plot_cat_cols(self, cat_col, target_col):
        palette = self.palette
    
        ax = sns.countplot(x=cat_col, data=self.df, hue=target_col, palette=palette)
    
        total = len(self.df)
        for p in ax.patches:
            percentage = '{:.1f}%'.format(100 * p.get_height() / total)
            x = p.get_x() + p.get_width() / 2
            y = p.get_height()
            ax.annotate(percentage, (x, y), ha='center')
    
        plt.xticks(rotation=90)
        plt.title(cat_col)
        plt.show()

    def plot_num_cols(self, num_col, target_col):
        palette = self.palette
        num_bins = int(np.sqrt(len(self.df[num_col])))
        
        sns.histplot(data=self.df, x=num_col, kde=True, hue=target_col, palette=palette, bins=num_bins)
        
        mean = self.df[num_col].mean()
        median = self.df[num_col].median()
        
        plt.axvline(mean, color='r', linestyle='dashed', linewidth=2, label=f'Mean: {mean:.2f}')
        plt.axvline(median, color='g', linestyle='dashed', linewidth=2, label=f'Median: {median:.2f}')                   
        plt.legend()
        plt.title(num_col)
        plt.show()
        
    def plot_target_col(self, target_col):
        ax = sns.countplot(data=self.df, x=target_col, palette=self.palette)

        total = len(self.df)
        for p in ax.patches:
            percentage = '{:.1f}%'.format(100 * p.get_height() / total)
            x = p.get_x() + p.get_width() / 2
            y = p.get_height()
            ax.annotate(percentage, (x, y), ha='center')

        plt.title('Churn Distribution')
        plt.show()
        
    def plot_contract_type(self, col):
        contract_type = ['Month-to-month', 'Two year', 'One year']
        
        fig, axes = plt.subplots(ncols=3, figsize=(12, 6))

        for i, c in enumerate(contract_type):
            contract_df = self.df[self.df['Contract'] == c]
    
            sns.histplot(data=contract_df, x=col, kde=True, ax=axes[i], hue='Churn', palette='ch:.25', bins=50)
            axes[i].set_title(c)
    
        plt.show()
        
    def scatter_plot(self, x,y, target_col):
        sns.scatterplot(data=self.df, x=x, y=y, hue=target_col, palette=self.palette)
        
        plt.title(f"{x} vs {y}")
        plt.show()
        
    def line_plot(self, x,y, target_col):
        sns.lineplot(data=self.df, x=x, y=y, hue=target_col, palette=self.palette)
        
        plt.title(f"{x} vs {y}")
        plt.show()
        