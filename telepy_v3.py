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
import shutil
from pathlib import Path
import glob
import io
import codecs
import re
import humanfriendly

import pandas as pd
import json
import time

import telegram
import socket
import warnings
import numpy as np
import threading

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
    #   self.token = token
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

    def convert_to_csv(self, json_files, threadName):

        if not os.path.exists(os.path.dirname("output/csv/")):
            try:
                os.makedirs(os.path.dirname("output/csv/"))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        #json_files = os.listdir("output/json/")
        json_files.sort()
        #print(json_files)
        sub = ".json"

        for filename in json_files:
            if sub in filename:
                filename = filename[:-5]
                print(bcolors.OKGREEN + "\n"+threadName+" - Converting '" + filename + "' to CSV" + bcolors.ENDC)
                command = "python -m libjson2csv.json_2_csv './output/json/" + filename + ".json' './output/csv/" + filename + ".csv' > /dev/null"
                os.system(command)

                DataFrame_name = pd.read_csv('output/csv/' + filename + '.csv', dtype='unicode')
                DataFrame_name.insert(loc = 0, column = 'Queried Name', value = re.sub(r'\([^)]*\)', '', filename))
                DataFrame_name.to_csv('output/csv/' + filename + '.csv', index = False)
                csv_files_list.append('output/csv/' + filename + '.csv')

    @staticmethod
    def natural_keys(text: object) -> object:
        return [atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]

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
        for company in range(0, rows):
            if df.iloc[company][1] > 0:
                for match in range(0, df.iloc[company][1] + 1):
                    if not Path("output/csv/" + df.iloc[company][0] + "_FINAL.csv").is_file():
                        company_csv = pd.read_csv("output/csv/" + df.iloc[company][0] + "(" + str(match) + ").csv",
                                                  dtype='unicode')
                        company_csv.to_csv("output/csv/" + df.iloc[company][0] + "_FINAL.csv", index=False)
                    else:
                        company_csv = pd.read_csv("output/csv/" + df.iloc[company][0] + "_FINAL.csv", dtype='unicode')
                        pandas_csv = pd.read_csv("output/csv/" + df.iloc[company][0] + "(" + str(match) + ").csv",
                                                 dtype='unicode')
                        concat_csv = [company_csv, pandas_csv]
                        final_company = pd.concat(concat_csv)
                        final_company.to_csv("output/csv/" + df.iloc[company][0] + "_FINAL.csv", index=False)
                    os.remove("output/csv/" + df.iloc[company][0] + "(" + str(match) + ").csv")

    def remove_location_cols(self, loc_to_keep):
        final_company = pd.read_csv("output/csv/final_company.csv", dtype='unicode')

        last_cols = 0
        for col in final_company.columns:
            if 'locations.values' in col:
                if int(col.split(".")[3].split("[")[1].split("]")[0]) > last_cols:
                    last_cols = int(col.split(".")[3].split("[")[1].split("]")[0])
        print("Number of values: ", last_cols)

        values = last_cols
        for values in range(loc_to_keep, values + 1):
            for col in final_company.columns:
                if 'locations.values[' + str(values) + ']' in col:
                    final_company = final_company.drop(col, 1)
        final_company.to_csv("output/csv/final_company.csv", index=False)

    def read_postal_codes(self, country):
        if country == "de":
            postal_codes = pd.read_csv("postalCodes/de_postal_codes.csv", encoding='latin-1')
            return postal_codes['Place Name']
        if country == "ar":
            postal_codes = pd.read_csv("postalCodes/ar_postal_codes.csv", encoding='latin-1')
            return postal_codes['Place Name']
        if country == "pe":
            postal_codes = pd.read_csv("postalCodes/Distritos.csv", encoding = "latin-1", sep=";")
            return postal_codes['NOMBDIST']

    
    
    def doQuery(self, app_, rows_, starting_point_, matches_to_get_, match_, threadname, df):
        app = app_
        zero_matches_to_get = []

        json_files = []
        print(bcolors.HEADER + "\nStarted processing JSON files!" + bcolors.ENDC)
        for row in range(0, rows_):
            company = df.iloc[row][0]
            starting_point = starting_point_
            matches_to_get = matches_to_get_
            match = match_
            print('\n----------------------')
            while match < matches_to_get + 1:
                while True:
                    try:
                        new_search = TELEPY.retrieve_json(app, company, starting_point, 1, 'by_name')

                        TELEPY.save_to_json((company + '(' + str(match) + ').json'), new_search)

                        json_files.append(company + '(' + str(match) + ').json')

                        if matches_to_get > TELEPY.read_initial_json(company + '(' + str(match) + ')') and match == 0:
                            print("->" + bcolors.ITALICS,
                                  'Matches to get reduced ' + bcolors.UNDERLINE + 'from ' + str(matches_to_get) + ' to ' + str(
                                      TELEPY.read_initial_json(company + '(' + str(match) + ')')) + bcolors.ENDC)

                            matches_to_get = TELEPY.read_initial_json(company + '(' + str(match) + ')')

                            zero_matches_to_get.append(matches_to_get)
                        elif matches_to_get <= TELEPY.read_initial_json(company + '(' + str(match) + ')') and match == 0:
                            matches_to_get = matches_to_get - 1

                            zero_matches_to_get.append(matches_to_get)

                        print(bcolors.OKGREEN +threadname+ ": "+ str(row) + " - " + company + bcolors.ENDC + ": Processed " + str(
                            starting_point + 1) + " of " + str(matches_to_get + 1) + " JSON files",
                              end='\n----------------------\n' if (row == rows_ - 1 and match == matches_to_get) else '\n')

                        starting_point += 1
                        match += 1
                    except Exception as e:
                        app = app + 1
                        print(e)
                        print("\n--------------------\n\nTrying app " + str(app) + ": \n")
                        if app == 550:
                            print('\n\n--> No more apps from which to source of. Aborting.')
                            app = 251
                        continue
                    break

        df['matches (starting at 0)'] = zero_matches_to_get
        return df, json_files
        #print(df)

    def drop_duplicates(self):
        with open("./sample_input.csv", encoding='latin-1') as infile, open("outfile.csv", "w") as outfile:
            for line in infile:
                outfile.write(line.replace(",", ""))
        os.rename("./outfile.csv", "./sample_input.csv")
        try:
            shutil.rmtree("./outfile.csv")
        except:
            pass

        sample_input = pd.read_csv("sample_input.csv")

        sample_input = sample_input.drop_duplicates( keep = 'first')

        sample_input['Company']= sample_input['Company'].str.replace('/',':')
        sample_input['Company']= sample_input['Company'].str.replace("'",' ')
        print("Cleaned input file!\n")

        sample_input.to_csv("./sample_input.csv", index=False)

    def unify_all_csv(self):

        if not os.path.exists(os.path.dirname("output/csv/final_company.csv")):
            try:
                os.makedirs(os.path.dirname("output/csv/final_company.csv"))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise


        #csv_files = os.listdir("output/csv/")
        #csv_files.sort(key=self.natural_keys)
        #print(csv_files)
        sub = ".csv"

        while True:

            if len(csv_files_list) > 0:

                csv_files = csv_files.extend(csv_files_list)
                csv_files_list.clear()

                print("\n---------------------------------\n\nUnifying now all CSV files into a big one\n")

                csv_unifier_index = 0
                company_csv = pd.DataFrame()
                final_company = pd.DataFrame()
                for filename in csv_files:
                    if sub in filename:
                        if not Path("output/csv/final_company.csv").is_file():
                            final_company = pd.read_csv("output/csv/" + filename, dtype='unicode')
                            final_company.to_csv("output/csv/final_company.csv", index=False)
                        else:
                            #company_csv = pd.read_csv("output/csv/final_company.csv", dtype='unicode')
                            pandas_csv = pd.read_csv("output/csv/" + filename, dtype='unicode')
                            concat_csv = [final_company, pandas_csv]
                            final_company = pd.concat(concat_csv)
                            #final_company.to_csv("output/csv/final_company.csv", index=False)
                        print("Unified file " + str(csv_unifier_index+1)+ " of "+str(len(csv_files)), end="\r")
                        csv_unifier_index+=1
                final_company.to_csv("output/csv/final_company.csv", index=False)                
                #print("\nFinished unifying all csv files to: 'final_company.csv'")

    def erase_unwanted_headquarters(self, postal_codes, final_company, threadName):        

        print(bcolors.HEADER + "\n"+threadName+" - Looking Through locations now!" + bcolors.ENDC)

        postal_codes = postal_codes.replace(np.nan, "*", regex=True)

        
        rows = len(final_company.index)

        col_completion_index = 0
        for col in final_company.columns:
            if 'locations.values' in col:
                if 'address.street1' in col:
                    if not 'contactInfo.fax' in final_company.columns[final_company.columns.get_loc(col)+1]:
                        #print("Not FAX in column",col_completion_index,'putting',"companies.values[0].locations.values["+col.split(".")[3].split("[")[1].split("]")[0]+"].contactInfo.fax")
                        final_company.insert(loc=final_company.columns.get_loc(col)+1, column="companies.values[0].locations.values["+col.split(".")[3].split("[")[1].split("]")[0]+"].contactInfo.fax",value="N/A")

            col_completion_index+=1

        col_completion_index = 0
        for col in final_company.columns:
            if 'locations.values' in col:
                if 'contactInfo.fax' in col:

                    if not 'contactInfo.phone1' in final_company.columns[final_company.columns.get_loc(col)+1]:
                        #print("Not FAX in column",col_completion_index,'putting',"companies.values[0].locations.values["+col.split(".")[3].split("[")[1].split("]")[0]+"].contactInfo.phone1")
                        final_company.insert(loc=final_company.columns.get_loc(col)+ 1, column="companies.values[0].locations.values["+col.split(".")[3].split("[")[1].split("]")[0]+"].contactInfo.phone1",value="N/A")

            col_completion_index+=1

        #final_company.replace(np.nan, "N/A", regex=True).to_csv("./output/csv/final_company.csv", index=False)

        # How many locations are there?
        last_cols = -1
        # Which names do the columns have?
        postCode_location_cols = []
        city_location_cols = []
        # Which index do they have?
        postCode_index_cols = []
        city_index_cols = []
        index_counter = 0

        location_start = []
        # Since i dont know how to return last location col, i do this
        last_location_col_index = 0

        index_helper = 0

        for col in final_company.columns:            
            if 'locations.values' in col:
                if int(col.split(".")[3].split("[")[1].split("]")[0]) != last_cols:
                    #print(int(col.split(".")[3].split("[")[1].split("]")[0]), last_cols, index_counter)
                    last_cols = int(col.split(".")[3].split("[")[1].split("]")[0])

                    # Puts start/stop on all values except last and the one before that
                    location_start.append([index_counter, 0]);
                    location_start[index_helper - 1][
                        1] = index_counter - 1 if index_helper >= 0 else location_start.append([index_counter, 0])

                    index_helper += 1

                # Gets the endpoint of all locations
                last_location_col_index = index_counter

            if 'locations.values' and 'city' in col:
                city_location_cols.append(col)
                city_index_cols.append(index_counter)
            index_counter += 1

        #print('START:',location_start)

        # Last touches to the start/stop list
        location_start[len(location_start) - 1][1] = last_location_col_index
        location_start[len(location_start) - 2][1] = location_start[len(location_start) - 1][0] - 1

        verified_index_postalCode = []
        verified_index_postalCode_colName = []

        verified_index_city = []
        verified_index_city_colname = []
        counter_feedback = 0
        counter_feedback_total = len(final_company.index) * len(city_index_cols)
        #print(bcolors.OKBLUE, "\nVerifying through named locations (city)", bcolors.ENDC, sep=' ', end='', flush=True)
        #print('\n')
        for row in range(0, rows):
            for index in city_index_cols:
                print(bcolors.OKBLUE+ 'Verifying through named locations (city) : (', counter_feedback,'of', counter_feedback_total,')',bcolors.ENDC,end='\r')
                counter_feedback+=1
                # print('checking row:',row,'and col:',index,':[',type(final_company.loc[row][index]),final_company.loc[row][index],']->',len(postal_codes[postal_codes['Place Name'].str.contains(final_company.loc[row][index])]) > 0)
                if len(postal_codes[postal_codes.str.contains(final_company.loc[row][index])]) > 0:
                    verified_index_city.append([row, index])
                    verified_index_city_colname.append([row, city_location_cols[city_index_cols.index(index)]])
        #print('\n\nCould verify the following locations through city:', verified_index_city)

        total_german_companies_index = sorted(verified_index_postalCode + verified_index_city,
                                              key=lambda element: (element[0], element[1]))

        total_german_companies_colNames = (
                    verified_index_city_colname + verified_index_postalCode_colName)  # .sort(key=self.natural_keys)

        #print('\nAll german locations by index:', total_german_companies_index)
        # print('\nAll german locations by column names:', total_german_companies_colNames)

        # Dataframe using the start/stop list
        location_df = pd.DataFrame()
        location_df['start_location'] = [i[0] for i in location_start]
        location_df['stop_location'] = [i[1] for i in location_start]
        #print('\n', location_df)

        # [item[0] for item in total_german_companies_index]

        companies = []
        companies_index_counter = 0
        i = 0

        ########## Does not get last entry ###########

        while i < len(total_german_companies_index):

           # print('---------->', len(total_german_companies_index))
            location = location_df.loc[(location_df.start_location <= total_german_companies_index[i][1]) & (
                        total_german_companies_index[i][1] <= location_df.stop_location)].index[0]
            #print('Company on row:',total_german_companies_index[i][0],'has match on',location,'meaning on positions:',location_df.start_location[location],'-',location_df.stop_location[location]+1)

            df_1 = final_company.iloc[:, 0:14][total_german_companies_index[i][0]: total_german_companies_index[i][0] + 1]

            #print('Retrieving from', total_german_companies_index[i][0], ':', total_german_companies_index[i][0] + 1)

            #print('COUNT i:', i, 'matches:',[item[0] for item in total_german_companies_index].count(total_german_companies_index[i][0]), '--->',total_german_companies_index)
            if [item[0] for item in total_german_companies_index].count(total_german_companies_index[i][0]) > 1:

                df_helper = []
                counter_helper = 0
                #print('\nDetected',[item[0] for item in total_german_companies_index].count(total_german_companies_index[i][0]),'matches!\n')

                for p in range(i, i + [item[0] for item in total_german_companies_index].count(
                        total_german_companies_index[i][0])):
                    #print('Entered HELPER',i,'---',p-1,p,p+1,'---',[item[0] for item in total_german_companies_index].count(i))

                    location = location_df.loc[(location_df.start_location <= total_german_companies_index[p][1]) & (
                                total_german_companies_index[p][1] <= location_df.stop_location)].index[0]

                    df_helper.append(pd.DataFrame())

                    df_helper[counter_helper] = final_company.iloc[:,location_df.start_location[location]:location_df.stop_location[location]+1][total_german_companies_index[i][0]: total_german_companies_index[i][0] + 1]

                    #print(df_helper[counter_helper])

                    df_helper[counter_helper] = df_helper[counter_helper].rename(columns = {df_helper[counter_helper].columns[0] : "companies.values[0].locations.values["+str(counter_helper)+"].address.city"})
                    df_helper[counter_helper] = df_helper[counter_helper].rename(columns = {df_helper[counter_helper].columns[1] : "companies.values[0].locations.values["+str(counter_helper)+"].address.postalCode"})
                    df_helper[counter_helper] = df_helper[counter_helper].rename(columns = {df_helper[counter_helper].columns[2] : "companies.values[0].locations.values["+str(counter_helper)+"].address.street1"})
                    df_helper[counter_helper] = df_helper[counter_helper].rename(columns = {df_helper[counter_helper].columns[3] : "companies.values[0].locations.values["+str(counter_helper)+"].contactInfo.fax"})
                    df_helper[counter_helper] = df_helper[counter_helper].rename(columns = {df_helper[counter_helper].columns[4] : "companies.values[0].locations.values["+str(counter_helper)+"].contactInfo.phone1"})
                    df_helper[counter_helper] = df_helper[counter_helper].rename(columns = {df_helper[counter_helper].columns[5] : "companies.values[0].locations.values["+str(counter_helper)+"].isActive"})
                    df_helper[counter_helper] = df_helper[counter_helper].rename(columns = {df_helper[counter_helper].columns[6] : "companies.values[0].locations.values["+str(counter_helper)+"].isHeadquarters"})


                    counter_helper += 1

                # for p in range(i, [item[0] for item in total_german_companies_index].count(total_german_companies_index[i][0])-1):
                #     total_german_companies_index.pop(p)

                df_2 = pd.concat([item for item in df_helper], axis=1)

            else:
                df_2 =final_company.iloc[:,location_df.start_location[location]:location_df.stop_location[location]+1][total_german_companies_index[i][0]: total_german_companies_index[i][0] + 1] 
                       

            df_3 = final_company.iloc[:,location_df['stop_location'].iloc[-1]+1 : len(final_company.columns)][total_german_companies_index[i][0]: total_german_companies_index[i][0] + 1]

            companies.append(pd.DataFrame())
            companies[companies_index_counter] = pd.concat([df_1, df_2, df_3], axis=1)
            #print(companies[companies_index_counter])
            companies_index_counter += 1

            if [item[0] for item in total_german_companies_index].count(total_german_companies_index[i][0]) > 1:
                i = i + [item[0] for item in total_german_companies_index].count(total_german_companies_index[i][0])
            else:
                i += 1

        verified_companies = pd.concat([item for item in companies], axis=0)

        df_companyName = verified_companies.pop('companies.values[0].name')

        verified_companies.insert(loc=1, column ='Returned Name', value = df_companyName)

        verified_companies.replace(np.nan, "N/A", regex=True)
        threadLock.acquire()
        if not Path('output/csv/TEST.csv').is_file():
            verified_companies.replace(np.nan, "N/A", regex=True).to_csv('./output/csv/TEST.csv', index=False)                   
        else:
            pandas_csv = pd.read_csv('./output/csv/TEST.csv', dtype='unicode')
            concat_csv = [verified_companies, pandas_csv]
            TEST = pd.concat(concat_csv)
            TEST.to_csv('./output/csv/TEST.csv', index=False)
        threadLock.release()

        #verified_companies.replace(np.nan, "N/A", regex=True).to_csv('./output/csv/TEST.csv', index=False)

        
