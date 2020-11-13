"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(isp_gdp.csv, newline='') as csvfile:
      csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar = quote)
      for row in csvreader:
        rowid = row[keyfield]
        table[rowid] = row
    return table



def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    results = []
    for year, gdp in gdpdata.items():
      try:
        num_gdp = float(gdp)
        num_year = int(year)
      except ValueError:
        continue
      if num_year >= gdpinfo.get('min_year') and num_year <= gdpinfo.get('max_year'):
        results.append((num_year, num_gdp))

    results.sort()
    return results


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    table = read_csv_as_nested_dict(gdpinfo.get('gdpfile'),
                                    gdpinfo.get("country_name"),
                                    gdpinfo.get("separator"),
                                    gdpinfo.get('quote'))
    country_gdp_by_year = {}

    for country in country_list:
      gdp_row = table.get(country)
      gdp_years = {}

      if gdp_row is not None:
        for year in range(gdpinfo.get('min_year'), gdpinfo.get('max_year')+1):
          gdp_years[year] = gdp_row.get(str(year))

      gdp_by_year = build_plot_values(gdpinfo, gdp_years)
      country_gdp_by_year[country] = gdp_by_year

    return country_gdp_by_year


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    
    data = build_plot_dict(gdpinfo, country_list)

    x_label = 'Year'
    y_label = 'GDP in USD'
    header = "World Bank GDP from 1960 to 2015"
    chart = pygal.XY(title = header, x_title = x_label, y_title = y_label)

    for country in country_list:
      chart.add(country, data.get(country))
    
    chart.render_in_browser()
    
    return


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

test_render_xy_plot()
