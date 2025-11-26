import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')

# Clean data
df = df[((df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975)))]
df.index = pd.to_datetime(df.index)

def draw_line_plot():
    # Draw line plot
    print(df)
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(df.index, df['value'], color='tab:red', linewidth=1.25)
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xticks(pd.date_range(start='2016-07-01', end='2020-01-01', freq='6MS'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    print(type(fig))

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')
    months = ['January', 'February', 'March',
              'April', 'May','June',
              'July', 'August', 'September',
              'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=months, ordered=True)
    df_grouped_months = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()
    df_pivot = df_grouped_months.pivot(index='year', columns='month', values='value')

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(7, 7))
    df_pivot.plot(kind='bar', ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(loc='upper left', title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # added for appropriate order
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box.month, categories=months, ordered=True)

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2,figsize=(16, 6))
    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0], palette='tab10')
    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1], palette='pastel')

    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[1].set_title('Month-wise Box Plot (Seasonality)')

    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
