import numpy as np
import pandas as pd

races = pd.read_csv("data/races.csv")
drivers = pd.read_csv("data/drivers.csv")
#print(drivers)
sprint_results = pd.read_csv("data/sprint_results.csv", index_col="resultId")
results = pd.read_csv("data/results.csv", index_col="resultId")
#print(sprint_results)
status = pd.read_csv("data/status.csv")

def prueba():
    df = drivers.merge(sprint_results, on="driverId", how="left")
    r2324_noSprint = races[races["sprint_date"] == "\\N"]
    r2324_Sprint = races[races["sprint_date"] != "\\N"]

    print(f"Carreras con sprint: \n{r2324_Sprint}")
    for i in r2324_Sprint["raceId"]:
        carrera = sprint_results[sprint_results["raceId"] == i]
        winners = carrera[carrera["position"]=="1"]
        winners_extra = winners.merge(drivers, on = "driverId").merge(races, on ="raceId")
        print(f'{winners_extra["forename"].get(0)} {winners_extra["surname"].get(0)} ganó el {winners_extra["sprint_date"].get(0)} en {winners_extra["name"].get(0)}')
    results = results.merge(status, on="statusId")
    carrera_18 = results[results["raceId"] == 18]
    carrera_18.drop(["constructorId", "number", "positionText", "milliseconds", "fastestLap", "fastestLapTime", "fastestLapSpeed", "statusId"],axis=1, inplace=True)
    for i in range(0, len(carrera_18)):
        pass
        print(carrera_18.iloc[[i]])


print("Terminado!")