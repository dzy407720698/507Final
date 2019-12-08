import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
import random
from itertools import product, permutations
import pandas as pd
import csv
import os
from flask import Flask, render_template, session, redirect,request, url_for 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'None'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./movies_results.db' 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG = True

class Cache:
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(self.filename, 'r') as cache_file:
                cache_json = cache_file.read()
                self.cache_diction = json.loads(cache_json)
        except:
            self.cache_diction = {}

    def _save_to_disk(self):
        with open(self.filename, 'w') as cache_file:
            cache_json = json.dumps(self.cache_diction)
            cache_file.write(cache_json)

    def _has_entry_expired(self, timestamp_str, expire_in_days):
        now = datetime.now()

        cache_timestamp = datetime.strptime(timestamp_str, DATETIME_FORMAT)

        delta = now - cache_timestamp
        delta_in_days = delta.days

        if delta_in_days > expire_in_days:
            return True 
        else:
            return False

    def get(self, identifier):
        identifier = identifier.upper() 
        if identifier in self.cache_diction:
            data_assoc_dict = self.cache_diction[identifier]
            if self._has_entry_expired(data_assoc_dict['timestamp'],data_assoc_dict['expire_in_days']):
                if DEBUG:
                    print("Cache has expired for {}".format(identifier))

                del self.cache_diction[identifier]
                self._save_to_disk()
                data = None
            else:
                data = data_assoc_dict['values']
        else:
            data = None
        return data

    def set(self, identifier, data, expire_in_days=7):
        identifier = identifier.upper() 
        self.cache_diction[identifier] = {
            'values': data,
            'timestamp': datetime.now().strftime(DATETIME_FORMAT),
            'expire_in_days': expire_in_days
        }

        self._save_to_disk()

FILENAME1 = "movies_search_cache1.json"
FILENAME2 = "movies_search_cache2.json"

program_cache1 = Cache(FILENAME1) 
program_cache2 = Cache(FILENAME2) 

url1 = "https://www.imdb.com/search/title/?title_type=feature&num_votes=4500,&languages=en&sort=user_rating,desc&start=1&ref_=adv_nxt" 
url2 = "https://www.imdb.com/search/title/?title_type=feature&num_votes=4500,&languages=en&sort=user_rating,desc&start=51&ref_=adv_nxt" 


data1 = program_cache1.get(url1)
data2 = program_cache2.get(url2)

if not data1 and not data2: 
    data1 = requests.get(url1).text 
    data2 = requests.get(url2).text 

    program_cache1.set(url1, data1, expire_in_days=1) 
    program_cache2.set(url2, data2, expire_in_days=1) 

soup1 = BeautifulSoup(data1, "html.parser") 
soup2 = BeautifulSoup(data2, "html.parser") 


movie_titles,release_dates,runtimes,descriptions,ratings,box_office,num_votes,IMDB_ratings,directors,metascores,genres = [],[],[],[],[],[],[],[],[],[],[]  


movies_list1 = soup1.find_all('div',{'class':'lister-item-content'})
movies_list2 = soup2.find_all('div',{'class':'lister-item-content'})

for i in movies_list1:
    title = i.h3.a.text
    movie_titles.append(title)

    release = i.find('span',{'class':'lister-item-year'})
    release_dates.append(release.text)

    time = i.find('span',{'class':'runtime'})
    if time == None:
        time = 'N/A'
        runtimes.append(time)
    else:
        runtimes.append(time.text)

    rating = i.find('span',{'class':'certificate'})
    if rating == None:
        rating = 'N/A'
        ratings.append(rating)
    else:
        ratings.append(rating.text)

    votes_gross = i.find_all('span',{'name':'nv'})
    votes = votes_gross[0]
    num_votes.append(votes.text)

    if len(votes_gross) == 2:
        gross = votes_gross[1]
        box_office.append(gross.text)
    else:
        gross = 'N/A'
        box_office.append(gross)

    imdb = i.find('div',{'class':'ratings-imdb-rating'})
    IMDB_ratings.append(imdb.strong.text)

    meta = i.find('span',{'class':'metascore'})
    if meta == None:
        meta = 'N/A'
        metascores.append(meta)
    else:
        metascores.append(meta.text)

    p_elements = i.find_all('p')
    p = p_elements[2]
    a_elements = p.find_all('a')
    director = a_elements[0]
    directors.append(director.text)

    p_text = i.find_all('p',{'class':'text-muted'})
    about = p_text[1]
    descriptions.append(about.text)

    genre = i.find('span',{'class':'genre'})
    genres.append(genre.text)

