# Written by: 
__author__ = "Cache Me if You Can"

import os
import requests
import requests_cache
from tabulate import tabulate
from requests import Response
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.dates as mdates
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image
from functools import wraps 
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


load_dotenv()
user_agent = os.getenv("USER_AGENT")

CACHE_EXPIRATION = 600
requests_cache.install_cache('params', expire_after=CACHE_EXPIRATION)

"""Inspiration from YouTube:
Memoization: The TRUE Way To Optimize Your Code In Python
 of Indently on Youtube: 
 https://www.youtube.com/watch?v=qORqpMg3Uew&ab_channel=Indently
"""



class Politikk:
    """
    Uses the API to fetch data.
    """

    def __init__(self):
        """
        On class initialization, important variables are defined and essential functions are run.
        """
        self.url = 'https://api...'
        self.headers = { 
            "User-Agent": os.getenv("USER_AGENT")
}
        
        
    def memoize(func):
        """
        Memoization is not implemented in the rest of the code,
        but can be used by interested developers to enhance the performance.
        """
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        return wrapper

    def json_data(self) -> bool:
        """
        Loads data from an existing JSON file or fetches from the API.
        Returns True if loaded from file, 
        False if fetched from API.
        """
        try:
            data_folder_json = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/json'))
            file_path = os.path.join(data_folder_json, 'CACHE_ME_IF_YOU_CAN.json')
            if os.path.exists(file_path) and self.check_if_correct_params():
                print("Loading data from file")
                with open(file_path, 'r') as file:
                    self.data = json.load(file)
                    self.process_all_data()
                return True
            else:
                print("Fetching data from API")
                self.fetch_data()
                return False
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print("Fetching data from API")
            self.fetch_data()
            return False

    def txt_data(self) -> bool:
        """
        Loads data from the test_file.txt file, for letting AI write and read secure information across computers.

        Returns True if the file can be read, otherwise False

        In this function, AI reads and writes content to a txt file, which later will be sent across the localhost using the TLS protocol. 
        This is a secure way to let AI write and read information across computers, without the risk of exposing sensitive information in the code or through unsecured channels.
    
        """
        
        try:
            data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            file_path = os.path.join(data_folder, 'test_file.txt')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            """
            
            Her kommer koden for å la AI skrive og lese. 


            """


        except FileNotFoundError:
            return False


    def fetch_data(self) -> dict:
        """
        Fetches data as a JSON file from the API
        """
        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code in [200, 203]:
            self.data = response.json()
            self.save_to_json_file()
            self.process_all_data()
            source = 'CACHE' if getattr(response, 'from_cache', False) else 'API'
        else:
            print(f'Error fetching data: {response.status_code}')
            source = 'API'

    def save_to_json_file(self) -> None:
        """
        Saves the data to a JSON file for later use.
        """
        try:
            data_json_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            file_path = os.path.join(data_json_folder, 'Hackaton.json')
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"Error saving JSON file: {e}")

    def communication(self):
        """
        
        This function ensures that the code read and written in the txt file is sent across the localhost server

        """

        
