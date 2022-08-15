import numpy as np
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import dash
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
# import dash_core_components as dcc
# import dash_html_components as html
from dash.dependencies import Input, Output

%%capture
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

df2 = gss_clean.groupby('sex').agg({'income':'mean', 'job_prestige':'mean', 'socioeconomic_index':'mean', 'education':'mean'})
df2 = df2.reset_index()

# Round col vals
df2['income'] = round(df2['income'], 2)
df2['job_prestige'] = round(df2['job_prestige'], 2)
df2['socioeconomic_index'] = round(df2['socioeconomic_index'], 2)
df2['education'] = round(df2['education'], 2)

# Rename col headings
df2['sex'] = df2['sex'].replace({'female':'Female', 'male':'Male'})
df2 = df2.rename({'sex':'',
                  'income':'Avg. Annual Income', 
                  'job_prestige': 'Avg. Job Prestige Score', 
                  'socioeconomic_index':'Avg. Socioeconomic Index',
                  'education':'Avg. Years of Formal Education'}, axis=1)
table = ff.create_table(df2)

bar3 = pd.DataFrame(gss_clean.groupby(['male_breadwinner', 'sex']).size()).reset_index()
bar3 = bar3.rename({0:'Frequency', 'male_breadwinner':'Response', 'sex':'Gender'}, axis=1)

bar3['Response'] = bar3['Response'].astype('category')
bar3['Response'] = bar3['Response'].cat.reorder_categories(['strongly disagree', 'disagree', 'agree', 'strongly agree'])

fig3 = px.bar(bar3, x='Response', y='Frequency', color='Gender', 
             hover_data = ['Frequency'], width=1000, height=600, barmode='group', color_discrete_map = {'Male':'deepskyblue', 'Female':'hotpink'}, 
             labels={'Response':'It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family.'}, 
             category_orders={'Response':['strongly disagree', 'disagree', 'agree', 'strongly disagree']})
fig3.update(layout=dict(title=dict(x=0.5)))
fig3.update_layout(showlegend=True)

scat4 = gss_clean[~gss_clean.sex.isnull()]

scat4['sex'] = scat4['sex'].replace({'female':'Female', 'male':'Male'})
fig4 = px.scatter(scat4, x='job_prestige', y='income', 
                 color = 'sex', 
                 height=600, width=800,
                 labels={'job_prestige':'Occupational Prestige Score', 
                        'income':'Annual Income', 
                        'sex':'Gender'},
                 hover_data=['education', 'socioeconomic_index'], 
                 trendline='ols', color_discrete_map = {'Male':'deepskyblue', 'Female':'hotpink'})
fig4.update(layout=dict(title=dict(x=0.5)))

# Income
gss_clean['sex'] = gss_clean['sex'].replace({'female':'Female', 'male':'Male'})
fig5 = px.box(gss_clean, x='income', y = 'sex', color = 'sex',
                   labels={'sex':'Gender', 
                           'income':'Annual Income'}, color_discrete_sequence=['deepskyblue', 'hotpink'])
fig5.update(layout=dict(title=dict(x=0.5)))
fig5.update_layout(showlegend=False)

# Job Prestige
fig5_2 = px.box(gss_clean, x='job_prestige', y = 'sex', color = 'sex',
                   labels={'sex':'Gender', 
                           'job_prestige':'Occupational Prestige Score'}, color_discrete_sequence=['deepskyblue', 'hotpink'])
fig5_2.update(layout=dict(title=dict(x=0.5)))
fig5_2.update_layout(showlegend=False)

df6 = gss_clean[['income', 'sex', 'job_prestige']].dropna()
bins = [0, 27, 38, 49, 60, 71, 90]
names = ['Not prestigious', 'Slightly prestigious', 'Moderately prestigious', 'Prestigious', 'Extremely prestigious', 'The most prestigious']

d = dict(enumerate(names, 1))

df6['PresRange'] = np.vectorize(d.get)(np.digitize(df6['job_prestige'].dropna(), bins))
# Facet grid (3x2)

df6['PresRange'] = df6['PresRange'].astype('category')

