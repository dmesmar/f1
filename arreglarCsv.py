import numpy as np
import pandas as pd


circuits = pd.read_csv("data/circuits.csv")
constructor_results = pd.read_csv("data/constructor_results.csv")
constructor_standings = pd.read_csv("data/constructor_standings.csv")
constructors = pd.read_csv("data/constructors.csv")
driver_standings = pd.read_csv("data/driver_standings.csv")
drivers = pd.read_csv("data/drivers.csv")
lap_times = pd.read_csv("data/lap_times.csv")
pit_stops = pd.read_csv("data/pit_stops.csv")
qualifying = pd.read_csv("data/qualifying.csv")
races = pd.read_csv("data/races.csv")
results = pd.read_csv("data/results.csv")
seasons = pd.read_csv("data/seasons.csv")
sprint_results = pd.read_csv("data/sprint_results.csv")
status = pd.read_csv("data/status.csv")

# El añadir si los circuitos son urbanos que es manual

NUMBER_OF_DRIVERS = drivers.shape[0]

# Quitar la columna de url
if "url" in seasons.columns:
    seasons = seasons.drop("url", axis=1)
seasons = seasons.sort_values("year")

# Añadir a seasons el ganador de cada año
def calculateWorldChampion(year, constructor=False):
    racesWDC = races[races["year"]==year]
    racesWDC = racesWDC.merge(results, on="raceId")

    listaCarreras = []
    mundial = {}
    listaCarrerasSprint = []
    for i in range(0, len(racesWDC)):
        loopRaceId = int(racesWDC.iloc[i].get("raceId"))
        if constructor:
            loopIdDriver = int(racesWDC.iloc[i].get("constructorId"))
        else:
            loopIdDriver = int(racesWDC.iloc[i].get("driverId"))
        loopPoints = int(racesWDC.iloc[i].get("points"))
        sprint = racesWDC.iloc[i].get("sprint_date")
        if sprint != "\\N":
            listaCarrerasSprint.append(loopRaceId)
        if loopIdDriver not in mundial:
            mundial[loopIdDriver] = loopPoints
        else:
            mundial[loopIdDriver] += loopPoints

    listaCarrerasSprint = list(set(listaCarrerasSprint))
    sprint_results_WDC = sprint_results[sprint_results["raceId"].isin(listaCarrerasSprint)]

    for i in range(0, len(sprint_results_WDC)):
        loopRaceId = int(sprint_results_WDC.iloc[i].get("raceId"))
        if constructor:
            loopIdDriver = int(sprint_results_WDC.iloc[i].get("constructorId"))
        else:
            loopIdDriver = int(sprint_results_WDC.iloc[i].get("driverId"))
        loopPoints = int(sprint_results_WDC.iloc[i].get("points"))
        sprint = sprint_results_WDC.iloc[i].get("sprint_date")
        if loopIdDriver not in mundial:
            mundial[loopIdDriver] = loopPoints
        else:
            mundial[loopIdDriver] += loopPoints


    mundial = {k: v for k, v in sorted(mundial.items(), key=lambda item: item[1], reverse=True)}

    driverId = max(mundial.items(), key=lambda x: (x[1], -x[0]))[0]
    return driverId

if "championshipWinnerId" not in seasons.columns:
    championshipWinnerId = []
    for i in range(0, len(seasons)):
        year = seasons.iloc[i].get("year")
        championshipWinnerId.append(calculateWorldChampion(year, False))
    seasons["championshipWinnerId"] = championshipWinnerId
    seasons.to_csv("data/seasons.csv", index=False)
if "constructorWinnerId" not in seasons.columns:
    constructorWinnerId = []
    for i in range(0, len(seasons)):
        year = seasons.iloc[i].get("year")
        constructorWinnerId.append(calculateWorldChampion(year, True))
    seasons["constructorWinnerId"] = constructorWinnerId
    seasons.to_csv("data/seasons.csv", index=False)


# Quitar la columna de url
if "url" in drivers.columns:
    drivers = drivers.drop("url", axis=1)

# nRaces, nRacesWon, nPodiums
def calculateRaces():
    nRaces = []
    nRacesWon = []
    nPodiums = []
    for i in range(0, len(drivers)):
        loopDriverId = drivers.iloc[i].get("driverId")
        # buscar carreras en las que participe loopDriverId y guardar el raceId
        loopResults = results[results["driverId"] == loopDriverId]
        loopResultsWon = loopResults[loopResults["position"] == "1"]
        loopResultsPodium = loopResults[loopResults["position"].isin(["1","2","3"])]
        nRaces.append(loopResults.shape[0]) # nRaces
        nRacesWon.append(loopResultsWon.shape[0]) # nRacesWon
        nPodiums.append(loopResultsPodium.shape[0]) # nPodiums
    drivers["nRaces"] = nRaces
    drivers["nRacesWon"] = nRacesWon
    drivers["nPodiums"] = nPodiums
    drivers.to_csv("data/drivers.csv", index=False)

if "nRaces" not in drivers.columns:
    calculateRaces()


def calculateH2Hr():
    #h2hrW, h2hrL
    h2hrW = [] # head 2 head race wins
    h2hrL = [] # head 2 head race loses
    for i in range(0, len(drivers)):
        loopDriverId = drivers.iloc[i].get("driverId")
        loopResults = results[results["driverId"] == loopDriverId]
        h2hW = 0
        h2hL = 0
        for j in range(0, len(loopResults)):
            loopRaceId = loopResults.iloc[j].get("raceId")
            loopConstructorId = loopResults.iloc[j].get("constructorId")
            rivalRace = results[
                (results["raceId"] == loopRaceId) &
                (results["constructorId"] == loopConstructorId) &
                (results["driverId"] != loopDriverId)
            ]
            positionHero = loopResults.iloc[j].get("position")
            if not rivalRace.empty:
                positionRival = rivalRace.iloc[0].get("position")
                if positionHero == "\\N":
                    positionHero = 99
                if positionRival == "\\N":
                    positionRival = 99
                
                if int(positionHero) > int(positionRival):
                    h2hL += 1
                elif int(positionRival) > int(positionHero):
                    h2hW += 1
            else:
                h2hD += 1
        h2hrW.append(h2hW)
        h2hrL.append(h2hL)
    drivers["h2hrW"] = h2hrW
    drivers["h2hrL"] = h2hrL
    drivers.to_csv("data/drivers.csv", index=False)

if "h2hrW" not in drivers.columns:
    calculateH2Hr()





# h2hqW, h2hqL, q1per, q2per, q3per