for i in movies_list2:
    title = i.h3.a.text
    movie_titles.append(title)

    release = i.find('span',{'class':'lister-item-year'})
    release_dates.append(release.text)

    time = i.find('span',{'class':'runtime'})
    if time == None:
        time = 'N/A'
        runtimes.append(time)
    else:
        runtimes.append(time.text)

    rating = i.find('span',{'class':'certificate'})
    if rating == None:
        rating = 'N/A'
        ratings.append(rating)
    else:
        ratings.append(rating.text)

    votes_gross = i.find_all('span',{'name':'nv'})
    votes = votes_gross[0]
    num_votes.append(votes.text)

    if len(votes_gross) == 2:
        gross = votes_gross[1]
        box_office.append(gross.text)
    else:
        gross = 'N/A'
        box_office.append(gross)

    imdb = i.find('div',{'class':'ratings-imdb-rating'})
    IMDB_ratings.append(imdb.strong.text)

    meta = i.find('span',{'class':'metascore'})
    if meta == None:
        meta = 'N/A'
        metascores.append(meta)
    else:
        metascores.append(meta.text)

    p_elements = i.find_all('p')
    p = p_elements[2]
    a_elements = p.find_all('a')
    director = a_elements[0]
    directors.append(director.text)

    p_text = i.find_all('p',{'class':'text-muted'})
    about = p_text[1]
    descriptions.append(about.text)

    genre = i.find('span',{'class':'genre'})
    genres.append(genre.text)

db = SQLAlchemy(app) 
session = db.session 

class Movies(db.Model):
    __tablename__ = "Movies"
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(64))
    ReleaseDate = db.Column(db.String(64))
    Director = db.Column(db.String(64))
    Genre = db.Column(db.String(64))
    Description = db.Column(db.String(1000))
    MPAARating = db.Column(db.String(64))
    RunTime = db.Column(db.String(64))

    def __repr__(self):
        return "{}: {} is a {} movie released in {} and directed by {}. It recieved an MPAA rating of {} and has a runtime of {}. \n Short Description: {}\n".format(self.id,self.Title,self.Genre,self.ReleaseDate,self.Director,self.MPAARating,self.RunTime,self.Description)

class Ratings(db.Model):
    __tablename__ = "Ratings"
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(64), db.ForeignKey("Ratings.Title"))
    IMDBRating = db.Column(db.String(64))
    Votes = db.Column(db.String(64))
    Metascore = db.Column(db.String(64))

    def __repr__(self):
        return "{}: {} has an IMDB rating of {} based on {} user ratings. It's Metascore is {}\n".format(self.id,self.Title,self.IMDBRating,self.Votes,self.Metascore)

movie_info = pd.DataFrame({'Title': movie_titles,
                       'Director': directors,
                       'Release Date': release_dates,
                       'Run Time': runtimes,
                       'Genre': genres,
                       'MPAA Rating': ratings,
                       'Description': descriptions,
                       'IMDB Rating': IMDB_ratings,
                       'Number of Votes': num_votes,
                       'Metascore': metascores,
})

csv_file_name = "movie_info.csv"

movie_info.to_csv(csv_file_name)


def add_to_db():
    with open("movie_info.csv", "r") as f:
        reader = csv.reader(f)
        data = []
        for i in reader:
            data.append(i)


    for i in data[1:]:
        movie = Movies(Title = i[1],ReleaseDate = i[3],Director = i[2],Genre = i[5],Description = i[7],MPAARating = i[6],RunTime = i[4])
        rating = Ratings(Title = i[1],IMDBRating = i[8],Votes = i[9],Metascore = i[10])

        session.add(movie)
        session.add(rating)
        session.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search_results')
def results():
    if request.method == 'GET':
        keyword = request.args.get('keyword')
        keyword = keyword if keyword else 'Endgame'
        results = session.query(Movies).all()
        results_lst = []
        for i in results:
            if keyword in i.Title:
                results_lst.append(i)
            if keyword in i.Director:
                results_lst.append(i)
        return render_template('results.html',keyword = keyword, results = results_lst)
    
@app.route('/movies')
def movies():
    movies = Movies.query.all()
    movies_str= list(map(lambda x: str(x), movies))
    return render_template('movies.html', results = movies_str)

@app.route('/ratings')
def ratings():
    ratings = Ratings.query.all()
    ratings_str= list(map(lambda x: str(x), ratings))
    return render_template('ratings.html', results = ratings_str)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    add_to_db()
    app.run()
