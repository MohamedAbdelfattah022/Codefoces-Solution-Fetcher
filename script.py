import pandas as pd
import requests
import json

def convert(tags):
    return ', '.join(tags)

def get_solved_problems(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"

    data = requests.get(url)
    jsonObject = json.loads(data.text)
    if jsonObject["status"] != "FAILED":
        results = jsonObject["result"]
        
        results_df = pd.DataFrame(results)
        
        solved = results_df.loc[results_df["verdict"] == "OK"]
        solved = solved["problem"].drop_duplicates().reset_index(drop=True)
        
        for i in range(len(solved)):
            solved[i]['tags'] = convert(solved[i]['tags'])

        df = pd.json_normalize(solved).drop(["type", "points", "problemsetName"], axis=1, errors='ignore')

    return df

def generate_link(row):
    if row["contestId"] == "N/A":
        return ""

    if len(row["contestId"]) >= 6:
        return "https://codeforces.com/problemset/gymProblem/" + row["contestId"] + "/" + row["index"]
    else:
        return "https://codeforces.com/contest/" + row["contestId"] + "/problem/" + row["index"]

def toString(id):
    if pd.isna(id):
        return "N/A"
    else:
        return str(int(id))


handle = input("Handle: ") 
df = get_solved_problems(handle)

df["contestId"] = df["contestId"].apply(lambda id: toString(id))
df["rating"] = df["rating"].apply(lambda id: toString(id))

df["url"] = df.apply(generate_link, axis=1)

df.columns = df.columns.str.capitalize()

df = df.drop(["Contestid", "Index"], axis=1)

df.to_excel(f"{handle} solutions.xlsx", index=False)