# Import essential libraries
import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd
import env

#acquire---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Acquire 
def cohort_data():
    '''
    This function reads the curriculum data from the mySQL database into a df.
    '''
    #url to connect to codeup servers
    url = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/curriculum_logs'
    # Create SQL query.
    sql_query = '''
    SELECT 
        date,
        time,
        ip,
        path,
        user_id,
        cohort_id,
        name as cohort_name,
        slack,
        start_date,
        end_date,
        program_id
    FROM
        curriculum_logs.logs
    join
        curriculum_logs.cohorts on cohort_id = id
    ;
    '''
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, url)
    
    return df

#prepare---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_lesson(string):
    arr = string.split('/')
    if len(arr) > 1:
        return arr[1]
    else:
        return None

def get_module(string):
    arr = string.split('/')
    return arr[0]



#preparing data 
def prep_data(df):
    '''
    This function takes in a messy dataframe and return the cleaned verison of dataframe.
    Detial steps are in code comment below.
    
    '''
    df = df[df.path.notna()]
    # Change date columns to datetime
    df.date = pd.to_datetime(df.date)
    df.start_date = pd.to_datetime(df.start_date)
    df.end_date = pd.to_datetime(df.end_date)
    # Set date columns as datatime as index
    df = df.set_index(df.date)
    
    # Drop null values
    df = df.dropna()

    # Encode program_id
    df['program'] = df.program_id.map({1: 'Full Stack ', 2: 'Full Stack Java', 3: 'Data Science', 4: 'Front'})
    df['module'] = df.path.apply(get_module)
    df['lesson'] = df.path.apply(get_lesson)
    df = df.replace({'':None})
    
    # Drop columns not import to me

    return df



#explore---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



def question1(df):
    '''
    This function plots the top accessed pages for full stack php, web dep program
    '''
    p1 = pd.DataFrame(df.loc[df.program_id==1].path.value_counts().nlargest(10))
    plt.figure(figsize = (12,6))
    sns.barplot(x=p1.index, y=p1.path)
    plt.title('Top 10 Accessed Pages for Web Development')

def question1_2(df):
    '''
    This function plots the top accessed pages for full stack java, web dep program
    '''
    p2 = pd.DataFrame(df.loc[df.program_id==2].path.value_counts().nlargest(10))
    plt.figure(figsize = (12,6))
    sns.barplot(x=p2.index, y=p2.path)
    plt.title('Top 10 Accessed Pages for Web Development (Java)')

def question1_3(df):
    '''
    This function plots the top accessed pages for data science program
    '''
    p3 = pd.DataFrame(df.loc[df.program_id==3].path.value_counts().nlargest(5))
    plt.figure(figsize = (20,6))
    sns.barplot(x=p3.index, y=p3.path)
    plt.title('Top 5 Accessed Pages for Data Science')

def question1_4(df):
    '''
    This function plots the top accessed pages for data science program
    '''
    p4 = pd.DataFrame(df.loc[df.program_id==4].path.value_counts().nlargest(10))
    plt.figure(figsize = (16,6))
    sns.barplot(x=p4.index, y=p4.path)
    plt.title('Top 4 Accessed Pages for Front End ')

def question1_web(df):
    '''
    This function takes in a dataframe and returns the top accessed lessons for web dep program
    '''
    # Remove staff from the analysis.
    df.loc[~(df.cohort_name == 'Staff')]

    # Step 1.
    # Web Devlopment Cohorts
    wd_cohorts = df.loc[df.program_id.isin([1, 2, 4])]

    # Data Science Cohorts
    ds_cohorts = df.loc[df.program_id == 3]
    # Step 2.
    # Create a variable to store pages to filter out.
    remove_pages = [ 'index.html', 'search/search_index.json', 'mkdocs/search_index.json','/', 'toc', 'appendix',]

    # Clean page_viewed to remove logistic pages: Searches, Table of Contents, Appendix
    wd_cohorts = wd_cohorts.loc[~wd_cohorts.path.isin(remove_pages)]

    # Replace content main page with empty string.
    wd_cohorts.page_viewed = wd_cohorts.path.replace('content/', '', regex=True)
    # Step 3 `.value_counts()`
    wd_top_10_pages = wd_cohorts.path.value_counts().nlargest(10)
    print(wd_top_10_pages)

