# Ingredients For A Good Recipe

# Abstract

What defines a successful recipe? There are a million different meals that have different popularities, and we each have our favorite ones. However, a lot of meals are objectively appreciated across a large part of the population… But what could be the origin of this attractiveness? Our goal is to investigate every variable that could have an impact on the success of the recipe, such as the ingredients, the type of meal (main course, dessert, …), time to prepare it, etc … We use the dataset “Cooking recipes” which provides a ranking of the recipes as well as a lot of interesting variables. We will investigate the relations between these variables and the ranking of the recipe. Based on our analysis, we will create a model that is able to predict the rating of a random recipe. 



# Research questions

For our project, we will focus on the following questions:

- From where does the rating of the recipe come from ? Ingredients, time, combination between ingredients, what type of meal (main course, dessert, ...), originality ?

- Is the pattern clear enough to be able to predict the ranking a new recipe will have ? 





# Dataset

We use the dataset "Cooking recipes". It contains the ingredients, the rating of the recipe (number of reviews and rating of the recipe to assign a popularity index) and the preparation time of the recipe. Scraping is needed since the dataset contains HTML documents, and as there is a lot of different websites, only the most popular ones will be scraped. The quantity of each ingredient is scraped, and online conversion tables for densities and quantities had to be used. For the prediction, the first task will be to select the variables which have a significant impact on the rating. Then, different models have to be fitted to the data. First, we apply a linear regression model to our data create a model able to predict the rating of recipes. After that, we decided to try several classification models. We divided the rating into a binary system of a "good" or "bad" recipe. To realize this classification, we used Random Forests, Neural Networks and K Nearest Neighbors, so we had to optimize the hyperparameters for each of these models. 




# A list of internal milestones up until project milestone 2

08.11.2019: 

- Import datasets / Learn how to use the cluster

- Study the datasets and select the useful information

- Scrap/filter the datasets (keep interesting and useful data)

29.11.2019:

- Scrap the quantity of each ingredient with the help of conversion tables

- Clean the data (adapt each value of the resulting data to fit in our functions)

- Analyse the correctness of our solution, the possible misintepretations and the limitations of our dataset

- Start Report

06.12.2019: 

- Create machine learning models that are able to predict the rating of a recipe

- Combine the different machine learning models to try and get a better result

20.12.2019:

- Finalize the Report

10.01.2020:

- Creation of the poster

- Preparation for the presentation


# Questions for TAa

- Is the prediction system doable in a reasonable amount of time ? 

- Are we allowed to import any libraries that can help us with our tasks ?

# Milestone 2
We have separated our code into 3 parts :
- project.ipynb : The main file for our project which contains all the results and comments.
- scrap.py : This file contains all the functions used for scraping and returning the desired variables.
- website_func.py : This file contains all the functions used to determine the origin of the html file (website).



# Milestone 3

The code is completed. The ingredients and their quantity are scraped and stored in an array.
The machine learning models are done first for regression, and then for classification.

