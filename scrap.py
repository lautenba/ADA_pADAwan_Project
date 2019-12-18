from pathlib import Path
import shutil
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from collections import OrderedDict # for removing redundant words in ingredient

#### Dictionnary quantities
# base unit is gram
tsp_q = 5 # teaspon in milliliter
cup_q = 250 ## volume in milliter
dr = ((e,tsp_q/96) for e in ("drop","drops","dr.","dr","gt.","gt","gtt.","gtt"))
smi = ((e,tsp_q/32) for e in ("smidgen", "smidgens", "smdg.","smdg","smi.","smi"))
p_ = ((e,tsp_q/16) for e in ("pinch","pinches", "pn.","pn"))
da_ = ((e,tsp_q/8) for e in ("dash","dashes","ds.","ds"))
salt_ = ((e,tsp_q/4) for e in ("saltspoon","saltspoons","scruple","scruples","ssp.","ssp"))
cof_ = ((e,tsp_q/2) for e in ("coffeespoon","coffeespoons","csp.","csp"))
tsp_ = ((e,tsp_q) for e in ("teaspoon", "teaspoons","tsp.","tsp","t.","t","fluid dram","fluid drams","fl.dr." ))
dsp_ = ((e,2*tsp_q) for e in ("dessertspoon","dessertspoons","dsp.","dsp","dssp.","dssp","dstspn.","dstspn"))
tbsp_ = ((e,3*tsp_q) for e in  ("tablespoon", "tablespoons", "zbsp.","tbsp","T.","T"))

liter_ = ((e,1000.0) for e in ("l", "l.","liter", "liter)", "liters)", "liters", "litre", "litre)", "litres", "litres)"))
centil_ = ((e,100.0) for e in ("cl","cl.","centiliter", "centiliter)", "centiliters)", "centiliters", "centilitre", "centilitre)", "centilitres", "centilitres)"))
decil_ = ((e,10.0) for e in ("dl", "dl.", "deciliter", "deciliter)", "deciliters)", "deciliters", "decilitre", "decilitre)", "decilitres", "decilitres)"))
ml_ = ((e, 1.0) for e in ("ml.","ml","milliliter","milliliters"))
          
oz_ = ((e, cup_q/8) for e in ("fluid ounces","ounce","ounces","fl.oz","oz.","oz")) #"ounces)", "ounce)",
wgf_ = ((e, cup_q/4) for e in ("wineglass","wineglasses","wgf.","wgf"))
tcf_ = ((e, cup_q/2) for e in ("gill","gills","teacup","teacups","tcf.","tcf"))
c_ = ((e, cup_q) for e in ("cup","cups", "C"))
pt_ = ((e, 2*cup_q) for e in ("pint", "pints", "pt.","pt"))
qt_ = ((e, 4*cup_q) for e in ("quart", "quarts", "qt.", "qt"))
pott_ = ((e, 8*cup_q) for e in ("pottle", "pottles","pot.","pot"))
gal_ = ((e, 16*cup_q) for e in ("gallon","gallons","gal.","gal"))

mg_ = ((e, 0.001) for e in ("mg.","mg","milligram","milligrams"))
cg_ = ((e, 0.01) for e in ("cg.","cg","centigram","centigrams"))
dg_ = ((e, 0.1) for e in ("dg.","dg","decigram","decigrams"))
g_ = ((e, 1.0) for e in  ("g.","g","gm.","gm" "gram", "grams"))
dag_ = ((e, 10.0) for e in  ("dag.","dag","decagram","decagrams"))
hg_ = ((e, 100.0) for e in ("hg.","hg","hectogram", "hectograms"))
kg_ = ((e, 1000.0) for e in ("kg.","kg","kilos","kilo","kilogram","kilograms"))
pound_ = ((e, 453.0) for e in  ("lb", "lb.", "lbs", "lbs.","pounds", "pound","pound)", "pounds)"))

fruit_ = ((e, 1) for e in ("olive", "olives"))

measures_list = (smi ,p_,da_,salt_,cof_,tsp_,dsp_,tbsp_ ,liter_,centil_, decil_, ml_,oz_,wgf_,tcf_,c_,pt_,qt_,pott_,gal_,mg_,cg_,dg_,g_,dag_,hg_,kg_,pound_, fruit_)
dict_quantities = {}
for e in measures_list:
    dict_quantities.update(e)
    
