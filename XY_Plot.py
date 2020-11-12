#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 17:56:32 2020
@author: Shiva P. 
"""

"""
Code to read World Bank GDP data and create some basic XY plots.
"""

import math
import csv
import pygal
import re #make our life easier 


def read_csv_as_nested_dict(isp_gdp, keyfield, separator, quote):
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
    with open(isp_gdp) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
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
    maxyr = gdpinfo['max_year'] 
    minyr = gdpinfo['min_year']
    outer = [] 
    inner = () 
    gdp = {} 
    
    for dic in gdpdata:
        try:
            key = int(dic)
        except ValueError:
            continue
        try:
            gdp[key] = float(gdpdata[dic])
        except ValueError:
            continue
        if gdpdata[dic] == '' or gdpdata[dic] == "":
            continue
        if float(gdpdata[dic]) < 0:
            continue

    gdpsorted=sorted(gdp.items(),key=lambda t:t[0])
    
    for tup in gdpsorted:
        #check again for empty value
        if tup[1] == '' or  tup[1] == "":
            continue
        key = tup[0]
        # value of key cannot be outside these bounds
        if (key >= minyr) and (key <= maxyr):
            inner = (key, float(tup[1]))
            outer.append(inner)
    return outer
    

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
    
    datadict = {} 
    gdpdata = {} 
    csvfile = gdpinfo['gdpfile']
    country = gdpinfo['country_name']
    sep = gdpinfo['separator']
    quote = gdpinfo['quote']
    plotdic = read_csv_as_nested_dict(csvfile, country, sep, quote)
    
    for country in country_list:
        if country in plotdic:
            tmp = plotdic[country]
            for dic in tmp:
                try:
                    key = int(dic)
                except ValueError:
                    continue
                gdpdata[key] = tmp[dic]
            value = build_plot_values(gdpinfo, gdpdata)
            gdpdata = {}
            datadict[country] = value
        else:
            datadict[country] = []
    return datadict
    
   
       
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
    
    xyplot = pygal.XY(height=400)
    xyplot.title = "GDP of World Bank Countries 1960-2015"
    xydata = build_plot_dict(gdpinfo, country_list)
    for country in xydata:
        xyplot.add(country, xydata[country])
    xyplot.render_to_file(plot_file) 


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


test_render_xy_plot()