class mainThread (threading.Thread):
    def __init__(self, threadID, name, counter, nThreads, df, postal_codes, final_company, mode):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.nThreads = nThreads
        self.df = df_input
        self.postal_codes = postal_codes
        self.final_company = final_company
        self.mode = mode
    def run(self):     
        print("Starting " + self.name)
        if self.mode ==1:               
            bot = telegram.Bot(token='544485370:AAGcj3tJlduMprdz3rpVt1Fm-GL7uDGia4Q')
            bot.send_message(chat_id=330239471, text="<b>"+socket.gethostname()+":</b> New search launched. Starting JSON query.", parse_mode=telegram.ParseMode.HTML)
            df_new = df_input[int(self.counter*len(self.df)/self.nThreads):(self.counter+1)*int(len(df_input)/nThreads)].reset_index(drop=True)
            print(df_new) 
            df, json_files = TELEPY.doQuery (251, len(df_new.index), 0, 3, 0, self.name, df_new)   
            print(bcolors.WARNING + '\n'+self.name+' - It took', humanfriendly.format_timespan(time.time() - start), 'seconds to fetch',
                  len(json_files), 'JSON files, from which',
                  len((df['matches (starting at 0)'] == 0).unique().astype(int)- 1), 'are empty\n', bcolors.ENDC)     
            TELEPY.convert_to_csv(json_files, self.name)
        else:            
            final_company = self.final_company[int(self.counter*len(self.final_company)/self.nThreads):(self.counter+1)*int(len(self.final_company)/nThreads)].reset_index(drop=True)
            TELEPY.erase_unwanted_headquarters(postal_codes, final_company, self.name)
        #TELEPY.unify_companies(df, len(df.index))
        print("Exiting " + self.name)

