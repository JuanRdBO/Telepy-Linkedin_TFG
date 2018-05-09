#!/usr/bin/env python
# -*- coding: utf-8 -*-

from linkedin import linkedin
import sys
import argparse
import json
from optparse import OptionParser
import os
import errno
import pandas as pd
import webbrowser
import csv
from pathlib import Path
import glob
import io
import codecs
import re

import pandas as pd
import json
import time

import warnings
import numpy as np


start = time.time()

from renew_token.access_token import ACCESS_TOKEN

parser = OptionParser()
(options, args) = parser.parse_args()

warnings.simplefilter(action='ignore', category=FutureWarning)


# print(args)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALICS = '\x1B[3m'
    UNDERLINE = '\033[4m'




def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval


class TELEPY:
    # def __init__(self, token):
    # 	self.token = token
    # Se define el access token para Telepy_2

    def retrieve_json(self, token, company, starting_point, count, query_type):

        token_juan = ACCESS_TOKEN(token)
        token_juan.read_csv(token)
        # print('Access Token: '+token_juan.read_csv(token)+'\n\n')
        self.application = linkedin.LinkedInApplication(token=token_juan.read_csv(token))

        if query_type == "by_location":
            print_json = self.application.search_company(selectors=[{'companies': ['id', 'name', 'email-domains',
                                                                                   'company-type', 'website-url',
                                                                                   'industries', 'status', 'twitter-id',
                                                                                   'employee-count-range',
                                                                                   'locations:(is-headquarters,is-active,address,contact-info)',
                                                                                   'founded-year', 'end-year',
                                                                                   'num-followers', 'specialties']}],
                                                         params={'facet': 'location,' + company,
                                                                 'start': starting_point, 'count': count})
        elif query_type == "by_name":
            print_json = self.application.search_company(selectors=[{'companies': ['id', 'name', 'email-domains',
                                                                                   'company-type', 'website-url',
                                                                                   'industries', 'status', 'twitter-id',
                                                                                   'employee-count-range',
                                                                                   'locations:(is-headquarters,is-active,address,contact-info)',
                                                                                   'founded-year', 'end-year',
                                                                                   'num-followers', 'specialties']}],
                                                         params={'keywords': company, 'start': starting_point,
                                                                 'count': count})

        return json.dumps(print_json, sort_keys=True, indent=4, separators=(',', ': '))

    def save_to_json(self, name, json_text):
        if '/' in name:
            name = name.replace('/', ':')
        if not os.path.exists(os.path.dirname("output/json/" + name)):
            try:
                os.makedirs(os.path.dirname("output/json/" + name))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open("output/json/" + name, 'w') as f:
            f.write(json_text)
            f.close()

    def convert_to_csv(self):

        if not os.path.exists(os.path.dirname("output/csv/")):
            try:
                os.makedirs(os.path.dirname("output/csv/"))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        json_files = os.listdir("output/json/")
        json_files.sort()
        print(json_files)
        sub = ".json"

        for filename in json_files:
            if sub in filename:
                filename = filename[:-5]
                print(bcolors.OKGREEN + "\nConverting '" + filename + "' to CSV" + bcolors.ENDC)
                command = "python -m libjson2csv.json_2_csv './output/json/" + filename + ".json' './output/csv/" + filename + ".csv'"
                os.system(command)

    @staticmethod
    def natural_keys(text: object) -> object:
        return [atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]

    def unify_all_csv(self):

        if not os.path.exists(os.path.dirname("output/csv/final_company.csv")):
            try:
                os.makedirs(os.path.dirname("output/csv/final_company.csv"))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        csv_files = os.listdir("output/csv/")
        csv_files.sort(key=self.natural_keys)
        print(csv_files)
        sub = ".csv"

        print("\n---------------------------------\n\nUnifying now all CSV files into a big one\n")

        for filename in csv_files:
            if sub in filename:
                if not Path("output/csv/final_company.csv").is_file():
                    company_csv = pd.read_csv("output/csv/" + filename, dtype='unicode')
                    company_csv.to_csv("output/csv/final_company.csv", index=False)
                else:
                    company_csv = pd.read_csv("output/csv/final_company.csv", dtype='unicode')
                    pandas_csv = pd.read_csv("output/csv/" + filename, dtype='unicode')
                    concat_csv = [company_csv, pandas_csv]
                    final_company = pd.concat(concat_csv)
                    final_company.to_csv("output/csv/final_company.csv", index=False)
            print("Unified file " + filename, end="\r")
        print("\nFinished unifying all csv files to: 'final_company.csv'")


    def read_source_csv(self):
        df = pd.read_csv('sample_input.csv', index_col=False)
        rows = len(df.index)
        return df, rows

    def read_initial_json(self, company_input):
        if '/' in company_input:
            company_input = company_input.replace('/', ':')
        with open('output/json/' + company_input + '.json') as f:
            total_matches = json.load(f)
        return int(total_matches["companies"]["_total"])

    def unify_companies(self, df, rows):
        for company in range(0,rows):
            if df.iloc[company][1] > 0:
                for match in range(0, df.iloc[company][1]+1):
                    if not Path("output/csv/" + df.iloc[company][0] +"_FINAL.csv").is_file():
                        company_csv = pd.read_csv("output/csv/" + df.iloc[company][0] + "(" + str(match) + ").csv", dtype='unicode')
                        company_csv.to_csv("output/csv/" + df.iloc[company][0] +"_FINAL.csv", index=False)
                    else:
                        company_csv = pd.read_csv("output/csv/" + df.iloc[company][0] +"_FINAL.csv", dtype='unicode')
                        pandas_csv = pd.read_csv("output/csv/" + df.iloc[company][0] + "(" + str(match) + ").csv", dtype='unicode')
                        concat_csv = [company_csv, pandas_csv]
                        final_company = pd.concat(concat_csv)
                        final_company.to_csv("output/csv/" + df.iloc[company][0] +"_FINAL.csv", index=False)
                    os.remove("output/csv/" + df.iloc[company][0] + "(" + str(match) + ").csv")

    def remove_location_cols(self, loc_to_keep):
        final_company = pd.read_csv("output/csv/final_company.csv", dtype='unicode')

        last_cols = 0
        for col in final_company.columns:
            if 'locations.values' in col:
                if int(col.split(".")[3].split("[")[1].split("]")[0]) > last_cols:
                    last_cols = int(col.split(".")[3].split("[")[1].split("]")[0])
        print("Number of values: ",last_cols)

        values = last_cols
        for values in range(loc_to_keep,values+1):
            for col in final_company.columns:
                if 'locations.values[' + str(values) + ']' in col:
                    final_company = final_company.drop(col, 1)
        final_company.to_csv("output/csv/final_company.csv", index=False)

    def read_postal_codes(self, country):
        if country == "de":
            postal_codes = pd.read_csv("postalCodes/de_postal_codes.csv", encoding='latin-1')
            return postal_codes


