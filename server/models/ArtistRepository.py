import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import functools
import operator
import logging

class ArtistRepository():
    
    def __init__(self):
        self.dataset = pd.read_csv('/Users/woutdemeyere/Documents/MCT/Advanced Programming & Maths/ProgrammingProject/server/models/artists.csv',
                                    dtype=str)
        self.genres = {}

        #self.get_sorted_genres()
    
    #Give a bar graph of most popular genres
    def get_sorted_genres(self):
        for i in range(100000):
            rec = self.dataset['tags_mb'][i]
        
            if type(rec) == str:

                rec_tags = rec.split(';')

                for tag in rec_tags:
                    self.check_tag(tag, int(self.dataset['listeners_lastfm'][i]) / 100)
    
    def check_tag(self, tag, amount):
        amount = round(amount, 2)
        
        if tag in self.genres:
            self.genres[tag] += amount

        else:
            self.genres[tag] = amount



    def execute_query(self, query_number, param):
        print(query_number ,param)

        try:
            if query_number == "Q0":
                    if type(param) == str:
                        temp = self.dataset.loc[self.dataset['artist_mb'] == param].tags_mb.values
                        #print(temp[0])
                        data = pd.Series(temp[0].split(';'))
                        #print(data)
            
            elif query_number == "Q1":
                    if type(param) == str:
                        data = self.dataset.loc[self.dataset['country_mb'] == param].artist_mb[:50]

            elif query_number == "Q2":
                    if type(param) == str:
                        data = self.dataset.loc[self.dataset['tags_mb'].str.contains(param, na=False)].artist_mb[:50]

            elif query_number == "Q3":
                    if type(param) == str:
                        data = self.dataset.loc[self.dataset['country_mb'] == param].artist_mb

            elif query_number == "Q4":
                    if type(param) == str:
                        data = self.dataset.loc[self.dataset['country_mb'] == param].artist_mb
            else:
                raise Exception('Unkonw Qurey number')
            print(type(data))

            data_json = data.to_json(orient='values')

            print(data_json)
            return data_json

        except Exception as e:
            logging.error(e)
            
        
        

if __name__ == '__main__':
    repo = ArtistRepository()

    print(repo.execute_query('Q0', "Eminem"))
            