class writerThread (threading.Thread):
    def __init__(self, name, nThreads):
        threading.Thread.__init__(self)
        self.name = name
        self.nThreads = nThreads
    def run(self):   
        # Threading.activeCount() returns 2 if only one thread is active (Main, active)

        if not os.path.exists(os.path.dirname("output/csv/final_company.csv")):
            try:
                os.makedirs(os.path.dirname("output/csv/final_company.csv"))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        final_company = pd.DataFrame()
        while threading.activeCount()-2 > 0:
            if len(csv_files_list) > 0:

                csv_unifier_index = 0
                company_csv = pd.DataFrame()  
                threadLock.acquire()              
                if not Path("output/csv/final_company.csv").is_file():
                    final_company = pd.read_csv(csv_files_list[0], dtype='unicode')
                    final_company.to_csv("output/csv/final_company.csv", index=False)
                    os.remove(csv_files_list[0])
                    csv_files_list.remove(csv_files_list[0])                    
                else:
                    pandas_csv = pd.read_csv(csv_files_list[0], dtype='unicode')
                    concat_csv = [final_company, pandas_csv]
                    final_company = pd.concat(concat_csv)
                    os.remove(csv_files_list[0])
                    csv_files_list.remove(csv_files_list[0])
                threadLock.release()

                #print("Unified file " + str(csv_unifier_index+1)+ " of "+str(len(csv_files_list)), end="\r")
                #csv_unifier_index+=1
                final_company.to_csv("output/csv/final_company.csv", index=False)    
