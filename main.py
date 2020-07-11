import discord, datetime, nekos, random
import sqlite3
from discord.ext import commands

PREFIX = '-'
client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )
# Префикс кмд


connect = sqlite3.connect('server.db')
cursor = connect.cursor()


hello_cmd = [ 'hello', 'hi', 'привет', 'privet', 'прив', 'priv', 'ky', 'ку', 'здарова'  ]
answer_cmd = [ '-инфа', '-инфа о сервере', '-info', '-information' ]


@client.event
async def on_ready():
    print( 'Бот работает' )

    await client.change_presence( status = discord.Status.online, activity = discord.Game( 'http://bot.botbukkin.tk/bot/' ) )
    cursor.execute("""CREATE TABLE IF NOT EXISTS users  (
        name TEXT,
        id INT,
        cash BIGINT,
        rep INT,
        lvl INT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
        role_id INT,
        id INT,
        cost BIGINT
    )""")


    for guild in client.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ( ' {member} ', {member.id}, 0, 0, 1)")

            else:
                pass
    connect.commit()




@client.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1)")
        connect.commit()
    else:
        pass


@client.command(aliases = ['balance', 'cash'])
async def __balance(ctx, member: discord.Member = None):
    if member is None:
        emb = discord.Embed( description = f"""Баланс юзера: **{ctx.author}** состовляет: **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}  :leaves:**""", colour = discord.Color.red() )
        await ctx.send(embed = emb)
    else:
        emb2 = discord.Embed( description = f"""Баланс юзера: **{member}** состовляет: **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]}  :leaves:**""", colour = discord.Color.red() )
        await ctx.send(embed = emb2)

@client.command(aliases = ['lvl'])
async def __lvl(ctx, member: discord.Member = None):
    if member is None:
        emb = discord.Embed( description = f"""Левел юзера: **{ctx.author}** состовляет: **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**""", colour = discord.Color.red() )
        await ctx.send(embed = emb)
    else:
        emb2 = discord.Embed( description = f"""Левел юзера: **{member}** состовляет: **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**""", colour = discord.Color.red() )
        await ctx.send(embed = emb2)


@client.command(aliases = ['award'])
@commands.has_permissions( manage_messages = True )
async def __award(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        await ctx.send(f"**{ctx.author.mention}**, укажите юзера что бы выдать ему :leaves:")
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author.mention}**, укажите сумму которую хотите выдать человеку")
        elif amount < 1:
            await ctx.send(f"**{ctx.author.mention}**, укажите сумму 1 или выше!")
        else:
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
            connect.commit()

            await ctx.message.add_reaction('✅')

@client.command(aliases = ['add-shop'])
@commands.has_permissions( administrator = True )
async def __add_shop(ctx, role: discord.Role = None, cost: int = None):
    if role is None:
        await ctx.send(f"**{ctx.author.mention}**, укажите роль которую хотите внести в магазин!")
    else:
        if cost is None:
            await ctx.send(f"**{ctx.author.mention}**, укажите цену для роли!")
        elif cost < 1:
            await ctx.send(f"**{ctx.author.mention}**, стоимость может быть тока 1 или выше!")
        else:
            cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
            connect.commit()
            await ctx.message.add_reaction('✅')

@client.command(aliases = ['remove-shop'])
@commands.has_permissions( administrator = True )
async def __remove_shop(ctx, role: discord.Role = None):
    if role is None:
        await ctx.send(f"**{ctx.author.mention}**, укажите роль которую хотите удалить из магазина!")
    else:
        cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
        connect.commit()
        await ctx.message.add_reaction('✅')

@client.command(aliases = ['shop'])
async def __shop(ctx):
    embed = discord.Embed(title = 'Магазин сервера')

    for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
        if ctx.guild.get_role(row[0]) != None:
            embed.add_field(
                name = f"Стоимость {row[1]}",
                value = f"Вы преобрете роль {ctx.guild.get_role(row[0]).mention}",
                inline = False
            )

        else:
            pass
    await ctx.send(embed = embed)
@client.command(aliases = ['buy'])
async def __buy(ctx, role: discord.Role):
    if role is None:
        await ctx.send(f"**{ctx.author.mention}**, укажите роль которую хотите преобрести")
    else:
        if role in ctx.author.roles:
            await ctx.send(f"**{ctx.author.mention}**, данная роль у вас уже есть!")
        elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
            await ctx.send(f"**{ctx.author.mention}, у вас нет денег для данной роли!!**")
        else:
            await ctx.author.add_roles(role)
            cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
            await ctx.message.add_reaction('✅')
            connect.commit()



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
    emb.add_field( name = '{}user'.format( PREFIX ), value = 'Информация о игроке' )
    emb.add_field( name = '{}avatar'.format( PREFIX ), value = 'Рандом аниме аватар' )
    emb.add_field( name = '{}add-shop'.format( PREFIX ), value = 'Добавление ролей в магазин' )
    emb.add_field( name = '{}remove-shop'.format( PREFIX ), value = 'Удаление ролей из магазина' )
    emb.add_field( name = '{}award'.format( PREFIX ), value = 'Выдать денег' )
    emb.add_field( name = '{}buy'.format( PREFIX ), value = 'Купить роль' )
    emb.add_field( name = '{}shop'.format( PREFIX ), value = 'Магазин ролей' )
    emb.add_field( name = '{}balance'.format( PREFIX ), value = 'Узнать свой баланс' )
    emb.add_field( name = '{}lvl'.format( PREFIX ), value = 'Узнать свой лвл' )
    emb.add_field( name = 'Информация', value = 'Более о кмд и правах: http://bot.botbukkin.tk/bot/' )

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

@client.command(aliases=['юзер', 'юзеринфо', 'user'])
async def __userinfo(ctx, member: discord.Member):
    roles = member.roles
    role_list = ""
    for role in roles:
        role_list += f"<@&{role.id}> "
    emb = discord.Embed(title=f'Информация о пользователе {member}', colour = 0x179c87)
    emb.set_thumbnail(url=member.avatar_url)
    emb.add_field(name='ID', value=member.id)
    emb.add_field(name='Ник', value=member.name)
    emb.add_field(name='Высшая роль', value=member.top_role)
    emb.add_field(name='Дискриминатор', value=member.discriminator)
    emb.add_field(name='Присоеденился к серверу', value=member.joined_at.strftime('%Y.%m.%d \n %H:%M:%S'))
    emb.add_field(name='Присоеденился к Discord', value=member.created_at.strftime("%Y.%m.%d %H:%M:%S"))
    emb.add_field(name='Роли', value=role_list)
    emb.set_footer(text='Вызвал команду: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed = emb)

@client.command(  )
@commands.has_permissions( manage_messages = True )
async def ad( ctx, arg ):
    await ctx.channel.purge( limit = 1 )
    emb = discord.Embed(title='Advert', colour = 0x1555bd)
    emb.add_field(name='Объявление!!', value = f'{ arg }' )
    await ctx.send(embed = emb)

@client.command()
async def avatar(ctx):
    emb = discord.Embed(description= 'Вот подобраная Вам аватарка.', color=0x6fdb9e)
    emb.set_image(url=nekos.img('avatar'))
    await ctx.send(embed=emb)

@client.command()
async def roll(ctx):
    a = 1
    b = 100
    rand = random.randint(a, b)
    emb = discord.Embed(title='Random', colour = 0x1555bd)
    emb.add_field(name='Random Int', value = f'Выпало число: { rand }' )
    await ctx.send(embed = emb)


TOKEN = open( 'token.bkl', 'r' ).readline()
client.run( TOKEN )