def question1_science(df):
    '''
    This function takes in a dataframe and returns the top accessed lessons for data science program
    '''
    # Step 1.
    # Data Science Cohorts
    ds_cohorts = df.loc[df.program_id == 3]
    # Create a variable to store pages to filter out.
    remove_pages = ['/', 'toc', 'appendix', 'index.html', 'search/search_index.json', 'mkdocs/search_index.json']

    # Clean page_viewed to remove logistic pages: Searches, Table of Contents, Appendix
    ds_cohorts = ds_cohorts.loc[~ds_cohorts.path.isin(remove_pages)]

    # Replace content main page with empty string.
    ds_cohorts.path = ds_cohorts.path.replace('content/', '', regex=True)

    # Step 2 `.value_counts()`
    ds_top_10_pages = ds_cohorts.path.value_counts().nlargest(10)
    print(ds_top_10_pages)
    
    
#question2------------------------------------------------------------------------------------------------------------------------
def question2_1(df):
    # Filter the dataset down to only current students
    current_student = (df.index > df.start_date) & (df.index < df.end_date)
    current = df[current_student]

    # Filter further to only include java modules since they were the easiest to pick out
    current.dropna(subset='module')
    mods = current.module.unique().tolist()
    mods.remove(None)
    mods = [col for col in mods if 'java-' in col]
    current = current[current.module.isin(mods)]

    # Another filter to reduce noise
    current= current[current.program !='Data Science']
    current = current[current.module != 'java-1']
    # Show popularity of java modules per cohort
    a = current.groupby('cohort_name').module.value_counts().rename('vcount')
    a = a.reset_index() # Prepare for plotting
    plt.figure(figsize=(15,10))
    sns.catplot(kind= 'bar', data=a.sort_values(by='vcount'), x='module', y='vcount', hue='cohort_name', height=7, aspect=2)
    
def Question2_3(df):
        # Filter the dataset down to only current students
    current_student = (df.index > df.start_date) & (df.index < df.end_date)
    current = df[current_student]

    # Filter further to only include java modules since they were the easiest to pick out
    current.dropna(subset='module')
    mods = current.module.unique().tolist()
    mods.remove(None)
    mods = [col for col in mods if 'java-' in col]
    current = current[current.module.isin(mods)]

    # Another filter to reduce noise
    current= current[current.program !='Data Science']
    current = current[current.module != 'java-1']
    # Show popularity of java modules per cohort
    a = current.groupby('cohort_name').module.value_counts().rename('vcount')
    a = a.reset_index() # Prepare for plotting
    sns.catplot(kind= 'bar', data=a[a.module=='java-ii'].sort_values(by='vcount'), y='cohort_name', x='vcount', height=4, aspect=1.5).set(title='Java-ii')


def question2():
    '''
    This function plots the full stack php program jquery view comparison
    '''
    # bar chart comparing jquery 
    x = ['1', '11', '7', '13', '19']
    y = [133, 4, 3, 2, 1]

    fig = plt.figure(figsize = (12,6))
    sns.barplot(x, y)
    
    plt.xlabel("Cohorts")
    plt.ylabel("No. of Views")
    plt.title("Cohorts View Comparison")
    plt.show()

