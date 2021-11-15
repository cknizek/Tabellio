import gspread
from datetime import *
import pandas as pd
import time
import pytz

pacific = pytz.timezone('US/Pacific')


credentials = {
  "YOUR CREDENTIALS HERE": "https://docs.gspread.org/en/latest/oauth2.html"
}

gc = gspread.service_account_from_dict(credentials)

sh = gc.open("YOUR-PUBLIC-SPREADSHEET-FILENAME-HERE")
sh2 = gc.open("YOUR-GOOGLE-FORM-RESPONSE-SPREADSHEET-FILENAME-HERE")
#sh2 = gc.open_by_key('YOUR_KEY_HERE') <<< I'd recommend doing it using open_by_key to avoid filename conflicts.
 

def main():
    '''
    The main function (deployed on Heroku!). Updates a public Google Sheet with data pulled from
    both an internal database, and a database of Google Form responses.

    Parameters:
            None

    Returns:
            None
    '''
    while True:
        df = makeDf(sh2)
        pub_df = convertToPub(df)
        form_df = getFormDf(sh2)
        result = getResult(pub_df, form_df)
        updateSheet(sh, result)
        bolden(sh)
        updateTime()
        #drawArt(sh, a, 0)
        #drawArt(sh, c, 12)
        time.sleep(60)


def getResult(pub_df, form_df):
    '''
    Returns the row-wise combination of the current, public database and the internal Google Form database.

    Parameters:
            pub_df  (DataFrame): The dataframe of published hours.
            form_df (DataFrame): The dataframe of Google Form responses.

    Returns:
            result  (DataFrame): The dataframe of form_df appended to pub_df.
    '''
    df = pub_df.append(form_df)
    mask = df["Name"].str.contains(",")
    df.loc[mask, "Name"] = df.loc[mask, "Name"].str.split(", ").apply(reversed).str.join(" ")
    df = df.groupby(['Name'], as_index=False).agg(sum)
    return df
    
def getFormDf(sheet):
    '''
    Returns a dataframe compiled from the Google Form responses.
    
    Parameters:
            sheet      (object): A Google Sheet, abstracted by gc.

    Returns:
            df2 (DataFrame): The converted Google Sheet.
    '''
    df = pd.DataFrame(sheet.get_worksheet(0).get_all_records())[["Name", "Hours Worked", "Col1"]]
    df["Col1"] = df["Col1"].apply(lambda x : pd.to_numeric(x, errors='coerce'))
    df["Hours Worked"] = df["Hours Worked"].apply(lambda x : pd.to_numeric(x, errors='coerce'))
    df = df.fillna(0)
    df["Hours Worked"] = df["Hours Worked"] + df["Col1"]
    df = df.drop(columns=["Col1"])
    df.columns = ["Name", "Hours Rewarded"]
    mask = df["Name"].str.contains(",")
    df.loc[mask, "Name"] = df.loc[mask, "Name"].str.split(", ").apply(reversed).str.join(" ")
    df = df.groupby(['Name'], as_index=False).sum()
    return df


def makeDf(sheet):
    '''
    Returns a dataframe made from a Google Sheet.

    Parameters:
            sheet (object): A Google Sheet, abstracted by gc.

    Returns:
            df (DataFrame): A DataFrame created from sheet.
    '''
    df = pd.DataFrame(sheet.get_worksheet(1).get_all_records())
    df = df.drop(columns=['HI Project']).groupby(['Name'], as_index=False).agg(sum)
    return df 

def updateTime():
    '''
    Updates the published Google Sheet with the current time (PST).

    Parameters:
            None

    Returns:
            None
    '''
    now = datetime.now(pacific)
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    sh.sheet1.update('C1', 'Last updated: ' + date_time)

def updateSheet(sheet, result):
    '''
    Updates the published Google Sheet from the Google Form responses.

    Parameters:
            sheet (object): A Google Sheet, abstracted by gc.
        result (DataFrame): The most up-to-date database, created by combining the published Google Sheet
                            and the Google Form response sheet.

    Returns:
           None                
    '''
    sheet.sheet1.batch_clear(["A2:A141", "B2:B141"])
    sheet.sheet1.update([result.columns.values.tolist()] + result.values.tolist())

def bolden(sheet):
    ''' 
    Converts the top-most row of the published Google Sheet to boldface.

    Parameters:
            None

    Returns:
            None
    '''
    sheet.sheet1.format('A1:C1', {'textFormat': {'bold': True}})

def convertToPub(df):
    '''
    Converts a dataframe to the format used for publishing.

    Parameters:
            df (DataFrame): A dataframe

    Returns:
            df (DataFrame): The filtered version of df
    '''
    return df[['Name', 'Hours Rewarded']]
  
        
def drawArt(sheet, art, idx):
    '''
    Takes in an string and prints it out in the "Art Zone" of the published Google Sheet
    
    Parameters:
       sheet (object): A Google Sheet, abstracted by gc
            art (str): A string of "art", such as ASCII art
            
    Returns:
            None
    '''
    worksheet = sheet.get_worksheet(0)
    currArt = art.splitlines()
    for k in range(1, len(currArt)):
        worksheet.update('E' + str(k+idx), currArt[k])
    

if __name__ == '__main__':
    main()
