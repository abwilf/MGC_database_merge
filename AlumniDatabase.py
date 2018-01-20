# Mcommunity querying
# Adam Heins

import requests
import pandas 
import json


def parseUmichEmail(email):
	return email.split('@')[0]

def getEmails(csv):
	df = pandas.read_csv(csv)
	return df

def getUmich(df):
	df = df[df.apply(lambda row: row.astype(str).str.contains('umich').any(), axis=1)]
	return df

def getNonUmich(df):
	df = df[~df.apply(lambda row: row.astype(str).str.contains('umich').any(), axis=1)]
	return df

def makeRequest(uniqname):
	url = "http://mcommunity-api.herokuapp.com/"
	data = {"uniqname" : uniqname}

	response = requests.get(url, params=data)

	responseJson = response.json()

	return responseJson

def queryAllUmich(df):
	toReturn = pandas.DataFrame()
	for index, row in df.iterrows():
		email = row["email"]
		newdict = makeRequest(parseUmichEmail(email))

		try:
			firstName = newdict["data"][0]["firstname"]
			lastName = newdict["data"][0]["surname"]
		except:
			firstName = "No Mcommunity data found"
			LastName = "No Mcommunity data found"

		newDF = pandas.DataFrame(data={"Email": [email], "First Name": [firstName], "Last Name": [lastName]})
		toReturn = toReturn.append(newDF)
	toReturn.to_csv("AlumniDatabase - Umich Emails.csv", index=False)


if __name__ == "__main__":
	df = getEmails("alums.csv")
	nonUmich = getNonUmich(df)
	nonUmich.to_csv("AlumniDatabase - Non-Umich Emails.csv", index=False)

