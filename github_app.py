#importing packages
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

#streamlit  background color
page_bg_color='''
<style>
[data-testid="stAppViewContainer"]{
        background-color:#FFDAB9;
}
</style>'''

#streamlit button color
button_style = """
    <style>
        .stButton>button {
            background-color: #ffa089 ; 
            color: black; 
        }
        .stButton>button:hover {
            background-color: #ffddca; 
        }
    </style>    
"""
#streamlit settings
st.set_page_config(
    page_title="Github Data Dive",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="auto")


st.markdown(page_bg_color,unsafe_allow_html=True)  #calling background color
st.markdown(button_style, unsafe_allow_html=True)  #calling button color

st.title("Github Data Dive")

#menu
selected = option_menu(menu_title=None,options= ["HOME", "INSIGHTS"],icons=["house", "bar-chart"],
          default_index=0,orientation='horizontal',
          styles={"container": { "background-color": "white", "size": "cover", "width": "100"},
            "icon": {"color": "brown", "font-size": "20px"},

            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#ffe5b4"},
            "nav-link-selected": {"background-color": "#E2838A"}})

#mysql connection
mydb=sql.connect(host="localhost",user="root",password="root",database= "github",port = "3306")
cursor=mydb.cursor(buffered=True)

#function programming language count
def query1():
    cursor.execute("select Programming_Language, count(Programming_Language) as Count from repositories group by Programming_Language order by Count desc ;")
    q1 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    with st.expander("View Table"):
        st.write(q1)
    st.write("### :orange[  Distribution of Programming Languages:]")
    fig = px.bar(q1,
                     title=' Distribution of Programming Languages ',
                     x="Programming_Language",
                     y="Count",
                     orientation='v',
                     color='Count',
                     color_continuous_scale=px.colors.sequential.Inferno)
    st.plotly_chart(fig,use_container_width=True)

#function reository star count 
def query2():
    c1,c2=st.columns(2)
    with c1:
        cursor.execute("select Repository_Name,Number_of_Stars from repositories order by Number_of_Stars desc limit 15 ")
        q2 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write("### :orange[  Top 15 Repositories by Number of Stars:]")
        with st.expander("View Table"):
            st.write(q2)
        
        fig = px.bar(q2,
                        title='Top 15 Repositories by Number of Stars ',
                        x="Repository_Name",
                        y="Number_of_Stars",
                        orientation='v',
                        color='Number_of_Stars',
                        color_continuous_scale=px.colors.sequential.Viridis)
        st.plotly_chart(fig,use_container_width=True)

    with c2:
        cursor.execute("select Repository_Name,Number_of_Stars from repositories where Number_of_Stars>1 order by Number_of_Stars limit 15 ")
        q2 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write("### :orange[  Top 15 Repositories by Number of Stars:]")
        with st.expander("View Table"):
            st.write(q2)
        
        fig = px.bar(q2,
                        title='Least 15 Repositories by Number of Stars ',
                        x="Repository_Name",
                        y="Number_of_Stars",
                        orientation='v',
                        color='Number_of_Stars',
                        color_continuous_scale=px.colors.sequential.Mint_r)
        st.plotly_chart(fig,use_container_width=True)

#function repo fork count
def query3():
    co1,co2=st.columns(2)
    with co1:
        cursor.execute("select Repository_Name,Number_of_Forks from repositories order by Number_of_Forks desc limit 15 ")
        q3 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write("### :orange[Top 15 Repositories by Number of Forks:]")
        with st.expander("View Table"):
            st.write(q3)
        fig = px.pie(q3,names="Repository_Name",
                            values="Number_of_Forks",
                            title='Top 15 Repositories by Number_of_Forks ',
                            hover_data=['Number_of_Forks'],
                            labels={'Number_of_Forks':'Number_of_Forks'},
                            color_discrete_sequence=px.colors.sequential.Pinkyl,hole=0.2)
        st.plotly_chart(fig,use_container_width=True)
    with co2:
        cursor.execute("select Repository_Name,Number_of_Forks from repositories where Number_of_Forks>1 order by Number_of_Forks  limit 15 ")
        q3 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write("### :orange[Least 15 Repositories by Number of Forks:]")
        with st.expander("View Table"):
            st.write(q3)
        fig = px.pie(q3,names="Repository_Name",
                            values="Number_of_Forks",
                            title='Least 15 Repositories by Number_of_Forks ',
                            hover_data=['Number_of_Forks'],
                            labels={'Number_of_Forks':'Number_of_Forks'},
                            color_discrete_sequence=px.colors.sequential.Magenta,hole=0.2)
        st.plotly_chart(fig,use_container_width=True)

