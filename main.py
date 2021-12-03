import discord
import json
import os
from discord import client
from discord.ext import commands

bot = commands.Bot(command_prefix = "-", description = "Bot discord")

@bot.event 
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        type=discord.ActivityType.playing, name="-help/Koze bot.py"
    ))
    print("Bot Ready !")


#----------------------------------------------------------------------------------------------
@bot.command()
async def Info(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    numberOfPerson = server.member_count
    serverName = server.name
    message = (f"Vous être accuelement sur un serveur qui se nomme **{serverName}** !\nCe serveur comporte **{numberOfPerson}** de joueur/e qui vous attende pour discuter !\nIl est aussi composé de **{numberOfTextChannels}** salon écris ainsi que **{numberOfVoiceChannels}** salon vocaux !")
    await ctx.send(message)

@bot.command()
async def serverInfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	serverDescription = server.description
	numberOfPerson = server.member_count
	serverName = server.name
	message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes ! \nLa description du serveur est {serverDescription}. \nCe serveur possède {numberOfTextChannels} salons écrit et {numberOfVoiceChannels} salon vocaux."
	await ctx.send(message)


@bot.command()
async def chinese(ctx, *text):
	chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
	chineseText = []
	for word in text:
		for char in word:
			if char.isalpha():
				index = ord(char) - ord("a")
				transformed = chineseChar[index]
				chineseText.append(transformed)
			else:
				chineseText.append(char)
		chineseText.append(" ")
	await ctx.send("".join(chineseText))

@bot.command()
async def userinfo(ctx, member: discord.Member = None):

    member = ctx.author if not member else member

    roles = [role for role in member.roles]


    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Nom:", value=member.display_name)

    embed.add_field(name="Crée à:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Join à:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role", value=member.top_role.mention)
    
    embed.add_field(name="Bot ?", value=member.bot)

    await ctx.send(embed=embed)

    



#----------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
	await ctx.guild.ban(user, reason = reason)
	embed = discord.Embed(title = "**Banissement**", description = "Un modérateur a frappé !", url = "https://discord.com/api/oauth2/authorize?client_id=909547587156185088&permissions=8&scope=bot", color=0xfa8072)
	embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://discord.com/api/oauth2/authorize?client_id=909547587156185088&permissions=8&scope=bot")
	embed.set_thumbnail(url = "https://discordemoji.com/assets/emoji/BanneHammer.png")
	embed.add_field(name = "Membre banni", value = user.name, inline = True)
	embed.add_field(name = "Raison", value = reason, inline = True)
	embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
	
	await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
	await ctx.guild.kick(user, reason = reason)
	embed = discord.Embed(title = "**Kick**", description = "Un modérateur a frappé !", url = "https://discord.com/api/oauth2/authorize?client_id=909547587156185088&permissions=8&scope=bot", color=0xfa8072)
	embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://discord.com/api/oauth2/authorize?client_id=909547587156185088&permissions=8&scope=bot")
	embed.set_thumbnail(url = "https://discordemoji.com/assets/emoji/BanneHammer.png")
	embed.add_field(name = "Membre kick", value = user.name, inline = True)
	embed.add_field(name = "Raison", value = reason, inline = True)
	embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
	
	await ctx.send(embed = embed)
    

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason = reason)
            await ctx.send(f"{user} à été unban.")
            return

    await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    for message in messages:
        await message.delete()
       
async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)


@bot.command()
@commands.has_permissions(manage_messages = True)
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")


@bot.command()
@commands.has_permissions(manage_messages = True)
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("Cette command n'existe pas, désoler !")

	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Il manque un argument.")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("Vous n'avez pas les permissions pour faire cette commande.")
	elif isinstance(error, commands.CheckFailure):
		await ctx.send("Oups vous ne pouvez utilisez cette commande\n.")
	if isinstance(error.original, discord.Forbidden):
		await ctx.send("Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande !\nveuiller réaisailler plus tard.")
#---------------------------------------------------------------------------------------------------



    



bot.run("TOCKEN")