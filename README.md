# Food Recipes App
Author: Xingyu Qiu

## Abstract
### Project Purpose
Create a website that display and visualizes the data of food recipes scraped from Fatsecret.

### Project Motivation
The most enjoyable part of a day is eating, and we may find it hard to decide what to cook depending on different numbers of people, preparation time, and steps for cooking. I want to make a web application to display all kinds of food recipes and allow users to search the types of food that fulfills their requirements.

## Technical Specification
- API: Flask
- Programming Languages: JavaScript, HTML, CSS, Python
- Stylistic Conventions: JavaScript Style Guide and Python style guide
- IDE: Visual Studio Code, PyCharm
- Tools/Interfaces: React, D3.js
- Backend: Flask, MongoDB

## Functional Specification
### Features
- Gather information of food recipes from Fatsecret by scraping
- Display of all food from mongoDB in web page
- Search food by fields like yields, prep time, cook time, meal type
- Update the food recipes by CRUD operations including PUT and POST
- Visualization of food by their yields, prep time, cook time, popularity in ascending or descending order

### Scope of the project
- This project currently might be only deployed on localhost
- Search by food ratings is not available because Fatsecret uses images to display ratings

## Brief Timeline
- Week 1:
    - Web Scraping of food recipes
    - Fields include name, summary, yields, prep time, cook time, meal type, popularity, ingredients, instructions
    - Data Storage in an MongoDB
    - Data export to JSON file
    - Command Line Interface
- Week 2:
    - query parser
    - API Creation
    - Command line extension
- Week 3:
    - Four tabs and tabpanels for all food names list, favourite food names list, food recipe display, data visualizations
    - Render and update content
    - Data Visualization by yields, prep time, cook time, popularity