#function license count
def query4():
    cursor.execute("select License_Type,count(License_Type) as count from repositories group by License_Type order by count desc")
    q4 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    st.write("### :orange[Count of License Types:]")
    with st.expander("View Table"):
        st.write(q4)
    fig = px.bar(q4,
                    title='License Types',
                    x="License_Type",
                    y="count",
                    orientation='v',
                    color='count',
                    color_continuous_scale=px.colors.sequential.Sunsetdark)
    st.plotly_chart(fig,use_container_width=True)

#function repo creation date
def query5(year):
    
    cursor.execute("select Repository_Name, Creation_Date from repositories where YEAR(Creation_Date) =%s  ",(c_year,))
    q5 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    st.write("### :orange[Repository Creation date per year:]")
    with st.expander("View Table"):
        st.write(q5)
    fig = px.treemap(q5, 
                 path=['Repository_Name'], 
                 title="Repository Creation date per year",
                 color='Creation_Date',  
                 color_discrete_sequence=px.colors.sequential.YlOrRd_r)
    st.plotly_chart(fig,use_container_width=True)

    cursor.execute("""SELECT YEAR(Creation_Date) AS creation_year, COUNT(*) AS count FROM repositories GROUP BY creation_year ORDER BY creation_year ASC;""")
    q5 = pd.DataFrame(cursor.fetchall(), columns=['creation_year', 'count'])
    st.write("### :orange[Number of Repositories Created Over the Years:]")
    with st.expander("View Table"):
        st.write(q5)
    fig = px.line(q5, 
                title='Number of Repositories Created Over the Years', 
                x='creation_year',  
                y='count',           
                markers=True,        
                line_shape='linear', 
                color_discrete_sequence=px.colors.sequential.Aggrnyl)  
    st.plotly_chart(fig, use_container_width=True)


    cursor.execute("SELECT YEAR(Creation_Date) AS creation_year, MONTH(Creation_Date) AS creation_month, COUNT(*) AS count FROM repositories GROUP BY creation_year, creation_month ORDER BY creation_year, creation_month;")
    q5 = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    st.write("### :orange[Heatmap of Repository Creation by Year and Month:]")
    with st.expander("View Table"):
        st.write(q5)
    fig = px.density_heatmap(q5,
                         x='creation_year', 
                         y='creation_month', 
                         z='count',
                         title='Heatmap of Repository Creation by Year and Month',
                         color_continuous_scale=px.colors.sequential.BuPu_r)
    st.plotly_chart(fig,use_container_width=True)

    cursor.execute("SELECT YEAR(Creation_Date) AS creation_year, Programming_Language AS language, COUNT(*) AS count FROM repositories GROUP BY creation_year, language ORDER BY creation_year;")
    q5 = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    st.write("### :orange[Language Popularity Over Time:]")
    with st.expander("View Table"):
        st.write(q5)
    fig = px.area(q5, 
              x='creation_year', 
              y='count', 
              color='language', 
              title='Language Popularity Over Time')
    st.plotly_chart(fig,use_container_width=True)

