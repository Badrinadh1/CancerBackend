import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import random
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Number of candidates
@app.on_event("startup")
async def Startup():
    pass


@app.get("/showdataset")
def readDataset():
    file_path="assets/cancer_patient_details.csv"
    data=pd.read_csv(file_path)
    print(data)
    return "Dataset Read Successfully!"

@app.get("/deathsperyear/{year}")
async def deathsperyear(year:int):
    final_data=[]
    file_path="assets/cancer_patient_details.csv"
    data=pd.read_csv(file_path)
    states=data["State"].unique()
    years=data["Year"].unique()
    year_data=data[(data['Year'] == year)]
    state_data=[]
    for state in states:
        data_filtered = year_data[(year_data['Year'] == year) & (year_data['State'] == state)]
        state_data.append({"state":state,"death_count":len(data_filtered)})
    final_data.append({"year":int(year),"state_data":state_data})
    return {"result":final_data}

@app.get("/uniqueyearstate")
def getKeysData():
    file_path="assets/cancer_patient_details.csv"
    data=pd.read_csv(file_path)
    states=[]
    years=[]
    for i in data["State"].unique():
        states.append(str(i))

    for i in data["Year"].unique():
        years.append(int(i))
    return {"states":states,"years":years}


@app.get("/deathspermoth/{year}/{state}")
async def deathspermonth(year:int,state:str):
    month_data=[]
    file_path="assets/cancer_patient_details.csv"
    data=pd.read_csv(file_path)
    data_filtered = data[(data['Year'] == year) & (data['State'] == state)]
    for month in range(1,13):
        data_month=data_filtered[(data_filtered["Death_Month"]==month)]
        month_data.append({"month":month,"deaths":len(data_month)})
    return {"result":month_data}

@app.get("/deathsfortypeofcancers/{year}/{state}")
def deathsForTypeOfCancers(year:int,state:str):
    cancer_data=[]
    file_path="assets/cancer_patient_details.csv"
    data=pd.read_csv(file_path)
    cancers=data["Cancer_Type"].unique()
    data_filtered = data[(data['Year'] == year) & (data['State'] == state)]
    print(len(data_filtered))
    for cancer in cancers:
        data_month=data_filtered[(data_filtered['Cancer_Type'] == str(cancer))]
        cancer_data.append({"cancer":str(cancer),"deaths_count":len(data_month)})
    return {"result":cancer_data}

@app.get("/deathforagegroup/{year}/{state}")
def deathsforagegroup(year:int,state:str):
    age_data=[]
    file_path="assets/cancer_patient_details.csv"
    data=pd.read_csv(file_path)
    age_groups=[[0,7],[8,18],[19,35],[36,50],[51,90]]
    data_filtered = data[(data['Year'] == year) & (data['State'] == state)]
    for i in age_groups:
        data_age = data_filtered[(data_filtered['Age'] >= i[0]) & (data_filtered['Age'] <= i[1])]

        age_data.append({"age":str(i[0])+"-"+str(i[1]),"death_count":len(data_age)})
    return {"result":age_data}

@app.get("/deathsforsmoking/{year}/{state}")
def deathsforsmoking(year:int,state:str):
    smoking_data=[]
    file_path="assets/cancer_patient_details.csv"
    data=pd.read_csv(file_path)
    data_filtered = data[(data['Year'] == year) & (data['State'] == state)]
    for smoke in ["Occasional","Never","Regular"]:
        data_smoking=data_filtered[(data_filtered['Smoking_Habit'] == str(smoke))]
        smoking_data.append({"type":smoke,"death_count":len(data_smoking)})
    return {"result":smoking_data}

@app.get("/deathsfordrinking/{year}/{state}")
def deathsfordrinking(year:int,state:str):
    drinking_data=[]
    file_path="assets/cancer_patient_details.csv"
    data=pd.read_csv(file_path)
    data_filtered = data[(data['Year'] == year) & (data['State'] == state)]
    for drink in ["Social Drinker","Never","Regular Drinker"]:
        data_smoking=data_filtered[(data_filtered['Drinking_Habit'] == str(drink))]
        drinking_data.append({"type":drink,"death_count":len(data_smoking)})
    return {"result":drinking_data}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