list_measures = dict_quantities.keys()
#####################################
### scraped 
augmented_quantity_dict = pd.read_pickle('data_pickles/augmented_quantity.pkl').set_index("Food").T.to_dict("list")
list_augmented = list(augmented_quantity_dict.keys())
#####
### string to keep for converting to float
s_float = set("01234567890/ ")

## Return the dictionnary of conversion of the units
def get_dict_quantities():
    return dict_quantities

# Credits to ekhumoro https://stackoverflow.com/questions/7794208/how-can-i-remove-duplicate-words-in-a-string-with-python
def removeDoubles(s):
    return ' '.join(OrderedDict.fromkeys(s.split()))
#     to Markus https://stackoverflow.com/a/7794619
#     words = s.split()
#     return ' '.join(sorted(set(words), key=words.index))


# Credits to James Errico https://stackoverflow.com/questions/1806278/convert-fraction-to-float
def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        try:
            num, denom = frac_str.split('/')
        except ValueError:
            return None
        try:
            leading, num = num.split(' ')
        except ValueError:
            return float(num) / float(denom)        
        if float(leading) < 0:
            sign_mult = -1
        else:
            sign_mult = 1
        return "%.3f" % (float(leading) + sign_mult * (float(num) / float(denom)))

##################### SCRAPING FUNCTIONS
def scrap_allrecipes(website, filename, list_ingredient_to_remove, list_unique_ingredients, recipe_data, website_list_used ,unique_ingredients_data):
                                                                                                # used_0 correspond to the first website i.e allrecipes
    try:
        soup = BeautifulSoup(open(filename), "html.parser")
    except:
        #print("Beautifulsoup can't read the page:",filename)
        return recipe_data, list_unique_ingredients, unique_ingredients_data
    
    recipe_name = soup.find('span', class_='itemreviewed')
                
    #We only take recipes and not searching pages
    if recipe_name is None:
        #print("We don't care about this page: ",filename)
        return recipe_data, list_unique_ingredients, unique_ingredients_data
        
    recipe_name = recipe_name.text
    
    rating_html = soup.find('img', class_='rating')
                
    #Determine position of the ranking in the string
    start_rank = 59
    end_rank = 62
    rating = rating_html['title'][start_rank:end_rank]
          
    #print(recipe_name)
    #print(rating)
                
    #Determine the number of reviews:
    if soup.find('span', class_='count') is not None:
        review_html = soup.find('span', class_='count').text
        review = int(review_html.replace(',',''))
    else:
        review = 0
    
    #Find the preparation time:
    prepare_time = np.nan
    soup1 = soup.find('span', class_='totalTime')
    
    if soup1 is not None:
                
        prepare_time_html = soup1.find('span', class_='value-title')
        #Determine position of the time in the string
        start_prepare_time = 2
        end_prepare_time = len(prepare_time_html['title']) 
        prepare_time_not_converted = prepare_time_html['title'][start_prepare_time:end_prepare_time]
        #print("prepare time", prepare_time_not_converted)
        #If recipe is more than a day:
        if ('Day' or 'Days') in prepare_time_not_converted:
            text_to_split_on ="" 
            if 'Days' in prepare_time_not_converted:
                text_to_split_on = 'Days' 
            else:
                text_to_split_on = 'Day'
            time_analyse = prepare_time_not_converted.split(text_to_split_on)
            time_hours = time_analyse[1].split('H')
            #To convert into minutes (add the days and hours to the minutes)
            if len(time_hours) == 1:
                try:
                    prepare_time = int(time_analyse[0])*60*24 + int(time_hours[0].replace('M',''))
                except:
                    print("text time", time_analyse, " filename", filename)
                    return recipe_data, list_unique_ingredients, unique_ingredients_data
            if len(time_hours) == 2:
                time_minute = time_hours[1].replace('M','');
                prepare_time = int(time_analyse[0])*60*24 + int(time_hours[0])*60 + (int(time_minute) if time_minute else 0) 
             #If the recipe is only in hours and minutes        
        else:
            time_analyse = prepare_time_not_converted.split('H')
            #To convert hours into minutes
            if len(time_analyse) == 1:
                prepare_time = int(time_analyse[0].replace('M',''))
            if len(time_analyse) == 2:
                time_minute = time_analyse[1].replace('M','');
                prepare_time = int(time_analyse[0])*60 + (int(time_minute) if time_minute else 0)
                    
                
    #Find the ingredient list:
    list_ingred = []
    ingredients = soup.find('div', class_='ingredients')
    
    if ingredients is None:
        #print("No ingredients found :", filename)
        return recipe_data,list_unique_ingredients, unique_ingredients_data
    
    all_ingredients = ingredients.find_all('li',class_="plaincharacterwrap ingredient")
    list_units = []
    list_quantities = []
    for ingredient in all_ingredients:
        ingredient_i = ingredient.text.replace('\n','').lower()
        
        unit_i = [word for word in ingredient_i.split(' ') if word in list_measures]
        if len(unit_i) ==0:
            #print("unit not found at : ", ingredient_i.split(' '))
            #return recipe_data, list_unique_ingredients, unique_ingredients_data
            unit_i = -1.0
        else:
            unit_i  = unit_i[0]
        #print('Original:', ingredient_i)
        ingredient_i = ingredient_i.strip().split(',')[0]
        
        quantity_text = ingredient_i.split(" ")
        scraped_quantity = quantity_text[0]
        if len(quantity_text) >= 2 and "(" not in quantity_text[1] and ")" not in quantity_text[1]:
            scraped_quantity += " "+ (quantity_text[1] if "/" in quantity_text[1] else "")
            
        quantity_i = -1.0
        if len(scraped_quantity) == 0:
            quantity_i= -1.0
        else:
            try:
                quantity_i = convert_to_float((''.join([c for c in scraped_quantity.split("-")[0] if c in s_float])).strip())
            except:
                print(scraped_quantity.split("-")[0])
                quantity_i= -1.0
                
        ingredient_i = [word for word in ingredient_i.split(' ') if word not in list_ingredient_to_remove] #Clean string to only have the ingredient
        ingredient_i = ' '.join(x for x in ingredient_i if x.isalpha()) + ' '
        ingredient_i = ingredient_i.replace(' or ', '//').replace(' and ','//').replace(' with ','//').split('//') #if options, add both in the list
        #print('After removing:              ', ingredient_i,"\n")
        for ingredient_in_list in ingredient_i:
            ingredient_in_list_strip = ingredient_in_list.strip()    
            
             ### remove doubles 
            ingredient_in_list_strip = removeDoubles(ingredient_in_list_strip)
            #### don't need to add twice the amoount
            if ingredient_in_list_strip == '' or str(ingredient_in_list_strip) in list_ingred:
                continue
            ####
            
            
            if ingredient_in_list_strip[len(ingredient_in_list_strip)-1] == 's' and ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] in list_unique_ingredients:
                ingredient_in_list_strip = ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] #Remove the plural form (s) of the ingredient
             ## If the ingredient is in the list of fruit quantities scraped and something is missing
            if ingredient_in_list_strip in list_augmented and ((unit_i == -1.0) ^ (quantity_i is None or quantity_i == -1.0)):
                ## if 2 bananas, quantity is known but unit not
                if quantity_i != -1.0 and quantity_i is not None: 
                    quantity_i = float(quantity_i)*augmented_quantity_dict[ingredient_in_list_strip][0]
                    unit_i = augmented_quantity_dict[ingredient_in_list_strip][1]
                else:
                    # if quantiy is missing -1.0
                    quantity_i = -1.0
            ###
             ###############################################     
            if ingredient_in_list_strip is not None:    
                list_ingred.append(ingredient_in_list_strip) #Add the element to the ingredient list  
                
            if ingredient_in_list_strip not in list_unique_ingredients:
                list_unique_ingredients.append(ingredient_in_list_strip)
