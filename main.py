import scrape
from bs4 import BeautifulSoup
from mako.template import Template

import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings


from dotenv import load_dotenv
load_dotenv()

# put this in a class or module


def get_met_office():
    """Get forecast for today"""
    raw_html = scrape.simple_get('https://www.metoffice.gov.uk/weather/forecast/gcqqnw58n')
    soup = BeautifulSoup(raw_html, 'html.parser')
    tab_today = soup.find(id="tabDay0")
    # the first a is pretty much what we want
    a_today = tab_today.find('a')

    str_today = str(a_today)

    # DRY this up
    max_start = str_today.find('Maximum daytime temperature: ')  # check for -1
    max_finish = str_today.find('C;', max_start) + 1  # check for -1

    min_start = str_today.find('Minimum nighttime temperature: ')  # check for -1
    min_finish = str_today.find('C.', min_start) + 1

    max_text = str_today[max_start:max_finish]
    min_text = str_today[min_start:min_finish]

    # text after that and stop at Sunrise
    str_sunrise = str_today.find('Sunrise')  # check for -1
    overview_text = str_today[min_finish + 1:str_sunrise]

    return {
        'met_min': min_text,
        'met_max': max_text,
        'met_summary': overview_text,
    }


def get_bbc():
    """Get forecast for today"""
    raw_html = scrape.simple_get('https://www.bbc.co.uk/weather/2655708')
    soup = BeautifulSoup(raw_html, 'html.parser')

    tab_today = soup.find(id="daylink-0")
    day_body = tab_today.find('div', class_='wr-day__body')

    description = day_body.find('div', class_='wr-day__details__weather-type-description').text

    min_temp = day_body.find('div', class_='wr-day-temperature__low').text
    max_temp = day_body.find('div', class_='wr-day-temperature__high').text

    return {
        'bbc_min': min_temp,
        'bbc_max': max_temp,
        'bbc_summary': description,
    }


def populate_template(dict_variables, results_template):
    """Render the template with the variables"""
    filled_template = results_template.render(**dict_variables)

    # Create a file:
    file_name = "populated.html"
    file = open(file_name, "w+")
    file.write(filled_template)
    file.close()


def upload_azure():
    """
    Upload to Azure using FTP
    https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/storage/azure-storage-blob/azure/storage/blob/_blob_client.py#L375
    """

    az_key = os.getenv("AZ_STORAGE_KEY")
    az_string = os.getenv("AZ_STORAGE_CONNECTION_STRING")
    container_name = '$web'
    local_file_name = 'index.html'

    try:
        print("Azure Blob storage v12 - Python quickstart sample")

        blob_service_client = BlobServiceClient.from_connection_string(az_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
        print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)
        my_content_settings = ContentSettings(content_type='text/html')

        with open('populated.html', "rb") as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=my_content_settings)

    except Exception as ex:
        print('Exception:')
        print(ex)


def main():
    results_template = Template(filename='templates/results.html')

    dict_met = get_met_office()
    dict_bbc = get_bbc()

    all_variables = {**dict_met, **dict_bbc}
    populate_template(all_variables, results_template)

    upload_azure()


main()
