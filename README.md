# Ingredients For A Good Recipe

# Abstract

What defines a successful recipe? There are a million different meals that have different popularities, and we each have our favorite ones. However, a lot of meals are objectively appreciated across a large part of the population… But what could be the origin of this attractiveness? Our goal is to investigate every variable that could have an impact on the success of the recipe, such as the ingredients, the type of meal (main course, dessert, …), time to prepare it, etc … We plan to use the dataset “Cooking recipes” which provides a ranking of the recipes as well as a lot of interesting variables. We will investigate the relations between these variables and the ranking of the recipe. Based on our analysis, we will create a model that is able to predict the rating of a random recipe. We will also try to see whether this model is able to create new recipes by using the optimal parameters found during the analysis.



# Research questions

For our project, we will focus on the following questions:

- From where does the rating of the recipe come from ? Ingredients, time, combination between ingredients, what type of meal (main course, dessert, ...), originality ?

- Is the pattern clear enough to be able to predict the ranking a new recipe will have ? 

- Is it possible to create new good recipes by using the data gathered in the analysis ?

- Is there a relation between the ingredients used in popular recipes and the production quantity of those ingredients in the year where the recipe is popular





# Dataset

We plan to mainly use the dataset "Cooking recipes". It contains the ingredients, the rating of the recipe (number of reviews and grade of the recipe to assign a popularity index) and for most of them we can estimate the upload year by looking at the earliest comment. Scraping will be needed since the dataset contains webpages, and it will take a long time since there are different types of webpages. If we want to improve/expand our dataset we can use other recipes found in the Recipe1M+ database (Json file), which contains information about the ingredients and the steps to cook the recipe. For the predictive part, the first task will be to select the variables which have a significant impact on the ranking. Then, the second task will be to find the best combos of variables by performing PCA for example. After that, if the linearity of the system is pleasing enough, we will use these principal axis for the prediction of the rank of a random recipe. Finally, by using an agglomeration function will determine the tendency of ingredients used in recipes and compare them with the ingredient production per year and per country (Global Food & Agriculture Statistics dataset) to see if we can detect some relations (based on the production year/used recipes).



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

- Create new recipes with the obtained data

- Determine if there is a relation between the ingredients used in popular recipes and the production quantity of those ingredients in the year where the recipe is popular

20.12.2019:

- Finalize the Data Notebook

10.01.2020:

- Creation of the poster

- Preparation for the presentation


# Questions for TAa

- Is the prediction system doable in a reasonable amount of time ? 

- Are we allowed to import any libraries that can help us with our tasks ?