fig_box = px.box(df6, x='sex', y = 'income', color = 'sex', facet_col='PresRange',
                   labels={'PresRange':'Occupational Prestige', 'sex':'Gender', 'income': 'Annual Income'},
                   facet_col_wrap=2, color_discrete_map = {'Male':'deepskyblue', 'Female':'hotpink'}, height=1000, 
                   category_orders = {'PresRange':['Not prestigious', 'Slightly prestigious', 'Moderately prestigious', 'Prestigious', 'Extremely prestigious', 'The most prestigious']})
fig_box.update(layout=dict(title=dict(x=0.5)))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

markdown_text = """
   For 50 years, the General Social Survey (GSS) has been conducted to collect and compare trends in opinions, attitudes, and behaviors on contemporary American society. The GSS consists of questions ranging from a demographic, behavioral, to an attitudinal standpoint. More specific topics addressed, for example, are civil liberties, crime and violence, intergroup tolerance, morality, national spending priorities, psychological well-being, social mobility, and stress and traumatic events. The majority of the data was collected via face-to-face interviews. However in recent years, computer-assisted personal interviewing (CAPI) and phone interviews, given special circumstances, began. This dataset in particular, consists of seventeen features, or questions asked during the General Social Survey (https://gss.norc.org/faq). These features are as followed: 
* `id`: a numeric unique ID for each person who responded to the survey
* `weight`: survey sample weights
* `sex`: whether the respondent is male or female
* `education`: years of formal education
* `region`: region of the country where the respondent lives
* `age`: age (years)
* `income`: the respondent's personal annual income
* `job_prestige`: the respondent's occupational prestige score, as measured by the GSS using the methodology described above
* `mother_job_prestige`: the respondent's mother's occupational prestige score, as measured by the GSS using the methodology described above
* `father_job_prestige`: the respondent's father's occupational prestige score, as measured by the GSS using the methodology described above
* `socioeconomic_index`: an index measuring the respondent's socioeconomic status
* `satjob`: responses to 'On the whole, how satisfied are you with the work you do?'
* `relationship`: agree or disagree with: 'A working mother can establish just as warm and secure a relationship with her children as a mother who does not work.'
* `male_breadwinner`: agree or disagree with: 'It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family.'
* `men_bettersuited`: agree or disagree with: 'Most men are better suited emotionally for politics than are most women.'
* `child_suffer`: agree or disagree with: 'A preschool child is likely to suffer if his or her mother works.'
* `men_overwork`: agree or disagree with: 'Family life often suffers because men concentrate too much on their work.'
   
These feature variables will be used in the following visualizations to explore the gender wage gap. 

Although calculated many different ways, the gender wage gap explains the difference in income betweeen men and women in the US. Analyzing the most recent Census Bureau data from 2018, women on average, regrdless of race, only 82 cents for every 1 dollar earned by men (https://www.americanprogress.org/article/quick-facts-gender-wage-gap/). Resulting in a wage gap of 18 cents, this measure is calculated by the ratio of median annual earnings, men compared to women. The visualizations presented in this dashboard will combine what we know about the gender wage gap, combined with social factors from the General Social Survey. 
"""

# Populate the dashboard 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("General Social Survey Trends"), 
        
        dcc.Markdown(children = markdown_text), 
        
        html.H2('Average Statistics, by Gender'), 
        dcc.Graph(figure=table), 
        
        html.H2('What is the overall sentiment of traditional family-gender roles?'), 
        dcc.Graph(figure=fig3), 
        
        html.H2('GSS Occupational Prestige Scores x Annual Income, by Gender'), 
        dcc.Graph(figure=fig4), 
        
        html.Div([
            html.H2('Annual Income Discrepencies between Men and Women'), 
            dcc.Graph(figure=fig5) 
        
        ], style = {'width':'48%', 'float':'left'}), 
    
        html.Div([
            html.H2('Differences in Occupational Prestige Scores between Men and Women'), 
            dcc.Graph(figure=fig5_2)
        ], style = {'width':'48%', 'float':'right'}),
        
        html.H2('Income Distributions of Men and Women, based on Job Prestige'), 
        dcc.Graph(figure=fig_box),
    ])
    
   

if __name__ == '__main__':
    app.run_server(debug=True)
