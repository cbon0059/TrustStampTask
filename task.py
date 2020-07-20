#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: chrisbonnici
"""

import requests 
import os 
from tqdm import tqdm

# Clearing progress bar instances
tqdm._instances.clear()


# Functions used to obtain information from data list
def get_first_name(data):
    first_name = data['name']['first']
    return first_name 

def get_last_name(data):
    last_name = data['name']['last']
    return last_name 

def get_city(data):
    city = data['location']['city']
    return city

def get_age(data):
    age = data['dob']['age']
    return age

def get_image(data):
    img = data['picture']['large']
    return img 


# Grouping users by their last name (alphabetically)
def group_users(data):
    
    last_names = [get_last_name(data[i]) for i in range(len(data))]        
    
    util_func = lambda x, y: x[0] == y[0] 
    res = [] 

    for sub in last_names: 
        ele = next((x for x in res if util_func(sub, x[0])), []) 
        if ele == []: 
            res.append(ele) 
        ele.append(sub)
        
    return res


# Creating a folder for each group 
def create_folder(last_names):
    
    for i in range (len(last_names)):
        dir = os.path.join("./Users/",last_names[i][0][0])
        if not os.path.exists(dir):
            os.mkdir(dir)
        
# Download image and save in corresponding group       
def download_image(data):

    for entry in tqdm(data, desc ="Downloading Images"):
        
        image_url = get_image(entry)
        letter = entry['name']['last'][0]

        fname = get_first_name(entry)
        lname = get_last_name(entry)
        city = get_city(entry)
        age = get_age(entry)
        
        sep = "_"
        filename = sep.join([str(fname),str(lname),str(city),str(age)])+'.jpg'
        folder = os.path.join('./Users/',letter)
        
        resp = requests.get(image_url, stream=True).content
        
        with open(os.path.join(folder,filename), 'wb') as handler:
            handler.write(resp)
        
        del resp

if __name__ == "__main__":
    
    # Initial request to obtain 200 users 
    resp = requests.get('https://randomuser.me/api/?results=200&inc=gender,name,location,dob,picture&?format=csv&?seed=foobar')

    # JSON Format of the request information
    r = resp.json()
  
    # Data list to be used 
    data = r['results']
    
    dir_name = './Users'
    try:
        os.mkdir(dir_name)
        print("Directory", dir_name, "Created")
    except FileExistsError:
        print("Directory", dir_name, "Exists")
        
    last_names = group_users(data)
    create_folder(last_names)
    download_image(data)






        
    
