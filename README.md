# Ingredients For A Good Recipe

# Abstract

What defines a successful recipe? There are a million different meals that have different popularities, and we each have our favorite ones. However, a lot of meals are objectively appreciated across a large part of the population… But what could be the origin of this attractiveness? Our goal is to investigate every variable that could have an impact on the success of the recipe, such as the ingredients, the type of meal (main course, dessert, …), time to prepare it, etc … We plan to use the dataset “Cooking recipes” which provides a ranking of the recipes as well as a lot of interesting variables. We will investigate the relations between these variables and the ranking of the recipe. Based on our analysis, we will create a model that is able to predict the rating of a random recipe. We will also try to see whether this model is able to create new recipes by using the optimal parameters found during the analysis.



# Research questions

For our project, we will focus on the following questions:

- From where does the rating of the recipe come from ? Ingredients, time, combination between ingredients, what type of meal (main course, dessert, ...), originality ?

- Is the pattern clear enough to be able to predict the ranking a new recipe will have ? 

- Is it possible to create new good recipes by using the data gathered in the analysis ?

- Is it possible to find some relations between the ingredient used in recipe and the production of those ingredient (based on the year of production/used recipes)?






# Dataset
List the dataset(s) you want to use, and some ideas on how do you expect to get, manage, process and enrich it/them. Show us you've read the docs and some examples, and you've a clear idea on what to expect. Discuss data size and format if relevant.

We plan to mainly use the dataset "Cooking recipes". It contains the ingredients, the rating of the recipe (number and grade of the recipe to assign a popularity index) and for most of them we could identify the year with the earliest comment. Scraping will be needed since the dataset contains webpages, and it will take a long time since there are different types of webpages. If we want to stuff more our datasets we can use other recipe coming from the database Recipe1M+ (Json file), which contain all information about ingredient and all the step to cook. For the predictive part, the first task will be to select the variables which have a significant impact on the raking. Then, the second task will be to find the best combos of variables by performing a PCA for example. After that, if the linearity of the system is pleasing enough, we will use these principal axis for predict the rank of a random recipe. Finally, but using agglomeration function we are able to determine the tendency of ingredient used in recipe and compare them with  the ingredient production per year and per country (Global Food & Agriculture Statistics dataset) to see if we can detect some relations (based on the year of production/used recipes).



# A list of internal milestones up until project milestone 2

08.11.2019: 

- Import datasets / Learn how to use the cluster

- Study the datasets and select the useful information

- Scrap/filter the datasets (keep interesting and useful data)

29.11.2019:

- Clean the data (adapt each value of the resulting data to fit in our functions)

- Analyse the correctness of our solution, the possible misintepretations and the limitations of our dataset

- Start Data Notebook

06.12.2019: 

- Create function to determine the ranking of a new recipe based on the analysis results

- Created new recipes with the obtained data

- Determine relations between the popular ingredients used in recipes and the production quantity of those ingredients (based on the year of production/used recipes)

20.12.2019:

- Finalize the Data Notebook

10.01.2020:

- Creation of the poster

- Preparation for the presentation


# Questions for TAa

- Is the prediction system doable in a reasonable amount of time ? 

- Are we allowed to import any libraries that can help us with our tasks ?

- Are the goals we have enough to make a good project ?
