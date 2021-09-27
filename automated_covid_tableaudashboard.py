# link to dashboard : https://public.tableau.com/app/profile/noor.fatima/viz/CovidDashboard-AutomatedDailyRefresh/Dashboard1
# Step1 : Importing libraries and latest Covid data into dataframe from ourworldindata.org.
from datetime import datetime
start_time = datetime.now()
import pandas as pd
from pandas import Series,DataFrame
covid_data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
# Step2 : Extracting covid_deaths and covid_vaccinations dataframes from 'covid_data' dataframe.Columns which are not part of the analysis will be filtered out in this step.
covid_deaths=pd.concat([covid_data.iloc[:,0:4],covid_data.iloc[:,46],covid_data.iloc[:,4:25]],axis=1)
covid_vaccinations=pd.concat([covid_data.iloc[:,0:4],covid_data.iloc[:,25:]],axis=1)
# Step3 : Save the filtered dataframes as csv files
covid_deaths.to_csv('D:\data analytics\covid19_dashboard\covid_deaths.csv',index = False)
covid_vaccinations.to_csv('D:\data analytics\covid19_dashboard\covid_vaccinations.csv',index = False)
# Step4 : Connection is established to SQL Server using pyodbc 
import pyodbc 
# Passing  in the names of server and name of database
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-URQRB3Q\SQLEXPRESS;'
                      'Database=Covid19_data;'
                      'Trusted_Connection=yes;'  ) 
    

#Step5 : Creating tables 'Covid_deaths' and 'Covid_vaccinations' in SQL database.The latest data is imported from 'ourworldindata.org' daily.Old tables are dropped and new tables are created everytime with latest data. 
cursor = conn.cursor()
import_covid_deaths='''
USE [Covid19_data];

IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[covid_deaths]') AND type in (N'U'))
DROP TABLE [dbo].[covid_deaths];


SET ANSI_NULLS ON;


SET QUOTED_IDENTIFIER ON;


CREATE TABLE [dbo].[covid_deaths](
[iso_code] [varchar](50) NULL,
[continent] [varchar](50) NULL,
[location] [varchar](50) NULL,
[date] [date] NULL,
[population] [float] NULL,
[total_cases] [float] NULL,
[new_cases] [float] NULL,
[new_cases_smoothed] [varchar](50) NULL,
[total_deaths] [float] NULL,
[new_deaths] [float] NULL,
[new_deaths_smoothed] [varchar](50) NULL,
[total_cases_per_million] [varchar](50) NULL,
[new_cases_per_million] [varchar](50) NULL,
[new_cases_smoothed_per_million] [varchar](50) NULL,
[total_deaths_per_million] [varchar](50) NULL,
[new_deaths_per_million] [varchar](50) NULL,
[new_deaths_smoothed_per_million] [varchar](50) NULL,
[reproduction_rate] [varchar](50) NULL,
[icu_patients] [varchar](50) NULL,
[icu_patients_per_million] [varchar](50) NULL,
[hosp_patients] [varchar](50) NULL,
[hosp_patients_per_million] [varchar](50) NULL,
[weekly_icu_admissions] [varchar](50) NULL,
[weekly_icu_admissions_per_million] [varchar](50) NULL,
[weekly_hosp_admissions] [varchar](50) NULL,
[weekly_hosp_admissions_per_million] [varchar](50) NULL
) 
ON [PRIMARY];

BULK INSERT [covid_deaths]
FROM 'D:\data analytics\covid19_dashboard\covid_deaths.csv'
WITH(FORMAT ='CSV',FIRSTROW = 2)
'''
cursor.execute(import_covid_deaths)
conn.commit()
import_covid_vaccinations='''
USE [Covid19_data];


IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[covid_vaccinations]') AND type in (N'U'))
DROP TABLE [dbo].[covid_vaccinations];


SET ANSI_NULLS ON;

SET QUOTED_IDENTIFIER ON;

CREATE TABLE [dbo].[covid_vaccinations](
[iso_code] [varchar](50) NULL,
[continent] [varchar](50) NULL,
[location] [varchar](50) NULL,
[date] [date] NULL,
[new_tests] [float] NULL,
[total_tests] [float] NULL,
[total_tests_per_thousand] [float] NULL,
[new_tests_per_thousand] [float] NULL,
[new_tests_smoothed] [float] NULL,
[new_tests_smoothed_per_thousand] [float] NULL,
[positive_rate] [varchar](50) NULL,
[tests_per_case] [varchar](50) NULL,
[tests_units] [varchar](50) NULL,
[total_vaccinations] [varchar](50) NULL,
[people_vaccinated] [varchar](50) NULL,
[people_fully_vaccinated] [varchar](50) NULL,
[total_boosters] [varchar](50) NULL,
[new_vaccinations] [varchar](50) NULL,
[new_vaccinations_smoothed] [varchar](50) NULL,
[total_vaccinations_per_hundred] [varchar](50) NULL,
[people_vaccinated_per_hundred] [varchar](50) NULL,
[people_fully_vaccinated_per_hundred] [varchar](50) NULL,
[total_boosters_per_hundred] [varchar](50) NULL,
[new_vaccinations_smoothed_per_million] [varchar](50) NULL,
[stringency_index] [varchar](50) NULL,
[population] [float] NULL,
[population_density] [varchar](50) NULL,
[median_age] [varchar](50) NULL,
[aged_65_older] [varchar](50) NULL,
[aged_70_older] [varchar](50) NULL,
[gdp_per_capita] [varchar](50) NULL,
[extreme_poverty] [varchar](50) NULL,
[cardiovasc_death_rate] [varchar](50) NULL,
[diabetes_prevalence] [varchar](50) NULL,
[female_smokers] [varchar](50) NULL,
[male_smokers] [varchar](50) NULL,
[handwashing_facilities] [varchar](50) NULL,
[hospital_beds_per_thousand] [varchar](50) NULL,
[life_expectancy] [varchar](50) NULL,
[human_development_index] [varchar](50) NULL,
[excess_mortality] [varchar](50) NULL
) ON [PRIMARY];


BULK INSERT [covid_vaccinations]
FROM 'D:\data analytics\covid19_dashboard\covid_vaccinations.csv'
WITH(FORMAT ='CSV',FIRSTROW = 2)
'''
cursor.execute(import_covid_vaccinations)
conn.commit()
# Step6 :4 queries will be executed from these tables and stored in dataframes using pandas. 
#Getting total covid cases and total deaths globally 
query1 = '''
SELECT 
    SUM(new_cases) AS total_cases, 
    SUM(new_deaths) AS total_deaths, 
    SUM(new_deaths)/SUM(new_cases)*100 AS total_death_percentage 
FROM [Covid19_data].dbo.covid_deaths 
WHERE continent IS NOT NULL 
ORDER BY 1,2;
'''
# Run the query and save the output to a dataframe
table1 = pd.read_sql_query(query1,conn) # pass in the query, and the connection

