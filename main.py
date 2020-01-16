import weather_scrape
import templater
import azure_uploader
import winsound

from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


def main():
    """
    Scrape the weather data.
    Populate the template.
    Upload to Azure.
    """
    dict_met = weather_scrape.get_met_office()
    dict_bbc = weather_scrape.get_bbc()
    now = datetime.now()
    updated_at = {'updated_at': now.strftime("%b %d %Y %H:%M:%S") }

    all_variables = {**dict_met, **dict_bbc, **updated_at}

    templater.populate_template(all_variables, 'templates/results.html')
    azure_uploader.upload('index.html')

    winsound.Beep(2500, 100)


main()