#function repo update date
def query6(year):

    cursor.execute("select Repository_Name, Last_Updated_Date from repositories where YEAR(Last_Updated_Date) =%s  ",(u_year,))
    q6 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    st.write("### :orange[Repository update date per year:]")
    with st.expander("View Table"):
        st.write(q6)
    fig = px.treemap(q6, 
                 path=['Repository_Name'],  
                 title="Repository update date per year",
                 color='Last_Updated_Date', 
                 color_discrete_sequence=px.colors.sequential.gray)
    st.plotly_chart(fig,use_container_width=True)

    cursor.execute("""SELECT YEAR(Last_Updated_Date) AS updated_year, COUNT(*) AS count FROM repositories GROUP BY updated_year ORDER BY updated_year ASC;""")
    q6 = pd.DataFrame(cursor.fetchall(), columns=['updated_year', 'count'])
    st.write("### :orange[Number of Repositories updated Over the Years:]")
    with st.expander("View Table"):
        st.write(q6)
    fig = px.line(q6, 
                title='Number of Repositories updated Over the Years', 
                x='updated_year',   
                y='count',           
                markers=True,        
                line_shape='linear', 
                color_discrete_sequence=["#636EFA"])  
    st.plotly_chart(fig, use_container_width=True)

    cursor.execute("SELECT YEAR(Last_Updated_Date) AS updated_year, MONTH(Last_Updated_Date) AS updated_month, COUNT(*) AS count FROM repositories GROUP BY updated_year, updated_month ORDER BY updated_year, updated_month;")
    q6 = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    st.write("### :orange[Heatmap of Repository updated by Year and Month:]")
    with st.expander("View Table"):
        st.write(q6)
    fig = px.density_heatmap(q6,
                         x='updated_year', 
                         y='updated_month', 
                         z='count',
                         title='Heatmap of Repository updated by Year and Month',
                         color_continuous_scale=px.colors.sequential.Burg)
    st.plotly_chart(fig,use_container_width=True)

    cursor.execute("SELECT YEAR(Last_Updated_Date) AS updated_year, Programming_Language AS language, COUNT(*) AS count FROM repositories GROUP BY updated_year, language ORDER BY updated_year;")
    q6 = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    st.write("### :orange[Language Popularity Over Time:]")
    with st.expander("View Table"):
        st.write(q6)
    fig = px.area(q6, 
              x='updated_year', 
              y='count', 
              color='language', 
              title='Language Popularity Over Time')
    st.plotly_chart(fig,use_container_width=True)

#function creation vs update date
def query7():
    cursor.execute("SELECT Repository_Name, Creation_Date, Last_Updated_Date FROM repositories;")
    q7 = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    st.write("### :orange[Repository Creation Date vs Last Update Date:]")
    with st.expander("View Table"):
        st.write(q7)
    fig = px.scatter(q7, 
                 x='Creation_Date', 
                 y='Last_Updated_Date', 
                 title='Repository Creation Date vs Last Update Date',
                 hover_data=['Repository_Name'],
                 color_discrete_sequence=px.colors.sequential.PuBu_r)
    st.plotly_chart(fig,use_container_width=True)

    cursor.execute("SELECT YEAR(Creation_Date) AS year, COUNT(Creation_Date) AS created_count, COUNT(Last_Updated_Date) AS updated_count FROM repositories GROUP BY year;")
    q7 = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    st.write("### :orange[Comparison of Repository Creation and Update Frequency:]")
    with st.expander("View Table"):
        st.write(q7)
    fig = px.bar(q7,
             x='year',
             y=['created_count', 'updated_count'],
             title='Comparison of Repository Creation and Update Frequency',
             barmode='group')
    st.plotly_chart(fig,use_container_width=True)

    cursor.execute("SELECT Repository_Name, Programming_Language AS language,DATEDIFF(Last_Updated_Date, Creation_Date) AS time_diff FROM repositories;")
    q7 = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    st.write("### :orange[Time Between Repository Creation and Last Update by Language:]")
    with st.expander("View Table"):
        st.write(q7)
    fig = px.box(q7,
             x='language', 
             y='time_diff', 
             title='Time Between Repository Creation and Last Update by Language',
             color_discrete_sequence=px.colors.sequential.Redor_r)
    st.plotly_chart(fig,use_container_width=True)