def question2_2():
    '''
    This function plots the full stack php program jquery & java-i/methods view comparison
    '''
    # bar chart comparing cohort 17 and others 
    x = ['17-jquery', '17-methods', '13-jquery', '13-methods', '19-jquery', '19-methods', '7-jquery', '12-methods']
    y = [71, 69, 2, 3, 1, 3, 3, 1]

    fig = plt.figure(figsize = (15, 8))
    sns.barplot(x, y, palette='mako')
    
    plt.xlabel("Cohorts")
    plt.ylabel("No. of Views")
    plt.title("Cohort Jquery & Java-i/methods View Comparison")
    plt.show()
    
#question3------------------------------------------------------------------------------------------------------------------------

def Question3():
    '''
    This function return the users who have hardly accessed the curriculum during their active time
    '''
    result_df = pd.DataFrame([[940, 138, 'Neptune', 'Full Stack Java'], [918, 138, 'Neptune', 'Full Stack Java'],
                         [879, 135, 'Macro', 'Full Stack Java'], [619, 57, 'Ganymede', 'Full Stack Java']], columns = ['User_id', 'Cohort_id', 'Cohort_name', 'Program'])
    return result_df

#question4------------------------------------------------------------------------------------------------------------------------


def question4(df):
    '''
    This function takes in a dataframe and plot the distribution of amount of IP addresses belong to users
    '''
    # Creating a dataframe with unique user id and each id's IP address amount
    ip = pd.DataFrame(df.groupby('user_id').ip.nunique(), columns = ['ip'])
    # Visualize distribution
    kwargs = dict(hist_kws={'alpha':.6}, kde_kws={'linewidth':2})
    plt.figure(figsize=(16,8), dpi= 80)
    plt.title('IP Address Amount per User Distribution')
    sns.distplot(x=ip['ip'], **kwargs, color = '#004987')

def Question4_abnormal_users(df):
    '''
    This function plot the top 6 users with abnormal 
    '''
    # Top 6 abnormal users
    plt.figure(figsize = (20,20))
    plt.subplot(321)
    pages_228 = df[df.user_id == 228]['path'].resample('d').count()
    pages_228.plot()
    plt.title('User 228 Activity', fontsize = 20)

    plt.subplot(322)
    pages_843 = df[df.user_id == 843]['path'].resample('d').count()
    pages_843.plot()
    plt.title('User 843 Activity', fontsize = 20)

    plt.subplot(323)
    pages_690 = df[df.user_id == 690]['path'].resample('d').count()
    pages_690.plot()
    plt.title('User 690 Activity', fontsize = 20)

    plt.subplot(324)
    pages_533 = df[df.user_id == 533]['path'].resample('d').count()
    pages_533.plot()
    plt.title('User 533 Activity', fontsize = 20)

    plt.subplot(325)
    pages_226 = df[df.user_id == 226]['path'].resample('d').count()
    pages_226.plot()
    plt.title('User 226 Activity', fontsize = 20)

    plt.subplot(326)
    pages_460 = df[df.user_id == 460]['path'].resample('d').count()
    pages_460.plot()
    plt.title('User 460 Activity', fontsize = 20)
    plt.tight_layout()

    
#question5------------------------------------------------------------------------------------------------------------------------    
    
def Question5(df):
    '''
    This function takes in a dataframe and return 2 dataframes based on the program
    '''
    # create data science data frame
    ds = df[df.program_id == 3]
    # create program 1 web dev dataframe
    wd1 = df[df.program_id == 1]
    # create program 2 webdev data frame
    wd2 = df[df.program_id == 2]
    # concatenate both web dev data frames into one df
    wd = pd.concat([wd1, wd2])

    # return most popular web dev paths viewed
    return ds, wd

              
def Question5_science(ds):
    '''
    This function plots the data science access activity to web dep curriculum
    '''
    ds_pages = ds[(ds['path'] == 'java-i') | (ds['path'] == 'java-ii') | (ds['path'] == 'java-ii') | (ds['path'] == 'java-iii') | (ds['path'] == 'jquery')]['path'].resample('d').count()
    plt.figure(figsize = (12,6))
    ds_pages.plot(title='Data Science Student Access to Web Devlopment Curriculum', color = '#003B85')

