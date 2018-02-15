'''
CIS 15 Final Project

Final Project - A simulated user input comparison application

My final project simulates a site that tracks and compares user entered data.

We achieve the simulation by seeding thousands of pieces of randomly generated data
that is realistic within the bounds of what real user input might be. We then ask 
the user to input their data so that we can compare it to what other "users" have input.

Because of the questions asked (geolocation and demograpic data), it was necessary to fake
user data by seeding the database and made for a good database query exercise. The datastore database will still 
store authentic user data. For this exercise, we would have never recieved enough authentic 
user data to get even close to a desired result.

NOTES ON USER INPUT: The app will crash if input data isn't well-formed. If it is well formed 
and out of the scope of data we are comparing against, we do handle that in our algorithm 
function by assigning the bad variable a new random value.

@author Christopher Jacobs
@updated 12/12/17


'''

from __future__ import print_function, division

import traceback, sys, random

from flask import Flask, render_template, request, redirect

from google.appengine.ext import ndb

app = Flask(__name__)


#data store class
class DataModel(ndb.Model):
    """Models a session of form entries from the user for google datastore
    Args:
        ndb.Model: the model structure
        grav (int): representing how hungover the user feels
        latitude(float): user location latitude
        longitude(float: user location longitude
        sex(str): user sex (male or female)
        age(int): user age
        dur(int): time in hours spent drinking (duration)
        drinks(int): amount of user drinks
        waters(int): amount of user waters
        
    Returns:
        entitiy with properties grav, latitude, longitude, sex, age, dur, drinks, waters
    
    """
    grav = ndb.IntegerProperty()
    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()
    sex = ndb.StringProperty()
    age = ndb.IntegerProperty()
    dur = ndb.IntegerProperty()
    drinks = ndb.IntegerProperty()
    waters = ndb.IntegerProperty()

#initialize user data, not necessary up here but helps visualize
session_data = DataModel(grav=-1, latitude=-1, longitude=-1,sex="",age=-1,dur=-1,drinks=-1,waters=-1)
session_data_key = session_data.put() #keep session key so we can keep changing the data

#every time the app starts up were gonna seed a bunch of random data so we can display results 
for i in range(0, 1000):
    male_female = ["male", "female"]
    rand_grav = random.randint(1,100)
    #bounding box (clockwise and approx) San Diego, Kootenai Nat Forrest, Toronto, Charlotsville
    rand_long = random.uniform(0, 90)
    rand_lat = random.uniform(0, 180)
    rand_age = random.randint(18, 112)
    rand_sex = random.choice(male_female)
    rand_dur = random.randint(2, 6) #between 2 and 8 hrs
    rand_drinks= random.randint(2, 10)
    rand_waters = random.randint(2, 10)
    fake_data = DataModel(grav=rand_grav, longitude=rand_long, latitude=rand_lat, age=rand_age, sex=rand_sex, dur=rand_dur, waters=rand_waters, drinks=rand_drinks)
    fake_data_key = fake_data.put()