#                 print("list unique ingredient", list_unique_ingredients)
                unique_ingredients_data = unique_ingredients_data.append({'Ingredient': ingredient_in_list_strip, 'Count': 1}, ignore_index=True)
            #If ingredient already seen, increment the count of it
            else:
                ingredient_index = unique_ingredients_data[unique_ingredients_data['Ingredient']== ingredient_in_list_strip].index[0]
                unique_ingredients_data.at[ingredient_index,'Count'] = unique_ingredients_data['Count'][ingredient_index] + 1
                            
             #print(list_ingred) 
            if ingredient_in_list_strip is not None:
                list_units.append(unit_i)
                list_quantities.append(quantity_i)       
            #print(list_ingred) 
        ### add the unit and quantity at the end
#         list_units.append(unit_i)
#         list_quantities.append(quantity_i)
    recipe_data = recipe_data.append({'Website': website, 'Recipe': recipe_name,'Prepare time': prepare_time, 'Ranking': rating, 'Reviews': review,\
                                                  'Ingredients': list_ingred, 'Quantities':list_quantities, 'Units':list_units}, ignore_index=True)
    return recipe_data, list_unique_ingredients, unique_ingredients_data

## Scraping the files of the domain food.com
#def scrap_food(website, filename, list_ingredient_to_remove, list_unique_ingredients, recipe_data, website_list_used ,unique_ingredients_data):
def scrap_food(website, filename,list_ingredient_to_remove, \
                                            list_unique_ingredients, recipe_data,website_list_used,unique_ingredients_data):                                                                                             
    try:
        soup = BeautifulSoup(open(filename), "html.parser")
    except:
        #print("Beautifulsoup can't read the page (food.com):",filename)
        return recipe_data, list_unique_ingredients, unique_ingredients_data