#function repo open issue count
def query8():
    col1,col2=st.columns(2)
    with col1:
        cursor.execute("select Repository_Name,Number_of_Open_Issues from repositories order by Number_of_Open_Issues desc limit 15 ")
        q8 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write("### :orange[  Top 15 Repositories by Number_of_Open_Issues:]")
        with st.expander("View Table"):
            st.write(q8)
        
        fig = px.pie(q8,names="Repository_Name",
                        values="Number_of_Open_Issues",
                        title='Top 15 Repositories by Number_of_Open_Issues ',
                        hover_data=['Number_of_Open_Issues'],
                        labels={'Number_of_Open_Issues':'Number_of_Open_Issues'},
                        color_discrete_sequence=px.colors.sequential.Peach)
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        cursor.execute("select Repository_Name,Number_of_Open_Issues from repositories where Number_of_Open_Issues>1 order by Number_of_Open_Issues  limit 15 ")
        q8 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.write("### :orange[Least 15 Repositories by Number_of_Open_Issues:]")
        with st.expander("View Table"):
            st.write(q8)
        
        fig = px.pie(q8,names="Repository_Name",
                        values="Number_of_Open_Issues",
                        title='Top 15 Repositories by Number_of_Open_Issues ',
                        hover_data=['Number_of_Open_Issues'],
                        labels={'Number_of_Open_Issues':'Number_of_Open_Issues'},
                        color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig,use_container_width=True)

# function owner repo count
def query9():
    cursor.execute("SELECT Owner, COUNT(Owner) AS count FROM repositories GROUP BY Owner HAVING count > 1;")
    q9 = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
    st.write("### :orange[Owners Having maximum repositories:]")
    with st.expander("View Table"):
        st.write(q9)
    fig = px.treemap(q9, 
                 path=['Owner'], 
                 values='count', 
                 title="Repository Count per Owner",
                 color='count',  
                 color_continuous_scale=px.colors.sequential.Cividis)  
    st.plotly_chart(fig, use_container_width=True) 

#function repo star vs fork vs openissues
def query10():
    cursor.execute("SELECT Repository_Name, Number_of_Stars, Number_of_Forks FROM repositories;")
    q10 = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    st.write("### :orange[Repository Number_of_Stars vs Number_of_Forks:]")
    with st.expander("View Table"):
        st.write(q10)
    fig = px.scatter(q10, 
                 x='Number_of_Stars', 
                 y='Number_of_Forks', 
                 title='Repository Number_of_Stars vs Number_of_Forks',
                 hover_data=['Repository_Name'],
                 color_discrete_sequence=px.colors.sequential.Brwnyl_r)
    st.plotly_chart(fig,use_container_width=True)

    cursor.execute("SELECT Repository_Name, Number_of_Forks,Number_of_Open_Issues FROM repositories;")
    q10 = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    st.write("### :orange[Repository Number_of_Forks vs Number_of_Open_Issues:]")
    with st.expander("View Table"):
        st.write(q10)
    fig = px.scatter(q10, 
                 y='Number_of_Open_Issues', 
                 x='Number_of_Forks', 
                 title='Repository Number_of_Forks vs Number_of_Open_Issues',
                 hover_data=['Repository_Name'],
                 color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig,use_container_width=True)

    cursor.execute("SELECT Repository_Name,Number_of_Open_Issues, Number_of_Stars FROM repositories;")
    q10 = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    st.write("### :orange[Repository Number_of_Open_Issues vs  Number_of_Stars:]")
    with st.expander("View Table"):
        st.write(q10)
    fig = px.scatter(q10, 
                 x='Number_of_Open_Issues', 
                 y='Number_of_Stars', 
                 title='Repository Number_of_Open_Issues vs  Number_of_Stars',
                 hover_data=['Repository_Name'],
                 color_discrete_sequence=px.colors.sequential.YlOrBr_r)
    st.plotly_chart(fig,use_container_width=True)

    cursor.execute("SELECT Repository_Name, Programming_Language AS Language, License_Type, YEAR(Creation_Date) AS Year, Number_of_Stars, Number_of_Forks, Number_of_Open_Issues  FROM repositories where Number_of_Stars>0 ")
    q10 = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    st.write("### :orange[Sunburst Chart of Repositories by Year, License, Language, and Stars:]")
    with st.expander("View Table"):
        st.write(q10)
    fig = px.sunburst(q10, 
                  path=['Year', 'License_Type', 'Language', 'Repository_Name'],  
                  values='Number_of_Stars',  
                  color='Number_of_Stars',  
                  hover_data=['Number_of_Stars','Number_of_Forks','Number_of_Open_Issues'],  
                  title="Sunburst Chart of Repositories by Year, License, Language, and Stars",
                  color_continuous_scale='RdYlBu')  

    st.plotly_chart(fig, use_container_width=True)

