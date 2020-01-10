# https://realpython.com/python-web-scraping-practical-introduction/

import scrape
from bs4 import BeautifulSoup
from mako.template import Template

#put this in a class or module


def get_met_office():
    """Get forecast for today"""
    raw_html = scrape.simple_get('https://www.metoffice.gov.uk/weather/forecast/gcty0kf9v')
    soup = BeautifulSoup(raw_html, 'html.parser')
    tab_today = soup.find(id="tabDay0")
    # the first a is pretty much what we want
    a_today = tab_today.find('a')

    str_today = str(a_today)

    #DRY this up
    max_start = str_today.find('Maximum daytime temperature: ')  # check for -1
    max_finish = str_today.find('C;', max_start) + 1  # check for -1

    min_start = str_today.find('Minimum nighttime temperature: ')  # check for -1
    min_finish = str_today.find('C.', min_start)+1

    max_text = str_today[max_start:max_finish]
    min_text = str_today[min_start:min_finish]

    # text after that and stop at Sunrise
    str_sunrise = str_today.find('Sunrise')  # check for -1
    overview_text = str_today[min_finish+1:str_sunrise]

    return {
        'met_min': min_text,
        'met_max': max_text,
        'met_summary': overview_text,
    }


def populate_template(dict_variables,results_template):
    """Render the template with the variables"""
    print(results_template.render(**dict_variables))


def main():
    results_template = Template(filename='templates/results.html')

    dict_variables = get_met_office()
    populate_template(dict_variables, results_template)




main()



