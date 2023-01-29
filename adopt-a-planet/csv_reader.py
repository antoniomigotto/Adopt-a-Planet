import pandas as pd
import csv

def planet_finder():
    planet = []
    with open("oec.csv") as csvfile:
        input_items = list(csv.reader(csvfile))
    for i in range(0, len(input_items)):
        if input_items[i][25] == 'False':
            planet = input_items[i]
            print(input_items[i][0])
            csv_changer(input_items[i][26])
            break
    for i in range(0, len(planet)):
        if planet[i] == "":
            planet[i] = "unknown"
            print(planet[i])
        else:
            print(planet[i])
    return planet


def csv_changer(planet_id):
    df = pd.read_csv("oec.csv")

    # updating the column value/data
    df.loc[int(planet_id), "WasAdopted"] = "TRUE"
    print("Changed to TRUE")

    # writing into the file
    df.to_csv("oec.csv", index=False)