# work in progress
    def erase_unwanted_headquarters(self, postal_codes):

        postal_codes = postal_codes.replace(np.nan, "*", regex=True)
        final_company = pd.read_csv("output/csv/final_company.csv", dtype='unicode').replace(np.nan, "N/A", regex=True)
        rows = len(final_company.index)

        # How many locations are there?
        last_cols = 0
        # Which names do the columns have?
        postCode_location_cols = []
        city_location_cols = []
        # Which index do they have?
        postCode_index_cols = []
        city_index_cols = []
        index_counter = 0
        for col in final_company.columns:
            if 'locations.values' and 'postalCode' in col:
                if int(col.split(".")[3].split("[")[1].split("]")[0]) > last_cols:
                    last_cols = int(col.split(".")[3].split("[")[1].split("]")[0])
                postCode_location_cols.append(col)
                postCode_index_cols.append(index_counter)
            if 'locations.values' and 'city' in col:
                city_location_cols.append(col)
                city_index_cols.append(index_counter)
            index_counter+=1
        print("Number of postcode values: ", last_cols)
        print('Postcode:',postCode_location_cols)
        print('Postcode:',postCode_index_cols)
        print('City:', city_location_cols)
        print('City:',city_index_cols)
        # implement condition if GER
        # drop rows: df.drop(df.index[[1,3]])

        verified_index_postalCode = []
        for row in range(0, rows):
            for index in postCode_index_cols:
                #print('\nchecking row:',row,'and col:',index,':[',type(final_company.loc[row][index]),final_company.loc[row][index],']->',final_company.loc[row][index] in postal_codes['Postal Code'].unique())
                if float(final_company.loc[row][index].split('-')[0].split(' ')[0]) if not re.search('[a-zA-Z]', final_company.loc[row][index]) else float(0) in postal_codes['Postal Code'].unique():
                    verified_index_postalCode.append([row, index])
        print('\nCould verify the following locations through postal code:', verified_index_postalCode)

        verified_index_city = []
        for row in range(0, rows):
            for index in city_index_cols:
                #print('checking row:',row,'and col:',index,':[',type(final_company.loc[row][index]),final_company.loc[row][index],']->',len(postal_codes[postal_codes['Place Name'].str.contains(final_company.loc[row][index])]) > 0)
                if len(postal_codes[postal_codes['Place Name'].str.contains(final_company.loc[row][index])]) > 0:
                    verified_index_city.append([row, index])
        print('\nCould verify the following locations through city:', verified_index_city)

        total_german_companies = verified_index_postalCode.extend(verified_index_city)


        # Append those two lists
        print('\nAll german locations:', total_german_companies)

        #Establish row-dropping

        


        # # if not a match
        # # Removes location columns from a locations list
        # print(postCode_location_cols)
        # for locations in postCode_location_cols:
        #     if "locations.values[1]" in locations:
        #         postCode_location_cols.remove(locations)
        # print(postCode_location_cols)
        #
        #
        # # Values = number of locations
        # values = last_cols
        # for values in range(0, values + 1):
        #     index = 0
        #     for col in final_company.columns:
        #         if 'locations.values[' + str(values) + '].address.postalCode' in col:
        #             pass
        #         index+=1