##########

try:
    shutil.rmtree('./output')
    print("Removed output folder!")
except:
    pass

global csv_files_list
csv_files_list = []


threadLock = threading.Lock()
bot = telegram.Bot(token='544485370:AAGcj3tJlduMprdz3rpVt1Fm-GL7uDGia4Q')
# bot.send_message(chat_id=330239471, text="<b>"+socket.gethostname()+":</b> New search launched. Starting JSON query.", parse_mode=telegram.ParseMode.HTML)
TELEPY = TELEPY()

TELEPY.drop_duplicates()

df_input, rows_input = TELEPY.read_source_csv()
postal_codes = TELEPY.read_postal_codes("de")
final_company = pd.DataFrame()

numberThreads = 12
nThreads = len(df_input.index) if numberThreads > len(df_input.index) else numberThreads

writerT = writerThread("Writer-Thread", nThreads).start()

thread_list = []
for index in range(0, nThreads):
    thread = mainThread(index, "Thread-"+str(index), index, nThreads, df_input, postal_codes, final_company, 1)
    thread.start()
    thread_list.append(thread)

threading.enumerate()[1].join()

for t in thread_list:
    t.join()

final_company = pd.read_csv("output/csv/final_company.csv", dtype='unicode').replace(np.nan, "N/A", regex=True)

