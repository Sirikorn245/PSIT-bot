import discord
from discord import client
from discord.ext import commands
import json
import os
import random

os.chdir("C:\\Users\\LENOVO\\OneDrive\\เดสก์ท็อป\\project")

client = commands.Bot(command_prefix='e!')

@client.event
async def on_ready() :
    print("Bot Started!")

@client.command()
async def balance(ctx): #เช็กยอดคงเหลือ
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"] 

    em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.dark_gold())
    em.add_field(name="Wallet balance", value=wallet_amt)
    em.add_field(name="Bank balance", value=bank_amt)
    await ctx.send(embed = em)

@client.command()
async def beg(ctx): #เสี่ยงดวง
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(-1000, 1001, 10)

    if earnings > 0:
        await ctx.send(f"You recieve {earnings} coins!")
    elif earnings < 0:
        await ctx.send(f"Oops! You lose {-earnings} coins!")
    else:
        await ctx.send(f"Go beg your father ka bitch")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

@client.command()
async def withdraw(ctx, amount = None): #ถอนเงิน
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the amount.")
        return
    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[1]:
        await ctx.send("You don't have enough money;)")
        return
    if amount < 0:
        await ctx.send("Amount must more than zero.")
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -amount, "bank")

    await ctx.send(f"You withdrew {amount} coins!")

@client.command()
async def deposit(ctx, amount = None): #ฝากเงิน
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the amount.")
        return
    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[0]:
        await ctx.send("You don't have enough money;)")
        return
    if amount < 0:
        await ctx.send("Amount must more than zero.")
        return

    await update_bank(ctx.author, -amount)
    await update_bank(ctx.author, amount, "bank")

    await ctx.send(f"You deposited {amount} coins!")

async def open_account(user): #เปิดบัญชี

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users

async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal

client.run('ODk4ODI4NzE4MDMyNjk1Mjk2.YWp5eQ.Pw0cdTIqvVaEwA5zlmf_CcGCR-I')