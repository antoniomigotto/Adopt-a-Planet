import pandas as pd
import csv

def planet_finder():
    planet = []
    with open("oec.csv") as csvfile:
        input_items = list(csv.reader(csvfile))
    for i in range(0, len(input_items)):
        if input_items[i][25] == "FALSE":
            planet = input_items[i]
            break
        elif input_items[i][25] == "False":
            planet = input_items[i]
            break
    for i in range(0, len(planet)):
        if planet[i] == "":
            planet[i] = "Unknown"
            print(planet[i])
        else:
            print(planet[i])
    return planet


def csv_changer(planet_id):

    df = pd.read_csv("oec.csv")

    # updating the column value/data
    df.loc[int(planet_id), "WasAdopted"] = "TRUE"

    # writing into the file
    df.to_csv("oec.csv", index=False)
