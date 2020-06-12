##############################################----Runs Light Furys token----##################################################################
import discord
import mysql.connector
import random

from discord.ext import commands,tasks
from discord.ext.commands import has_permissions , Bot

client = commands.Bot(command_prefix = '?')

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Dheeru@1612",
    database ="discord_levels_test",
    auth_plugin = "mysql_native_password"
)


def generate_xp():
    return random.randint(1,3)

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle , activity = discord.Game("Havana"))
    print("Bot is ready")
    print(mydb)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.lower() == "?help":
        pass
    elif message.content.lower() == "?addrole":
        pass 
    else:
        xp = generate_xp()
        cursor = mydb.cursor()
        cursor.execute("SELECT User_XP,User_lvl from users WHERE Client_ID = "+ str(message.author.id))
        result = cursor.fetchall()
        
        if(len(result) == 0):
            print("User is not in database, adding them....")
            print(message.author.name + " recieved " + str(xp)+"xp as starting bonus!!!")
            cursor.execute("INSERT into users(Client_ID,User_XP) VALUES("+str(message.author.id)+","+str(xp)+")")
            mydb.commit()
            print("Inserted user details")
        
        else:
            new_xp = result[0][0] + xp
            cursor.execute("UPDATE users SET User_XP = "+str(new_xp)+" WHERE Client_ID = "+str(message.author.id))
            print("Updated xp of user : "+message.author.name+" to " +str(new_xp))
            next_lvl = int(result[0][0] ** (1/3))
            if( next_lvl > result[0][1]):
                cursor.execute("UPDATE users SET User_lvl = "+str(next_lvl)+" WHERE Client_ID = "+str(message.author.id))
                embed=discord.Embed(title="Level UP! "+str(message.author.mention), description=(message.author.name+" reached Level "+str(next_lvl)+". Keep Going"), color=0xff00f6)
                await message.channel.send( embed = embed )
            mydb.commit()
    await client.process_commands(message)

@client.command(name = '8ball', pass_context = True , aliases = ["test","_ball"])
async def eight_ball(context,*,qustion):
    # Imports
    import random
    print("Trigerred 8ball Reponse to", context)
    possible_responses=['As I see it, yes',
    'Ask again later',
    'Better not tell you now',
    'Cannot predict now',
    'Concentrate and ask again', 
    'Don’t count on it',
    'It is certain',
    'It is decidedly so',
    'Most likely',
    'My reply is no',
    'My sources say no',
    'Outlook not so good',
    'Outlook good',
    'Reply hazy, try again',
    'Signs point to yes',
    'Very doubtful',
    'Without a doubt',
    'Yes',
    'Yes – definitely',
    "You may rely on it"]
    await context.channel.send(random.choice(possible_responses) + context.message.author.mention)
    return

client.run("NzE3MzkyNzIwMTA0MjU5NjE0.XtZqLg.ChRLy7LuhArMNo2bNLenkZq2LYs")

