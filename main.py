import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


allowed_roles = ['Admin', 'CEO'] # for the admin commands
allowed_roles2= ['Staff', 'CEO', 'Admin'] # for the staff commands
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name='Banning annoying kids'))

@bot.command(name='setstatus')
async def set_status(ctx, *, status):
    # Check if the user has the required role(s)
    if any(role.name in allowed_roles for role in ctx.author.roles):
        # User has the required role, set the custom status
        await bot.change_presence(activity=discord.Game(name=status))
        await ctx.send(f'Custom status set to: {status}')
    else:
        # User does not have the required role(s)
        await ctx.send("You do not have the required role to use this command.")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.command(name='kick')
async def kick(ctx, member: discord.Member, *, reason='No reason provided'):
    if any(role.name in allowed_roles2 for role in ctx.author.roles):
        await member.kick(reason=reason)
        await ctx.send(f'AWWW Shucks {member.mention} has been kicked. `Reason: {reason}`')
    else:
        await ctx.send('You do not have the required role to use this command.')

@bot.command(name='ban')
async def ban(ctx, member: discord.Member, *, reason='No reason provided'):
    if any(role.name in allowed_roles for role in ctx.author.roles):
        await member.ban(reason=reason)
        await ctx.send(f'Tough luck {member.mention} has been banned, Better luck next time. `Reason: {reason}`')
    else:
        await ctx.send('You do not have the required role to use this command.')

@bot.command(name='unban')
async def unban(ctx, *, member):
    if any(role.name in allowed_roles for role in ctx.author.roles):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} has been unbanned.')
                return

        await ctx.send(f'User with the name {member} not found in the ban list.')
    else:
        await ctx.send('You do not have the required role to use this command.')

@bot.command(name='clear')
async def clear(ctx, amount=5):
    if any(role.name in allowed_roles for role in ctx.author.roles):
        await ctx.channel.purge(limit=amount + 1)
    else:
        await ctx.send('You do not have the required role to use this command.')

@bot.command(name='userinfo', aliases=['ui'])
async def user_info(ctx, member: discord.Member = None):
    # If no member is specified, default to the author
    member = member or ctx.author

    # Create an embed to display user information
    embed = discord.Embed(title=f'{member.name}#{member.discriminator}', color=member.color)
    embed.add_field(name='ID', value=member.id, inline=False)
    embed.add_field(name='Nickname', value=member.display_name, inline=False)
    embed.add_field(name='Joined Server', value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name='Account Created', value=member.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name='Roles', value=', '.join(role.name for role in member.roles[1:]), inline=False)
    embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}')

    await ctx.send(embed=embed)

@bot.command(name='addrole')
async def add_role(ctx, member: discord.Member, role_name):
    # Check if the user has the allowed role to use the addrole command
    if any(role.name in allowed_roles for role in ctx.author.roles):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            print(f'Found role: {role.name}')
            if role not in member.roles:
                await member.add_roles(role)
                await ctx.send(f'{member.mention} has been given the role: {role_name}')
            else:
                await ctx.send(f'{member.mention} already has the role: {role_name}')
        else:
            print(f'Role {role_name} not found in the server.')
            await ctx.send(f'Role {role_name} not found.')
    else:
        await ctx.send('You do not have the required role to use this command.')

@bot.command(name='removerole')
async def remove_role(ctx, member: discord.Member, role_name):
    # Check if the user has the allowed role to use the removerole command
    if any(role.name in allowed_roles for role in ctx.author.roles):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            print(f'Found role: {role.name}')
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f'{member.mention} no longer has the role: {role_name}')
            else:
                await ctx.send(f'{member.mention} does not have the role: {role_name}')
        else:
            print(f'Role {role_name} not found in the server.')
            await ctx.send(f'Role {role_name} not found.')
    else:
        await ctx.send('You do not have the required role to use this command.')

@bot.command(name='MODcommands')
async def show_embed(ctx):
    # Creating an embed object
    embed = discord.Embed(
        title='These are all the commands for the C1baby Mod (Must be Staff)',
        description='!kick <mention user> <reason> | this will kick a member from the server `(within reason for exaple self promo, things like rudeness and spamming is a timeout)` \n \n !MODcommands | Will bring up this pannel \n \n  !userinfo <mention member> | this will look up any member of the server \n \n !ADMINcommands | Only for admins ', 
        
        color=discord.Color.dark_purple()  # You can set the color of the embed
    )

    # Sending the embed message
    await ctx.send(embed=embed)

@bot.command(name='ADMINcommands')
async def show_embed(ctx):
    # Creating an embed object
    embed = discord.Embed(
        title='These are all the commands for the C1baby Mod (Must be Admin)',
        description='!kick <mention user> <reason> | this will kick a member from the server `(within reason for exaple self promo, things like rudeness and spamming is a timeout)` \n \n !ban <mention user> <Reason> | Bans someone from the server \n \n !clear <amount of messages to delete> | Purges messages in a channel \n \n !addrole <mention user> <role name> | Add a role to a member of the server \n \n !removerole <mention user> <role name> | Removes a role to a member of the server ',
        
        color=discord.Color.dark_purple()  # You can set the color of the embed
    )

    # Sending the embed message
    await ctx.send(embed=embed)

bot.run('ENTER BOT TOKEN HERE')
