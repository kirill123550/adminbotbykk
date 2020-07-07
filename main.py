import discord, datetime
from discord.ext import commands

PREFIX = '-'
client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )
# Префикс кмд



hello_cmd = [ 'hello', 'hi', 'привет', 'privet', 'прив', 'priv', 'ky', 'ку', 'здарова'  ]
answer_cmd = [ '-инфа', '-инфа о сервере', '-info', '-information' ]


@client.event
async def on_ready():
    print( 'Бот работает' )

    await client.change_presence( status = discord.Status.online, activity = discord.Game( 'AdminBot by kirill_kochurov' ) )

@client.event
async def on_command_error( ctx, error ):
    pass


@client.event
async def on_message( message ):
    await client.process_commands( message )
    msg = message.content.lower()

    if msg in hello_cmd:
        await message.channel.send( 'Привет!' )

    if msg in answer_cmd:
        await message.channel.send( 'В разработке' )

# Clear message
@client.command( pass_context = True )
@commands.has_permissions( manage_messages = True )
async def clear( ctx, amount = 100 ):
    await ctx.channel.purge( limit = amount )

# Kick command
@client.command( pass_context = True )
@commands.has_permissions( kick_members = True )
async def kick( ctx, member: discord.Member, *, reason = 'Kicked user reason for administration' ):
    emb = discord.Embed( title = 'Kick', colour = discord.Color.red() )
    await ctx.channel.purge( limit = 1 )

    await member.kick( reason = reason )
    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.add_field( name = 'Кик юзера', value = 'Юзер : {}'.format( member.mention ) )
    emb.add_field( name = 'Reason', value = f'Reason: {reason}' )

    await ctx.send( embed = emb )
    #await ctx.send( f'Кикнут юзер: { member.mention } Причина: { reason }' )

# Ban
@client.command( pass_context = True )
@commands.has_permissions( ban_members = True )
async def ban( ctx, member: discord.Member, *, reason = 'Banned user reason for administration' ):
    emb = discord.Embed( title = 'Ban', colour = discord.Color.red() )
    await ctx.channel.purge( limit = 1 )
    await member.ban( reason = reason )

    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.add_field( name = 'Ban user', value = 'Banned User : {}'.format( member.mention ) )
    emb.add_field( name = 'Reason', value = f'Reason: {reason}' )

    await ctx.send( embed = emb )
    #await ctx.send( f'Забанен юзер: { member.mention } Причина: { reason }' )

# Unban
@client.command( pass_context = True )
@commands.has_permissions( ban_members = True )
async def unban( ctx, *, member ):

    await ctx.channel.purge( limit = 1 )

    banned_users = await ctx.guild.bans()

    for ban_e in banned_users:
        emb = discord.Embed( title = 'Unban', colour = discord.Color.green() )
        user = ban_e.user

        await ctx.guild.unban( user )
        emb.add_field( name = 'Разбанен юзер', value = f'Юзер: { user.mention }' )
        await ctx.send( embed = emb )

#        #await ctx.send( f'Разбанен юзер: { user.mention }' )

        return

# Prefix
#@client.command( pass_context = True )
#@commands.has_permissions( administrator = True )
#async def prefix( ctx, arg ):
#    global PREFIX = arg
#    await ctx.send( f'Теперь префикс не сервере:  { arg }' )

# Command help
@client.command( pass_context = True )
async  def help( ctx ):
    await ctx.channel.purge( limit = 1 )
    emb = discord.Embed( title = 'Навигация по командам', colour = discord.Color.green() )

    emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
    emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Отчиска чата' )
    emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Кик юзера' )
    emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Бан юзера' )
    emb.add_field( name = '{}unban'.format( PREFIX ), value = 'Разбан юзера' )
    emb.add_field( name = '{}test_enb'.format( PREFIX ), value = 'Сам перейди и узнаешь' )
    emb.add_field( name = '{}send_a'.format( PREFIX ), value = 'Просто напиши  :)' )

    await ctx.send( embed = emb )

@client.command( pass_context = True )
async def test_emb( ctx ):
    emb = discord.Embed( title = 'Embed на заказ(для бота цена: 0 руб!)', colour = discord.Color.green(), url = 'https://vk.com/kirill_kochurov' )
    emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )

    now_date = datetime.datetime.now()
    emb.add_field( name = 'Time', value = 'Time : {}'.format( now_date ) )
    await ctx.send( embed = emb )

@client.command(  )
async def send_a( ctx ):
    await ctx.author.send( 'Hello World' )

@client.command(  )
async def send_m( ctx, member: discord.Member, arg ):
    await ctx.channel.purge( limit = 1 )
    await member.send( f'{ member.name }, { arg }' )

TOKEN = open( 'token.bkl', 'r' ).readline()

client.run( TOKEN )