thread_list = []
start = time.time()
for index in range(0, nThreads):
    thread = mainThread(index, "Thread-"+str(index), index, nThreads, df_input, postal_codes, final_company, 2)
    thread.start()
    thread_list.append(thread)
    
for t in thread_list:
    t.join()


final_company = pd.read_csv("output/csv/final_company.csv", dtype='unicode')

counter_final_statement = 0
for col in final_company.columns: 
 if 'locations.values' and 'city' in col:
    counter_final_statement+=1

TOTAL = pd.read_csv("output/csv/TEST.csv", dtype='unicode')

erase_unwanted_headquarters_finalStatement = 'It took '+ humanfriendly.format_timespan(time.time() - start)+ ' to comb through '+str(len(final_company.index) * counter_final_statement)+' entries (or '+str(len(final_company.index))+' companies) and verify  '+str(len(TOTAL.index))+ ' matches - ',"{0:.2f}".format(len(TOTAL.index)/len(final_company.index)*100)+'% hit rate.'

fd = open('./output/csv/TEST.csv','a')
fd.write("".join(erase_unwanted_headquarters_finalStatement))
fd.close()

print('\n'+bcolors.WARNING + "".join(erase_unwanted_headquarters_finalStatement)+ bcolors.ENDC)
bot.send_message(chat_id=330239471, text="<b>"+socket.gethostname()+":</b> Done. "+"".join(erase_unwanted_headquarters_finalStatement), parse_mode=telegram.ParseMode.HTML)