TELEPY: TELEPY = TELEPY()

df, rows = TELEPY.read_source_csv()
# print("\nNrows:",rows)
app = 1
zero_matches_to_get = []

print(bcolors.HEADER + "\nStarted processing JSON files!" + bcolors.ENDC)
for row in range(0, rows):
    company = df.iloc[row][0]
    starting_point = 0
    matches_to_get = 3
    match = 0
    print('\n----------------------')
    while match < matches_to_get + 1:
        while True:
            try:
                new_search = TELEPY.retrieve_json(app, company, starting_point, 1, 'by_name')

                TELEPY.save_to_json((company + '(' + str(match) + ').json'), new_search)

                if matches_to_get > TELEPY.read_initial_json(company + '(' + str(match) + ')') and match == 0:
                    print("->" + bcolors.ITALICS,
                          'Matches to get reduced ' + bcolors.UNDERLINE + 'from ' + str(matches_to_get) + ' to ' + str(
                              TELEPY.read_initial_json(company + '(' + str(match) + ')')) + bcolors.ENDC)

                    matches_to_get = TELEPY.read_initial_json(company + '(' + str(match) + ')')

                    zero_matches_to_get.append(matches_to_get)
                elif matches_to_get <= TELEPY.read_initial_json(company + '(' + str(match) + ')') and match == 0:
                    matches_to_get = matches_to_get - 1

                    zero_matches_to_get.append(matches_to_get)


                print(bcolors.OKGREEN + str(row) + " - " + company + bcolors.ENDC + ": Processed " + str(
                    starting_point + 1) + " of " + str(matches_to_get + 1) + " JSON files",
                      end='\n----------------------\n' if (row == rows - 1 and match == matches_to_get) else '\r')

                starting_point += 1
                match += 1
            except Exception as e:
                app = app + 1
                print(e)
                print("\n--------------------\n\nTrying app " + str(app) + ": \n")
                if app == 250:
                    print('\n\n--> No more apps from which to source of. Aborting.')
                    app = 1
                continue
            break

df['matches (starting at 0)'] = zero_matches_to_get
print(df)

print(bcolors.WARNING + '\nIt took', "{0:.2f}".format(time.time() - start), 'seconds to fetch',
      len(os.listdir("output/json/")), 'JSON files, from which', len((df['matches (starting at 0)'] == 0).unique().astype(int))-1, 'are empty\n', bcolors.ENDC)

TELEPY.convert_to_csv()

TELEPY.unify_companies(df, rows)

TELEPY.unify_all_csv()

postal_codes = TELEPY.read_postal_codes("de")

TELEPY.erase_unwanted_headquarters(postal_codes)


# This only when I got all three locations from country (loc_to_keep)
#TELEPY.remove_location_cols(3)
