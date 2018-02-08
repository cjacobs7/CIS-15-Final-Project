CIS 15 Final Project 
Christopher Jacobs

============================================
INSTRUCTIONS FOR DEPLOYING AGAIN At DIFF URL:
make new project on google app engine
gcloud init a new project
gcloud app deploy from /FinalProject/hangovr
============================================


My final project simulates a site that tracks and compares user entered data.

We achieve the simulation by seeding thousands of pieces of randomly generated data
that is realistic within the bounds of what real user input might be. We then ask the user to input
their data so that we can compare it to what other "users" have input.

Because of the questions asked (geolocation and demograpic data), it was necessary to fake
user data. However, the datastore database will store authentic user data. For this exercise,
we would have never recieved enough authentic user data to get even close to a desired result.

Couple Notes: The app will crash if input data isn't well-formed. If it is well formed and out
of the scope of data we are comparing against, we do handle that in our algorithm function by
assigning the bad variable a new value. 

I also could have stored my seed data in cache but I thought that it would be better to utilize a database
so I could seed as much data as I wanted.



You can find it hosted on: 

  https://helloworld-187417.appspot.com/ and https://hangovr-network.appspot.com
  
Requirements met (indicate what file/line if yes): 

  - Has a class: Yes
  - Uses a list or dictionary: Yes 
  - Uses a for or while loop: Yes both
  - Takes input using a form: Yes main function of the UI
  - All python files with a docstring: Yes
  - All classes with a docstring: Yes
  - All functions with a docstring: Yes