#     soup = try_reading(filename)
#     if soup is None:
#         print("Beautifulsoup can't read the page (food.com):",filename)
#         return recipe_data, list_unique_ingredients, unique_ingredients_data                
    recipe_name = soup.find('h1', class_='fn')
                
    #We only take recipes and not searching pages
    if recipe_name is None:
#         print("No name found : We don't care about this page: ",filename)
        return recipe_data, list_unique_ingredients, unique_ingredients_data
        
    recipe_name = recipe_name.text
    
    rating = soup.find('li', {"class":"current-rating"})
    # If no rating can be found, we don't use the file
    if rating is None:
        #print("No rating found")
        return recipe_data, list_unique_ingredients, unique_ingredients_data
    rating = float(rating["style"][7:-2]) *5/100 # the review is a percentage of 5 stars storred in the attribute of a li block
    #print("rating", rating)   
    #print(recipe_name)
    #print(rating)
    if recipe_name is None:
        print("No name but rating found at the file ", filename)
    #Determine the number of reviews:
    review_html = soup.find('span', itemprop='reviewCount')
    if review_html is not None:
        review = int(review_html.text.replace(',',''))
    else:
        review = 0
    
    #Find the preparation time:
    prepare_time = np.nan
    soup1 = soup.find('h3', class_='duration')
    if soup1 is not None:
        
        words_time = soup1.text.strip().split(" ")
        len_words_time = len(words_time)
        if len_words_time %2 == 1:
            print("strange words", words_time)
        
        prepare_time = 0
        for i in range(int(len_words_time/2)):
            try : 
                prepare_time += 60**i * int(words_time[len_words_time -(1+i)*2])
            except :
                prepare_time = 0 
                print(" ERROR TIME on file ", filename, " with time ", words_time, "and text", soup1.text)            
                
    #Find the ingredient list:
    list_ingred = []
    ingredients = soup.find('div', class_='pod ingredients')
    
    if ingredients is None:
        #print("No ingredients found :", filename)
        return recipe_data,list_unique_ingredients, unique_ingredients_data
    list_units = []
    list_quantities = []
    #all_ingredients = ingredients.find_all('a')
    
    all_ingredients = ingredients.find_all('span', class_="ingredient")
    #print(all_ingredients[0].text.split())
    for ingredient in all_ingredients:
        ingredient = " ".join(ingredient.text.split())
        ingredient_i = ingredient.replace('\n','').lower()
        
        unit_i = [word for word in ingredient_i.split(' ') if word in list_measures]
        if len(unit_i) ==0:
            #print("unit not found at : ", filename)
            #return recipe_data, list_unique_ingredients, unique_ingredients_data
            unit_i = -1.0
        else:
            unit_i  = unit_i[0]
        #print('Original:', ingredient_i)
        ingredient_i = ingredient_i.strip().split(',')[0]
        
        quantity_text = ingredient_i.split(" ")
        #print(ingredient_i)
        scraped_quantity = quantity_text[0]
        if len(quantity_text) >= 2 and "(" not in quantity_text[1] and ")" not in quantity_text[1]:
            scraped_quantity += " "+ (quantity_text[1] if "/" in quantity_text[1] else "")
        #print(quantity_text[0]+" " + (quantity_text[1] if "/" in quantity_text[1] else ""))
        quantity_i = -1.0
        if len(scraped_quantity) == 0:
            quantity_i= -1.0
        else:
            try:
                quantity_i = convert_to_float((''.join([c for c in scraped_quantity.split("-")[0] if c in s_float])).strip())
            except:
                print(scraped_quantity.split("-")[0])
                quantity_i= -1.0
        
        
        #print('Original:', ingredient_i)
        ingredient_i = [word for word in ingredient_i.split(' ') if word not in list_ingredient_to_remove] #Clean string to only have the ingredient
        ingredient_i = ' '.join(x for x in ingredient_i if x.isalpha()) + ' '
        ingredient_i = ingredient_i.replace(' or ', '//').replace(' and ','//').replace(' with ','//').split('//') #if options, add both in the list
        #print('After removing:              ', ingredient_i,"\n")
        for ingredient_in_list in ingredient_i:
            ingredient_in_list_strip = ingredient_in_list.strip() 
             ### remove doubles 
            ingredient_in_list_strip = removeDoubles(ingredient_in_list_strip)
            #### don't need to add twice the amoount
            if ingredient_in_list_strip == '' or str(ingredient_in_list_strip) in list_ingred:
                continue
            ####
           
            
            if ingredient_in_list_strip[len(ingredient_in_list_strip)-1] == 's' and ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] in list_unique_ingredients:
                ingredient_in_list_strip = ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] #Remove the plural form (s) of the ingredient
                    
              ## If the ingredient is in the list of fruit quantities scraped and something is missing but only
            if ingredient_in_list_strip in list_augmented and ((unit_i == -1.0) ^ (quantity_i is None or quantity_i == -1.0)):
                ## if 2 bananas, quantity is known but unit not
                if quantity_i != -1.0 and quantity_i is not None: 
                    quantity_i = float(quantity_i)*augmented_quantity_dict[ingredient_in_list_strip][0]
                    unit_i = augmented_quantity_dict[ingredient_in_list_strip][1]
                else:
                    # if quantiy is missing -1.0
                    quantity_i = -1.0
            ###
           ###############################################     
            if ingredient_in_list_strip is not None:    
                list_ingred.append(ingredient_in_list_strip) #Add the element to the ingredient list  
            
            if ingredient_in_list_strip not in list_unique_ingredients:
                list_unique_ingredients.append(ingredient_in_list_strip)
