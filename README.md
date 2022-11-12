# SOEN6441_Project
This project is an implementation of an application for interacting with Football Fantasy pl API(fpl) and sending requests to local database to get the best lineup for the next weekgame.
In this project we will mainly use python for our implementation. sqlite was used to store the tables and their relations into a local database.\
this application returns out a 15-men shortlist which gives you a suggested team when you you want to use your fpl wildcard. It should be noted that no team in fpl can have more than 3 players from a specific pl-team. secondly our suggested team should be within a 1000 budget limit to be considered as a reasonable team.