print("Finished!")



# df = TELEPY.doQuery(1, rows, 0, 3, 0)

# print(bcolors.WARNING + '\nIt took', humanfriendly.format_timespan(time.time() - start), 'seconds to fetch',
#       len(os.listdir("output/json/")), 'JSON files, from which',
#       len((df['matches (starting at 0)'] == 0).unique().astype(int)) - 1, 'are empty\n', bcolors.ENDC)

# bot.send_message(chat_id=330239471, text="<b>"+socket.gethostname()+":</b> Telepy_v2: Starting CSV conversion.", parse_mode=telegram.ParseMode.HTML)
# TELEPY.convert_to_csv()

# bot.send_message(chat_id=330239471, text="<b>"+socket.gethostname()+":</b> Telepy_v2: Unifying all CSV files.", parse_mode=telegram.ParseMode.HTML)
# TELEPY.unify_companies(df, rows)

# bot.send_message(chat_id=330239471, text="<b>"+socket.gethostname()+":</b> Telepy_v2: Creating 'final_companies.csv'.", parse_mode=telegram.ParseMode.HTML)
# TELEPY.unify_all_csv()

# postal_codes = TELEPY.read_postal_codes("de")

# bot.send_message(chat_id=330239471, text="<b>"+socket.gethostname()+":</b> Sourcing all german locations.", parse_mode=telegram.ParseMode.HTML)
# final_statement = TELEPY.erase_unwanted_headquarters(postal_codes)

# bot.send_message(chat_id=330239471, text="<b>"+socket.gethostname()+":</b> Done. "+final_statement, parse_mode=telegram.ParseMode.HTML)

###########

# This only when I got all three locations from country (loc_to_keep)
# TELEPY.remove_location_cols(3)
