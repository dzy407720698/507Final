from SI507FinalProject import * 
import unittest
import csv
import json
import numpy as np
import random
import itertools

class PartTwo(unittest.TestCase):
    def test_cache_file(self):
        self.cached_file = open('movies_search_cache.json','r')
        self.row_reader = self.cached_file.readlines()
        self.assertTrue(self.row_reader[0].split(",")[0], "Testing that there are contents in the Cache file")
        self.cached_file.close()

class PartThree(unittest.TestCase):
    def test_csv_file(self):
        self.csv_file = open('movie_info.csv','r')
        self.row_reader = self.csv_file.readlines()
        self.assertTrue(self.row_reader[0], "Testing that there are contents in the CSV file")
        self.csv_file.close()

class PartFour(unittest.TestCase):
    def test_csv_size(self):
        self.csv_file = open('movie_info.csv','r')
        self.row_reader = self.csv_file.readlines()
        self.assertTrue(len(self.row_reader) >= 50, "Testing that there are at least 50 lines of data in the CSV")
        self.csv_file.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