#                 print("list unique ingredient", list_unique_ingredients)
                unique_ingredients_data = unique_ingredients_data.append({'Ingredient': ingredient_in_list_strip, 'Count': 1}, ignore_index=True)
            #If ingredient already seen, increment the count of it
            else:
                ingredient_index = unique_ingredients_data[unique_ingredients_data['Ingredient']== ingredient_in_list_strip].index[0]
                unique_ingredients_data.at[ingredient_index,'Count'] = unique_ingredients_data['Count'][ingredient_index] + 1
                    
            #print(list_ingred) 
            if ingredient_in_list_strip is not None:
                list_units.append(unit_i)
                list_quantities.append(quantity_i)
        if len(list_units) != len(list_ingred):
            print(filename)
    recipe_data = recipe_data.append({'Website': website, 'Recipe': recipe_name,'Prepare time': prepare_time, 'Ranking': rating, 'Reviews': review,\
                                                  'Ingredients': list_ingred,'Quantities':list_quantities, 'Units':list_units}, ignore_index=True)
    return recipe_data,list_unique_ingredients, unique_ingredients_data

#Scrap foodnetwork
def scrap_foodnetwork(website, filename, list_ingredient_to_remove, list_unique_ingredients, recipe_data, website_list_used ,unique_ingredients_data):
    #print('The file is a foodnetwork:', filename)                                                                                   # used_2 correspond to the first website i.e foodnetwork
    try:
        soup = BeautifulSoup(open(filename), "html.parser")
    except:
        print("Beautifulsoup can't read the page (foodnetwork):",filename)
        return recipe_data,list_unique_ingredients, unique_ingredients_data
                
    recipe_name = soup.find('h1', class_='fn')
                
    #We only take recipes and not searching pages
    if recipe_name is None:
        #print("We don't care about this page (foodnetwork): ",filename)
        return recipe_data,list_unique_ingredients, unique_ingredients_data
        
    recipe_name = recipe_name.text
    
    #print("the recipe_name is :",recipe_name)
    
    rating_html = soup.find('div', class_='rm-block lead hreview-aggregate review')
    if (rating_html is None) or (rating_html.find('div') is None):
        #print("No rating found")
        return recipe_data, list_unique_ingredients, unique_ingredients_data 
    
    #Determine the rating in the html sequence
    rating = rating_html.find('div')['title']
    #rating =  rating_html.find('div')['title']
          
    #print("the rating is:", rating)
                
    #Determine the number of reviews:
    review = 0
    if soup.find('div', class_='rm-block lead hreview-aggregate review') is not None:
        review_html = soup.find('li', class_='cta count')
        review = review_html.find('a').text
        review = [int(s) for s in review.split() if s.isdigit()]
        review = int(review[0])
    else:
        review = 0
        
    #print('The number of Reviews:',review)
    
    #Find the preparation time:
    prepare_time = np.nan
    prepare_time_html = soup.find('span', class_='value-title rspec-value-small')
    if prepare_time_html is not None:
                
        prepare_time_not_converted = prepare_time_html['title'].replace('PT','')
        
        #If recipe is more than a day:
        if ('Day' or 'Days') in prepare_time_not_converted:
            text_to_split_on ="" 
            if 'Days' in prepare_time_not_converted:
                text_to_split_on = 'Days' 
            else:
                text_to_split_on = 'Day'
            time_analyse = prepare_time_not_converted.split(text_to_split_on)
            time_hours = time_analyse[1].split('H')
            #To convert into minutes (add the days and hours to the minutes)
            if len(time_hours) == 1:
                prepare_time = int(time_analyse[0])*60*24 + int(time_hours[0].replace('M',''))
            if len(time_hours) == 2:
                time_minute = time_hours[1].replace('M','');
                prepare_time = int(time_analyse[0])*60*24 + int(time_hours[0])*60 + (int(time_minute) if time_minute else 0) 
             #If the recipe is only in hours and minutes        
        else:
            time_analyse = prepare_time_not_converted.split('H')
            #To convert hours into minutes
            if len(time_analyse) == 1:
                prepare_time = int(time_analyse[0].replace('M',''))
            if len(time_analyse) == 2:
                time_minute = time_analyse[1].replace('M','');
                prepare_time = int(time_analyse[0])*60 + (int(time_minute) if time_minute else 0)
                    
    #print('The time is:',prepare_time )           
    #Find the ingredient list:
    list_ingred = []
    ingredients = soup.find('ul', class_='kv-ingred-list1')
    if ingredients is None:
        ingredients = soup.find('ul', class_='kv-ingred-list2')  
        
    if ingredients is None:
        #print("No ingredients found :", filename)
        return recipe_data,list_unique_ingredients, unique_ingredients_data
    list_units = []
    list_quantities = []
    
    all_ingredients = ingredients.find_all('li',class_="ingredient")
    # Loop over the found ingredients
    for ingredient in all_ingredients:
        ingredient_i = ingredient.text.replace('\n','').lower()
        
        unit_i = [word for word in ingredient_i.split(' ') if word in list_measures]
        if len(unit_i) ==0:
            #print("unit not found at : ", filename)
            #return recipe_data, list_unique_ingredients, unique_ingredients_data
            unit_i = -1.0
        else:
            unit_i  = unit_i[0]
        #print('Original:', ingredient_i)
        ingredient_i = ingredient_i.strip().split(',')[0]
        
        quantity_text = ingredient_i.split(" ")
        scraped_quantity = quantity_text[0]
        if len(quantity_text) >= 2 and "(" not in quantity_text[1] and ")" not in quantity_text[1]:
            if set(quantity_text[1]) <= s_float: # if all char in quantity_text belongs to predefined character
                scraped_quantity += " "+ (quantity_text[1] if "/" in quantity_text[1] else "")
        #print(quantity_text[0]+" " + (quantity_text[1] if "/" in quantity_text[1] else ""))
        quantity_i = -1.0
        if len(scraped_quantity) == 0:
            quantity_i= -1.0
        else:
            try:
                
                quantity_i = convert_to_float((''.join([c for c in scraped_quantity.split("-")[0] if c in s_float])).strip())
            except:
                print(scraped_quantity.split("-")[0])
                quantity_i= -1.0
                
        
        #print('Original:', ingredient_i)
        
        ingredient_i = [word for word in ingredient_i.split(' ') if word not in list_ingredient_to_remove] #Clean string to only have the ingredient
        ingredient_i = ' '.join(x for x in ingredient_i if x.isalpha()) + ' '
        ingredient_i = ingredient_i.replace(' or ', '//').replace(' and ','//').replace(' with ','//').split('//') #if options, add both in the list
        #print('After removing:              ', ingredient_i,"\n")
                    
        for ingredient_in_list in ingredient_i:
            ingredient_in_list_strip = ingredient_in_list.strip()    
            
            
             ### remove doubles 
            ingredient_in_list_strip = removeDoubles(ingredient_in_list_strip)
            #### don't need to add twice the amoount
            if ingredient_in_list_strip == '' or str(ingredient_in_list_strip) in list_ingred:
                continue
            ####
            
            if ingredient_in_list_strip[len(ingredient_in_list_strip)-1] == 's' and ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] in list_unique_ingredients:
                ingredient_in_list_strip = ingredient_in_list_strip[0:len(ingredient_in_list_strip)-1] #Remove the plural form (s) of the ingredient
                
                
             ## If the ingredient is in the list of fruit quantities scraped and something is missing
            if ingredient_in_list_strip in list_augmented and ((unit_i == -1.0) ^ (quantity_i is None or quantity_i == -1.0)):
                ## if 2 bananas, quantity is known but unit not
                if quantity_i != -1.0 and quantity_i is not None: 
                    quantity_i = float(quantity_i)*augmented_quantity_dict[ingredient_in_list_strip][0]
                    unit_i = augmented_quantity_dict[ingredient_in_list_strip][1]
                else:
                    # if quantiy is missing -1.0
                    quantity_i = -1.0
            ###
                            
             ###############################################     
            if ingredient_in_list_strip is not None:    
                list_ingred.append(ingredient_in_list_strip) #Add the element to the ingredient list  
                
                
            if ingredient_in_list_strip not in list_unique_ingredients:
                list_unique_ingredients.append(ingredient_in_list_strip)
#                 print("list unique ingredient", list_unique_ingredients)
                unique_ingredients_data = unique_ingredients_data.append({'Ingredient': ingredient_in_list_strip, 'Count': 1}, ignore_index=True)
            #If ingredient already seen, increment the count of it
            else:
                ingredient_index = unique_ingredients_data[unique_ingredients_data['Ingredient']== ingredient_in_list_strip].index[0]
                unique_ingredients_data.at[ingredient_index,'Count'] = unique_ingredients_data['Count'][ingredient_index] + 1
                            
             #print(list_ingred) 
            if ingredient_in_list_strip is not None:
                list_units.append(unit_i)
                list_quantities.append(quantity_i)       

    #print(list_ingred)        
    recipe_data = recipe_data.append({'Website': website, 'Recipe': recipe_name, 'Prepare time': prepare_time, 'Ranking': rating, 'Reviews': review,\
                                                  'Ingredients': list_ingred,'Quantities':list_quantities, 'Units':list_units}, ignore_index=True)
    return recipe_data,list_unique_ingredients, unique_ingredients_data