def algorithm(DataModel, session_key):
    """This does all the heavy lifting for finding our output on percentile hungove and hangover rank by region
    Args:
        DataModel(Object): data model to use for creating query
        session_key(int): key of the current user entity for retrieving archived current user data
    Returns:
        float: user's index in sorted list divided by total list len
        int: index of user data in sorted list
        
    """
    tot_grav_percentile = [] #list so we can sort then divide by len
    tot_grav_rank_list = [] #so we can sort and get index from search
    percent = 0
    rank = 0
    fetch_data = session_data_key.get()
    user_grav = fetch_data.grav
    #request and find our demographic
    demographic_sex = fetch_data.sex
    demographic_age = fetch_data.age
    demographic_lat = fetch_data.latitude
    demographic_lon = fetch_data.longitude
    #gotta put a placeholder number and our own data 
    #so we return results at index 0 to do math with
    tot_grav_percentile.append(-69)
    tot_grav_rank_list.append(-69)
    tot_grav_percentile.append(user_grav)
    tot_grav_rank_list.append(user_grav)
    # do some validation here instead of in the form. If it's not valid we'll assign it a rand for our purposes
    if 100 < user_grav or 0 > user_grav:
        user_grav = random.randint(1,100)
    if 112 < demographic_age or demographic_age < 18:
        demographic_age = random.randint(18, 112)
    if 90 < demographic_lon or demographic_lon < 0:
        demographic_lon = random.uniform(0, 90)
    if 180 < demographic_lat or demographic_lat < 0:
        demographic_lat = random.uniform(0, 180)
    if demographic_sex != "male" or demographic_sex != "female":
        male_female = ["male", "female"]
        demographic_sex = random.choice(male_female)
    
    #manipulate data to get demographic age range
    demographic_age_min = demographic_age - 6
    demographic_age_max = demographic_age + 6
    
    #get lat and lon range
    demographic_lat_min = demographic_lat - 5
    demographic_lat_max = demographic_lat + 5
    
    demographic_lon_min = demographic_lon - 10
    demographic_lon_max = demographic_lon + 10
 
    #query is a list of our Data Models
    #query for demographic info by age and sex
    query_age = DataModel.query(DataModel.age > demographic_age_min, DataModel.age < demographic_age_max, DataModel.sex == demographic_sex).fetch()
    query_location = DataModel.query(DataModel.latitude >= demographic_lat_min, DataModel.latitude < demographic_lat_max).fetch()
    #for loop to add our grav (hungoverness) to lists to manipulate and get desired percentile and rank
    for temp in query_age:
        tot_grav_percentile.append(temp.grav)

    for temp in query_location:
        if demographic_lon_max > temp.longitude > demographic_lon_min:
            tot_grav_rank_list.append(temp.grav)
        else:
            pass
    #prep lists (sort) so we can return index of first instance to get stats
    tot_grav_percentile.sort()
    tot_grav_rank_list = sorted(tot_grav_rank_list, key=int, reverse=True)
    #case where user pain isn't in list, use new counting var so we can use user_grav again for rank
    count_grav = user_grav
    while count_grav not in tot_grav_percentile:
        count_grav+1
    
    #percentile calculated from position of user data in the whole sorted list 
    percent = (tot_grav_percentile.index(count_grav) / len(tot_grav_percentile)) * 100
    
    count_grav = user_grav
    while count_grav not in tot_grav_rank_list:
        count_grav+1
    
    rank = tot_grav_rank_list.index(count_grav) + 1 #so we can't be the 0th
    #print(percent)
    #print(rank)
    #print(len(tot_grav_percentile))
    #print(tot_grav_percentile.index(count_grav))
    #print(tot_grav_rank_list)
    
    return percent, rank
    
@app.route('/', methods = ("GET", "POST"))
def landing():
    return render_template("landing.ejs")

@app.route('/step1', methods = ("GET", "POST"))
def step1():
    if request.method == 'POST':
        #snatch up the data
        fetch_data = session_data_key.get()
        fetch_data.grav = int(request.form["gravity"])
        fetch_data.put()
        
        return render_template("step2.ejs")
    else:    
        return render_template("step1.ejs")

@app.route('/step2', methods = ("GET", "POST"))
def step2():
    if request.method == 'POST':
        #snatch up the data
        fetch_data = session_data_key.get()
        fetch_data.latitude = int(request.form["latitude"])
        fetch_data.longitude = int(request.form["longitude"])
        fetch_data.age = int(request.form["age"])
        sex_lowercase = request.form["sex"]
        sex_lowercase = sex_lowercase.lower()
        fetch_data.sex = sex_lowercase
        fetch_data.put()
        #testing to see if our data made it in 
        #print(session_data, file=sys.stderr)
        
        return render_template("step3.ejs")
    else:    
        return render_template("step2.ejs")

@app.route('/step3', methods = ("GET", "POST"))
def step3():    
    if request.method == 'POST':
               #snatch up the data
        fetch_data = session_data_key.get()
        fetch_data.dur = int(request.form["duration"])
        fetch_data.drinks = int(request.form["drinks"])
        fetch_data.waters = int(request.form["waters"])
        fetch_data.put()
        
        #testing to see if our data made it in 
        #print(session_data, file=sys.stderr)
        
        return redirect("/display")
    else:    
        return render_template("step3.ejs")
        
@app.route('/display')
def display():
    fetch_data = session_data_key.get()
    
    percent, rank = algorithm(DataModel, session_data_key)
    
    return render_template("display.ejs", percent=percent, rank=rank)

#static about page
@app.route('/about')
def about():
    return render_template("about.ejs")
#static contact page
@app.route('/contact')
def contact():
    return render_template("contact.ejs")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.ejs'), 404

@app.errorhandler(500)
def server_error(e):
    print (traceback.format_exc())
    return traceback.format_exc(), 500, {'Content-Type': 'text/plain charset=utf-8'}