import requests
import pandas as pd
import numpy as np


def gdp():

    """Get GPD Data from the WorldBank API"""
    #id,br,ke,gh,ng
    country="za;chn;us;ru;ke;gh;ng"
    indicator="NY.GDP.MKTP.CD"

    url="https://api.worldbank.org/v2/country/"+country+"/indicator/"+indicator

    parameters={

        'format':'json',
        'per_page':441,

    }

    response = requests.get(url, params=parameters)
    response.raise_for_status()
    data = response.json()

    country_values=data[1]

    all_data=[]
    for value in country_values:
        country_name=value['country']['value']
        date=value['date']
        gdp=value['value']
        all_data.append((country_name,date,gdp))
    result=pd.DataFrame(all_data,columns=['Country','Date','GDP'])
    result['Date'] = result['Date'].astype('datetime64[ns]').dt.year
    result['Country'].replace("Russian Federation",'Russia',inplace=True)

    #when you return result and call function it will print the results
    return result


gdp_data=gdp()




def gdp_pp_employed():

    """GDP Per Person Employed for the latest year available"""

    country="za;chn;us;ru;ke;gh;ng"
    indicator="SL.GDP.PCAP.EM.KD"

    url="https://api.worldbank.org/v2/country/"+country+"/indicator/"+indicator


    parameters={

        'format':'json',
        'per_page':441,

    }

    response = requests.get(url, params=parameters)
    response.raise_for_status()
    data = response.json()

    country_values=data[1]


    all_data=[]
    for value in country_values:
            country_name=value['country']['value']
            date=value['date']
            gdp_person=value['value']
            all_data.append((country_name,date,gdp_person))

    result=pd.DataFrame(all_data,columns=['Country','Date','GDP pp Employed'])
    result["GDP pp Employed"] =  result["GDP pp Employed"] .replace(np.nan, 0)
    result['Date'] = result['Date'].astype('datetime64[ns]').dt.year
    result=result.sort_values(['Country', 'Date']).drop_duplicates('Country', keep='last')
    result['Country'].replace("Russian Federation",'Russia',inplace=True)

    return result


gdp_pp=gdp_pp_employed()







