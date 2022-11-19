from google.oauth2 import service_account
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def main():
    #init google sheet
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'keys.json'
    SAMPLE_SPREADSHEET_ID = '1WqnSubcBJYzAkTmHk8-tNVMz3WCLTot2t5tg12zJo-E'
    credentials = None
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes = SCOPES)
    service = build('sheets', 'v4', credentials = credentials)
    sheet = service.spreadsheets()

    #retrieve data from web op.gg
    winSoloQ,loseSoloQ = getSummonersData()

    #write in sheet
    value = []

    for i in range(3):
        value.append([winSoloQ[i],loseSoloQ[i]])

    print(value)

    sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID, range = "PRE SAISON!C24",
    valueInputOption="USER_ENTERED",body = {"values": value}).execute()
    
    value = []
    for i in range(4,5):
        value.append([winSoloQ[i],loseSoloQ[i]])

    print(value)
    
    sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID, range = "PRE SAISON!C32",
    valueInputOption="USER_ENTERED",body = {"values": value}).execute()

#retrieve data from web op.gg
def getSummonersData():
    winLoseSoloQ = []
    summonerNames = ["APO Boby","Morvatch","Dreadless","LA MERE A WAKZ","PtitHeri"]
    winSoloQ = []
    loseSoloQ = []

    options = webdriver.chrome.options.Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    for name in summonerNames:
        url = "https://www.op.gg/summoners/euw/" + name
        driver.get(url)
        winLose = driver.find_element(By.XPATH,'//*[@id="content-container"]/div[1]/div[1]/div[2]/div[3]/div[1]').text
        winLoseSoloQ.append(winLose)

    winSoloQ = list(map(lambda x: x[0], winLoseSoloQ))
    loseSoloQ = list(map(lambda x: x[3], winLoseSoloQ))

    print(winLoseSoloQ)
    print(winSoloQ)
    print(loseSoloQ)

    return winSoloQ,loseSoloQ

main()


