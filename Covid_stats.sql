--SELECT * FROM PortfolioProject..covidDeaths
--order by 3,4

--SELECT * FROM PortfolioProject..CovidVaccinations
--order by 3,4

SELECT Location,date,total_cases,total_deaths,population
FROM
PortfolioProject..covidDeaths
where continent is not NULL
order by 1,2

--Likelihood of dying if contracted Covid in USA
SELECT Location,date,total_cases,total_deaths,(total_deaths/total_cases)*100 as DeathPercentage
FROM
PortfolioProject..covidDeaths
WHERE Location like '%states%'
order by 1,2

--Looking at total cases vs population--
--shows percentage of population infected with Covid
SELECT Location,date,population,total_cases,(total_cases/population)*100 as InfectedPercentage
FROM
PortfolioProject..covidDeaths
WHERE Location like '%states%'
order by 1,2


--Looking at countries with highest infection rate compared to population
SELECT Location,population,max(total_cases) as HighestInfectionCount,MAX((total_cases/population)*100) as InfectedPercentage
FROM
PortfolioProject..covidDeaths
where continent is not NULL
Group by Location,population
order by 4 DESC

---Countries with highest deathcount per population
SELECT Location,population,max(cast(total_deaths as int)) as HighestDeathCount
FROM
PortfolioProject..covidDeaths
where continent is not NULL
Group by Location,population
order by 3 DESC

---Lets break things by continent----
SELECT location,max(cast(total_deaths as int)) as HighestDeathCount
FROM
PortfolioProject..covidDeaths
where continent is NULL
Group by location
order by 2 DESC


--Lets break things by continent---
SELECT continent,max(cast(total_deaths as int)) as HighestDeathCount
FROM
PortfolioProject..covidDeaths
where continent is not NULL
Group by continent
order by 2 DESC


--GLOBAL nUMBERS---

SELECT date,sum(new_cases) as new_cases,sum(cast(new_deaths as int)) as new_deaths,(sum(cast(new_deaths as int))/sum(new_cases))*100 as Death_percentage
FROM
PortfolioProject..covidDeaths
WHERE CONTINENT IS NOT null
group by date
order by 1,2

--getting total death percentage till date for whole world
SELECT sum(new_cases) as new_cases,sum(cast(new_deaths as int)) as new_deaths,(sum(cast(new_deaths as int))/sum(new_cases))*100 as Death_percentage
FROM
PortfolioProject..covidDeaths
WHERE CONTINENT IS NOT null
--group by date
order by 1,2

--Looking at total populations vs vaccinations

Select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations,
sum(cast(vac.new_vaccinations as int)) over (partition by dea.location order by dea.date,dea.location) as rolling_vaccination_sum
from 
PortfolioProject..covidDeaths dea
join PortfolioProject..CovidVaccinations vac
on dea.date=vac.date and
dea.location=vac.location
WHERE dea.continent is not NULL
order by 2,3

--USE CTE

WITH popvsvac (continent,location,date,population,new_vaccinations,rolling_vaccination_sum)
as
(
Select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations,
sum(cast(vac.new_vaccinations as int)) over (partition by dea.location order by dea.date,dea.location) as rolling_vaccination_sum
from 
PortfolioProject..covidDeaths dea
join PortfolioProject..CovidVaccinations vac
on dea.date=vac.date and
dea.location=vac.location
WHERE dea.continent is not NULL
--order by 2,3
)
SELECT *  ,(rolling_vaccination_sum/population)*100 as peprcentage_vacicnated from popvsvac 

--TEMP table

DROP TABLE IF EXISTS #PercenPopulationVaccinated
Create Table #PercenPopulationVaccinated
(

Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric, 
Rolling_people_vaccinated numeric

)


Insert into #PercenPopulationVaccinated


Select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations,
sum(cast(vac.new_vaccinations as int)) over (partition by dea.location order by dea.date,dea.location) as rolling_vaccination_sum
from 
PortfolioProject..covidDeaths dea
join PortfolioProject..CovidVaccinations vac
on dea.date=vac.date and
dea.location=vac.location
WHERE dea.continent is not NULL
--order by 2,3

SELECT *  ,(Rolling_people_vaccinated/population)*100 as peprcentage_vacicnated from #PercenPopulationVaccinated



--Creating View to store data for later data visualizations

Create View Percent_Population_Vaccinated as

Select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations,
sum(cast(vac.new_vaccinations as int)) over (partition by dea.location order by dea.date,dea.location) as rolling_vaccination_sum
from 
PortfolioProject..covidDeaths dea
join PortfolioProject..CovidVaccinations vac
on dea.date=vac.date and
dea.location=vac.location
WHERE dea.continent is not NULL
--order by 2,3

SELECT * FROM Percent_Population_Vaccinated