def Question5_web(wd):
    '''
    This function plots the web devlopemnt student access activity to data science curriculum
    '''
    wd_pages = wd[(wd['path'] == 'classification/overview') | (wd['path'] == 'fundamentals/intro-to-data-science') | (wd['path'] == 'stats/compare-means')]['path'].resample('d').count()
    plt.figure(figsize = (12,6))
    wd_pages.plot(title='Web Development Student Access to Data Science Curriculum', color = '#f09c1a')
    

#question6------------------------------------------------------------------------------------------------------------------------

    
def Question6(df):
    grads = pd.DataFrame(df[df.date>df.end_date].program.value_counts())
    plt.figure(figsize=(16,8))
    sns.barplot(x=grads.index, y=grads.program)
    plt.title('Post Graduation Number of Logs per Program', fontsize = 20)
    plt.xlabel('Program', fontsize = 15)
    plt.ylabel('No. of Log Entry', fontsize = 15)
    
def Question6_2(df):
    '''
    This function visualize the most frequently visited topics for full stack java 
    '''
    p1 = pd.DataFrame(df[(df.date>df.end_date)&(df.program_id == 1)].path.value_counts().head(10))
    # Visualizing full stack java most frequent lesson
    plt.figure(figsize=(16,8))
    sns.barplot(x=p1.index, y=p1.path)
    plt.title('Most Frequently Visited Topics Post Graduation - Full Stack Java Program', fontsize = 20)
    plt.xlabel('Topics', fontsize = 15)
    plt.ylabel('No. of Log Entry', fontsize = 15)

def Question6_4(df):
    '''
    This function visualize the most frequently visited topics for data science program
    '''
    p3 = pd.DataFrame([ ['Anomaly Detection', 384],['MySQL', 275], ['Classification', 266], ['Feature Scaling', 219],
                  ['AL-ML-DL-timeline', 189], ['Modern_Data_Scientist.jpg', 187], ['Intro to Data Science', 184], ['SQL Database Design', 84]], columns = ['Lesson', 'Count'])
    
    # Visualizing full stack php most frequent lesson
    plt.figure(figsize=(20,8))
    sns.barplot(x=p3['Lesson'], y=p3['Count'])
    plt.title('Most Frequently Visited Topics Post Graduation - Data Science Program', fontsize = 20)
    plt.xlabel('Topics', fontsize = 15)
    plt.ylabel('No. of Log Entry', fontsize = 15)

    
#question7------------------------------------------------------------------------------------------------------------------------    
    
    
def Question7(df):
    '''
    This function visualize the topics that got accessed the least for web dep 
    '''
    wb_plot = pd.DataFrame([['JavaScript Working with Variables', 1], ['Java-i', 1], ['HTML', 1], ['HTML-CSS Introduction', 1], ['Environment Setup', 1], ['Coding Challenges', 1]], columns = ['Lesson', 'Count'])

    plt.figure(figsize=(16,8))
    sns.barplot(x=wb_plot['Lesson'], y=wb_plot['Count'])
    plt.title('Topics Accessed the Least - Web Development Programs', fontsize = 20)
    plt.xlabel('Topics', fontsize = 15)
    plt.ylabel('No. of Log Entry', fontsize = 15)

def Question7_2(df):
    '''
    This function visualize the topics that got accessed the least for data science students
    '''
    ds_plot = pd.DataFrame([['Introduction to Python', 1], ['Creating Charts',1], ['Case Statements', 1], ['ML Methodologies Drawing', 1], ['Tidy Data', 1], ['git/cli', 1], ['mySQL-Introduction', 1]], columns = ['Lesson', 'Count'])
    plt.figure(figsize=(16,8))
    sns.barplot(x=ds_plot['Lesson'], y=ds_plot['Count'])
    plt.title('Topics Accessed the Least - Data Science', fontsize = 20)
    plt.xlabel('Topics', fontsize = 15)