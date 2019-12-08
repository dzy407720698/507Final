# 507Final Project
Data sources: </br>
https://www.imdb.com/search/title/?title_type=feature&num_votes=4500,&languages=en&sort=user_rating,desc&start=1&ref_=adv_nxt
https://www.imdb.com/search/title/?title_type=feature&num_votes=4500,&languages=en&sort=user_rating,desc&start=51&ref_=adv_nxt

## Instruction to Before Run the Program:
Mac: use Terminal to run/Windows: use Anaconda Prompt & pip install -r requirements.txt


## Code Structured:
a) I have one Class called cache which contains five functions. Through this class, I could using BeautifulSoup to get the data.
  1) _has_entry_expired function make sure the scraping data is new. 
  2) get function scraping the data from website, and saving it as csv to the local by call the _save_to_disk function.

b) Creating two tables, Movies and Ratings, and import the data from csv file.

c) Using flask_sqlalchemy to open the Flask, so you don't need to create the new flask, and install the package If you already has the packages in your Python.

## How to Run the Program
1. Open Terminal/Anaconda Prompt
2. type: python (file path)
3. go to http://localhost:5000/

There have four nevigation pages:index(Welcome page),search page, movie info page, and rating info page.

In the search page, you could search the movie title or director name.

In the movie info page, you could check the movie information.

In the rating info page, you could check the rating information.