#home page
if selected=="HOME":
    coll1,coll2=st.columns(2)
    with coll1:
        st.write("")
        st.write('''**In today's rapidly evolving software development landscape, GitHub serves as a pivotal platform for collaboration and innovation in the open-source community. With millions of repositories available, identifying relevant projects, understanding development trends, and leveraging insights can be challenging for developers, researchers, and organizations alike.**''')
        st.write("")
        st.write('''**This project aims to extract and analyze data from GitHub repositories focused on specific topics,to uncover patterns and trends in repository characteristics, popularity, and technology usage. By leveraging the GitHub API, the project seeks to provide a comprehensive overview of repository dynamics, including metrics like stars, forks, programming languages, and creation dates.**''')
        st.write("")
        st.write('''**The ultimate goal is to create a user-friendly Streamlit application that visualizes these insights, enabling users to make informed decisions regarding project collaboration, technology adoption, and educational resource identification in the open-source ecosystem.**''')

    with coll2:
        st.image(r"C:\Users\HP\Downloads\github.jpg")
#insights page
#selectbox insights
if selected=="INSIGHTS":
    options1=["1. Distribution of Programming Languages",
    "2. Top 15 and Least 15 Repositories by Number of Stars",
    "3. Top 15 and Least 15 Repositories by Number of Forks",
    "4. License Types",
    "5. Repositories based on Creation Date",
    "6. Repositories based on Last Updated Date",
    "7. Comparison of Creation vs. Update Date",
    "8. Top 15 and Least 15 Repositories by Number_of_Open_Issues",
    "9. Owners Having maximum repositories",
    "10. Comparison of No.of.stars vs. No.of.forks vs No.of.open_issues"]
    selection = st.selectbox("QUERIES", options1)

    if selection=="1. Distribution of Programming Languages":
        query1()

    if selection=="2. Top 15 and Least 15 Repositories by Number of Stars":
        query2()
        
    if selection=="3. Top 15 and Least 15 Repositories by Number of Forks":
        query3()
        
    if selection=="4. License Types":
        query4()
        
    if selection=="5. Repositories based on Creation Date":
        cursor.execute("select distinct year(Creation_Date) from repositories order by year(Creation_Date) ")
        q = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        c_year =st.select_slider("Select Year",q['year(Creation_Date)'])
        query5(c_year)
        
    if selection=="6. Repositories based on Last Updated Date":
        cursor.execute("select distinct year(Last_Updated_Date) from repositories order by year(Last_Updated_Date) ")
        q = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        u_year =st.select_slider("Select Year",q['year(Last_Updated_Date)'])
        query6(u_year)

    if selection=="7. Comparison of Creation vs. Update Date":
        query7()
        
    if selection=="8. Top 15 and Least 15 Repositories by Number_of_Open_Issues":
        query8()

    if selection=="9. Owners Having maximum repositories":
        query9()

    if selection=="10. Comparison of No.of.stars vs. No.of.forks vs No.of.open_issues":
        query10()
    