#Getting covid deaths and cases in different continents of the world
query2 = '''
SELECT location ,  sum(cast(new_deaths as int)) as total_deaths

FROM [Covid19_data].dbo.covid_deaths 
WHERE continent is null
and
location not in ('World','Europeon Union','International')
Group by location
order by total_deaths desc

'''
table2 = pd.read_sql_query(query2,conn)
#Getting hightest infection count from different countries todate.Maximum of all the cases reported daily will be selected for each country.(achieved using Group by location and population)
query3='''
SELECT
 location,population, max(total_cases) as HighestInfectionCount,(Max(total_cases)/population)*100 as PercentPopulationInfected
from
[Covid19_data].dbo.covid_deaths 
Group by location,population
order by PercentPopulationInfected desc
'''
table3 = pd.read_sql_query(query3,conn)
table3 = table3.fillna(0)
#Daily infection count is recorded for each country.Because of large amount of data, timeline of infection count for only few countries will be represented visually.
query4='''
SELECT
 location,date,population, max(total_cases) as HighestInfectionCount,(Max(total_cases)/population)*100 as PercentPopulationInfected
from
[Covid19_data].dbo.covid_deaths 
Group by location,population,date
order by PercentPopulationInfected desc
'''
table4 = pd.read_sql_query(query4,conn)
table4 = table4.fillna(0)

# Step7 : Since our aim is automatic refresh of data in Tableau, we will export these 4 dataframes in Google Sheets using pygsheets library
import pygsheets
creds = r"C:\Users\Noor Fatima\Downloads\credential.json" #pass in the key json file
api = pygsheets.authorize(service_file=creds)

# Open the workbook that contains the final output
wb = api.open('Covid Tables') # pass in the name of the workbook
# Open Sheet1
sheet1= wb.worksheet_by_title(f'Sheet1')
# Write table1 into Sheet1
sheet1.set_dataframe(table1, (1,1)) #specify the position, (1,1) means A1 - the first cell
# Open Sheet2
sheet2= wb.worksheet_by_title(f'Sheet2')
# Write table2 into Sheet2
sheet2.set_dataframe(table2, (1,1)) #specify the position, (1,1) means A1 - the first cell
# Open Sheet3
sheet3= wb.worksheet_by_title(f'Sheet3')
# Write table3 into Sheet3
sheet3.set_dataframe(table3, (1,1)) #specify the position, (1,1) means A1 - the first cell
# Open Sheet4
sheet4= wb.worksheet_by_title(f'Sheet4')
# Write table4 into Sheet4
sheet4.set_dataframe(table4, (1,1)) #specify the position, (1,1) means A1 - the first cell

# Step8 : Adding timelog in Goolge sheets and also generating a timelog text document so that we have information on latest time the data is refreshed. 
end_time = datetime.now()
elapsed_time = end_time - start_time

date = end_time.strftime("%m/%d/%y")
time = end_time.strftime("%H:%M")

datetime_message = 'Updated at: ' + time + ' on ' + date + '\n' 
runtime_message = 'Runtime: ' + str(elapsed_time) + '\n'+ "*"*50 + '\n'

# Write the update time to Google Sheet
table5 = pd.DataFrame.from_dict({'last_update':[time,date]})
sheet5 = wb.worksheet_by_title(f'Sheet5')
sheet5.set_dataframe(table5, (1,1))


with open('update_log.txt','a') as file:
    file.write(datetime_message+runtime_message)
