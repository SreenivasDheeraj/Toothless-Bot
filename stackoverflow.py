from selenium import webdriver 

# Taking input from user 
search_string = input("Input the URL or string you want to search for:") 

# This is done to structure the string 
# into search url.(This can be ignored) 
search_string = search_string.replace(' ', '+') 

# Assigning the browser variable with chromedriver of Chrome. 
# Any other browser and its respective webdriver  
browser = webdriver.Chrome('chromedriver')   #this only for chrome 

for i in range(1): 
	matched_elements = browser.get("https://www.stackoverflow.com/search?q=" +
									search_string + "&start=" + str(i)) 



import random

###Dice Simulation###
@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int):
    dice = [
        str(random.choice(range(1, 7)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))