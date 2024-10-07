import pandas as pd
import numpy as np
import json
import requests
from bs4 import BeautifulSoup as bs

systems = {}
df = pd.read_csv(r"C:\Users\USER\Desktop\Spaceapps\python\PS_2024.10.05_16.25.57.csv")
print(df)
for index, row in df.iterrows():
    if row["hostname"] not in systems:
        if row["st_lum"] == 0 or row["st_logg"] == 0 or row["st_met"] == 0:
            continue
        
        print(row["hostname"])
        
        # Scrape Kyoto
        try:
            kyoto_URL = "https://www.exoplanetkyoto.org/exohtml/" + row["hostname"].replace(" ","_") + ".html"
            print(kyoto_URL)
            r = requests.get(kyoto_URL)
            if r.status_code == 404:
                print("No Page. Because the Japaneese are stupid")
                continue

            # Sanitize and get all of the details
            soup= bs(r.text, "html.parser")

            # First table. 
            first_image = "https://www.exoplanetkyoto.org/exohtml/" + soup.find("table").findChild().findChildren()[1].findChild()["src"][1:][1:]
            print(first_image)
            img_data = requests.get(first_image).content

            # Second table.
            dist = float(soup.find_all("table")[1].findChildren()[8].string)
            mag1 = float(soup.find_all("table")[1].findChildren()[32].string)
            spectral_type = soup.find_all("table")[1].findChildren()[26].string
            metallicity = float(soup.find_all("table")[1].findChildren()[29].string)
            mag2 = float(soup.find_all("table")[1].findChildren()[35].string)
            RA = float(soup.find_all("table")[1].findChildren()[38].string)
            declination = float(soup.find_all("table")[1].findChildren()[41].string)
            mass_sun = float(soup.find_all("table")[1].findChildren()[22].string)

            # scrape the second kyoto
            kyoto_2_URL= "https://www.exoplanetkyoto.org/exohtml/" + row["pl_name"].replace(" ","_") + ".html"
            print(kyoto_2_URL)
            r2 = requests.get(kyoto_2_URL)
            planet_image = ""
            if r2.status_code != 404:
                # Sanitize and get all of the details
                soup_2 = bs(r2.text, "html.parser")

                # First table. 
                planet_image = "https://www.exoplanetkyoto.org/exohtml/" + soup_2.find("table").findChild().findChildren()[1].findChild()["src"][1:][1:]

                # Second table
                size = soup_2.find_all("table")[1].findChildren()[72].string
                eccentricity = float(soup_2.find_all("table")[1].findChildren()[29].string)
                gravity = float(soup_2.find_all("table")[1].findChildren()[41].string)
                axis = float(soup_2.find_all("table")[1].findChildren()[23].string)
                rad_jup = float(soup_2.find_all("table")[1].findChildren()[11].string)
                mass_jup = float(soup_2.find_all("table")[1].findChildren()[17].string)


            systems[row["hostname"]] = {
                row["pl_name"] : {
                    "pl_orbper" : row["pl_orbper"],
                    "pl_rade" : row["pl_rade"],
                    "pl_bmasse" : row["pl_bmasse"],
                    "pl_orbeccen" : row["pl_orbeccen"], 
                    "pl_image" : planet_image,
                    "pl_eccentricity" : eccentricity,
                    "pl_grav" : gravity,
                    "pl_rad_jup" : rad_jup,
                    "pl_mass_jup" : mass_jup,
                    "pl_size" : size
                },
                "img" : first_image,
                "st_mag_1" : mag1,
                "st_mag_2" : mag2,
                "st_declination" : declination,
                "st_RA" : RA,
                "st_spectraltype" : spectral_type,
                "st_teff" : row["st_teff"],
                "st_rad" : row["st_rad"],
                "st_mass" : row["st_mass"],
                "st_met" : row["st_met"],
                "st_met_2" : metallicity,
                "st_sun_mass" : mass_sun,
                "st_logg" : row["st_logg"],
                "st_lum" : row["st_lum"],
                "st_dist" : dist
            }
            print("broski is a W")

        except Exception as e:
            print(e)
            continue   
    else:
        # scrape the second kyoto
        kyoto_2_URL= "https://www.exoplanetkyoto.org/exohtml/" + row["pl_name"].replace(" ","_") + ".html"
        print(kyoto_2_URL)
        r2 = requests.get(kyoto_2_URL)
        planet_image = ""
        if r2.status_code != 404:
            # Sanitize and get all of the details
            soup_2 = bs(r2.text, "html.parser")

            # First table. 
            planet_image = "https://www.exoplanetkyoto.org/exohtml/" + soup_2.find("table").findChild().findChildren()[1].findChild()["src"][1:][1:]

            # Second table
            size = soup_2.find_all("table")[1].findChildren()[72].string
            eccentricity = float(soup_2.find_all("table")[1].findChildren()[29].string)
            gravity = float(soup_2.find_all("table")[1].findChildren()[41].string)
            axis = float(soup_2.find_all("table")[1].findChildren()[23].string)
            rad_jup = float(soup_2.find_all("table")[1].findChildren()[11].string)
            mass_jup = float(soup_2.find_all("table")[1].findChildren()[17].string)


        systems[row["hostname"]][row["pl_name"]] = {
            "pl_orbper" : row["pl_orbper"],
            "pl_rade" : row["pl_rade"],
            "pl_bmasse" : row["pl_bmasse"],
            "pl_orbeccen" : row["pl_orbeccen"], 
            "pl_image" : planet_image,
            "pl_eccentricity" : eccentricity,
            "pl_grav" : gravity,
            "pl_rad_jup" : rad_jup,
            "pl_mass_jup" : mass_jup,
            "pl_size" : size
        }

        print("broski is an acc W")
json.dump(systems,open("data-new-2.json","w+"))