# EbayScrapper
A program for scraping and graphing prices off of Ebay.

This program requires selenium so make sure you have that installed.
These programs also need you to tell them what their path and user is, so open them up and look for two variables called "user" and "path", then set them accordingly. They should be near the top of the program.

Put the items you want to scrape the prices of in the "inputs" list of the EbayScrapper file, the list should be on line 28, the more items you add the longer it takes to run.

The scraper puts all of its info into a file named the current date in YY/MM/DD all in a single line like this, 20220820, for August 20th, 2022. This file will be put into a folder called, "Details". It won't create this file automatically (yet) so you have to do it. The folder should be in the same directory as the scraper program.

The analysis program should be run in the same directory as the scrapper and the "Details" folder and will output its graph as a pdf called "Gpu_Price_Graph" but if you go into the code you can change this to whatever you want.
