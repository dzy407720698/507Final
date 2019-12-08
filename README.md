# 507Final Project
Data sources: </br>
https://www.imdb.com/search/title/?title_type=feature&num_votes=4500,&languages=en&sort=user_rating,desc&start=1&ref_=adv_nxt
https://www.imdb.com/search/title/?title_type=feature&num_votes=4500,&languages=en&sort=user_rating,desc&start=51&ref_=adv_nxt

## Instruction to Run the Program:
Mac: use Terminal to run/Windows: use Anaconda Prompt
1. pip install -r requirements.txt
2. python (file path)
3. go to http://localhost:5000/

## Code Structured:
a) I have one Class called cache which contains five functions. Through this class, I could using BeautifulSoup to get the data.
  1) _has_entry_expired function make sure the scraping data is new. 
  2) get function scraping the data from website, and saving it as csv to the local by call the _save_to_disk function.

b) Creating two tables, Movies and Ratings, and import the data from csv file.

c) Using flask_sqlalchemy to open the Flask, so you don't need to create the new flask, and install the package If you already has the packages in your Python.


