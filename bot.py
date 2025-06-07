import discord
from discord.ext import commands
from discord.ui import Select, View
from datetime import timedelta

# Configuration
OWNER_ID = 1296982056966033469
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='+', intents=intents)

# Variables pour stocker le préfixe et la couleur
dynamic_prefix = '+'
dynamic_color = 0x000000
owners = {OWNER_ID}

# Préfixe dynamique
@bot.event
async def on_guild_join(guild):
    bot.command_prefix = dynamic_prefix

def get_prefix(bot, message):
    return dynamic_prefix

bot.command_prefix = get_prefix

# Vérification si l'utilisateur est propriétaire
def is_owner():
    async def predicate(ctx):
        return ctx.author.id in owners
    return commands.check(predicate)

# Commandes

@bot.command()
@is_owner()
async def prefix(ctx, *, new_prefix: str):
    global dynamic_prefix
    dynamic_prefix = new_prefix
    await ctx.message.delete()
    embed = discord.Embed(
        title="Préfixe changé",
        description=f"Le préfixe a été changé en : `{new_prefix}`",
        color=dynamic_color
    )
    await ctx.send(embed=embed)

@bot.command()
@is_owner()
async def owner(ctx, user: discord.User):
    owners.add(user.id)
    await ctx.message.delete()
    embed = discord.Embed(
        title="Propriétaire ajouté",
        description=f"{user.mention} est maintenant propriétaire du bot.",
        color=dynamic_color
    )
    await ctx.send(embed=embed)

@bot.command()
@is_owner()
async def unowner(ctx, user: discord.User):
    if user.id == OWNER_ID:
        await ctx.send("Impossible de retirer le propriétaire principal.")
        return
    owners.discard(user.id)
    await ctx.message.delete()
    embed = discord.Embed(
        title="Propriétaire retiré",
        description=f"{user.mention} n'est plus propriétaire du bot.",
        color=dynamic_color
    )
    await ctx.send(embed=embed)

@bot.command()
@is_owner()
async def name(ctx, *, new_name: str):
    try:
        await bot.user.edit(username=new_name)
        await ctx.message.delete()
        embed = discord.Embed(
            title="Nom du bot changé",
            description=f"Le nom du bot a été changé en : {new_name}",
            color=dynamic_color
        )
        await ctx.send(embed=embed)
    except discord.HTTPException as e:
        await ctx.send(f"Une erreur est survenue : {e}")

@bot.command()
@is_owner()
async def setpic(ctx):
    if not ctx.message.attachments:
        await ctx.send("Veuillez joindre une image.")
        return
    avatar = await ctx.message.attachments[0].read()
    await bot.user.edit(avatar=avatar)
    await ctx.message.delete()
    embed = discord.Embed(
        title="Avatar du bot mis à jour",
        description="L'avatar du bot a été mis à jour avec succès.",
        color=dynamic_color
    )
    await ctx.send(embed=embed)

@bot.command()
@is_owner()
async def theme(ctx, hex_color: str):
    global dynamic_color
    try:
        dynamic_color = int(hex_color.strip('#'), 16)
        await ctx.message.delete()
        embed = discord.Embed(
            title="Couleur des embeds changée",
            description=f"La couleur des embeds a été changée en : #{hex_color}",
            color=dynamic_color
        )
        await ctx.send(embed=embed)
    except ValueError:
        await ctx.send("Couleur invalide. Utilisez un format hexadécimal comme `#000000`.")

@bot.command()
@is_owner()
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.message.delete()
    embed = discord.Embed(
        title="Salon verrouillé",
        description=f"Le salon {ctx.channel.mention} a été verrouillé.",
        color=dynamic_color
    )
    await ctx.send(embed=embed)

@bot.command()
@is_owner()
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.message.delete()
    embed = discord.Embed(
        title="Salon déverrouillé",
        description=f"Le salon {ctx.channel.mention} a été déverrouillé.",
        color=dynamic_color
    )
    await ctx.send(embed=embed)

@bot.command()
@is_owner()
async def hide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.message.delete()
    embed = discord.Embed(
        title="Salon caché",
        description=f"Le salon {ctx.channel.mention} a été caché.",
        color=dynamic_color
    )
    await ctx.send(embed=embed)

@bot.command()
@is_owner()
async def unhide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.message.delete()
    embed = discord.Embed(
        title="Salon visible",
        description=f"Le salon {ctx.channel.mention} est à nouveau visible.",
        color=dynamic_color
    )
    await ctx.send(embed=embed)

@bot.command()
@is_owner()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.message.delete()
    embed = discord.Embed(
        title="Messages supprimés",
        description=f"{amount} messages ont été supprimés.",
        color=dynamic_color
    )
    await ctx.send(embed=embed, delete_after=5)

@bot.command()
@is_owner()
async def warn(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Avertissement",
        description=f"{member.mention} a été averti pour : {reason}",
        color=dynamic_color
    )
    await ctx.send(embed=embed)

@bot.command()
@is_owner()
async def timeout(ctx, member: discord.Member, seconds: int):
    try:
        timeout_duration = discord.utils.utcnow() + timedelta(seconds=seconds)
        await member.timeout(timeout_duration, reason=f"Timeout par {ctx.author}")
        await ctx.message.delete()
        embed = discord.Embed(
            title="Utilisateur en Timeout",
            description=f"{member.mention} a été mis en mute pour {seconds} secondes.",
            color=dynamic_color
        )
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("Je n'ai pas la permission de mettre cet utilisateur en timeout.")

@bot.command()
@is_owner()
async def say(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
@is_owner()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} a été expulsé du serveur. Raison : {reason if reason else 'Aucune raison spécifiée.'}")
        except discord.Forbidden:
            await ctx.send("Je n'ai pas la permission d'expulser cet utilisateur.")
        except discord.HTTPException:
            await ctx.send("Une erreur s'est produite lors de l'expulsion.")
    else:
        await ctx.send("Vous n'avez pas la permission d'expulser un membre.")


@bot.command()
async def aide(ctx):
    embed = discord.Embed(
        title="Menu d'aide",
        description="**Utilisez le menu déroulant pour explorer et sélectionner** un __thème adapté__ à vos **préférences**. __Chaque choix applique instantanément__ **un style unique**, *offrant une personnalisation rapide et facile de l'apparence*.",
        color=dynamic_color
    )
    embed.set_footer(text="Bot Chatgpt")
    embed.set_image(url="")

    select = Select(
        placeholder="Choisissez un thème",
        options=[
            discord.SelectOption(label="Modération", description="Commandes de gestion de serveur", emoji="\ud83d\udd12"),
            discord.SelectOption(label="Utilitaire", description="Commandes générales", emoji="\u2699\ufe0f"),
            discord.SelectOption(label="Réglage", description="Commandes pour configurer le bot", emoji="\ud83c\udf10")
        ]
    )

    async def callback(interaction):
        if select.values[0] == "Modération":
            mod_embed = discord.Embed(
                title="Commandes de Modération",
                description=( 
                    "**`lock`** : Verrouille un salon.\n"
                    "**`unlock`** : Déverrouille un salon.\n"
                    "**`ban`** : Bannit un utilisateur.\n"
                    "**`unban`** : Débannit un utilisateur.\n"
                    "**`bl`** : Ajoute un utilisateur à la liste noire.\n"
                    "**`unbl`** : Retire un utilisateur de la liste noire.\n"
                    "**`warn`** : Avertit un utilisateur.\n"
                    "**`warnlist`** : Liste les avertissements.\n"
                    "**`delwarn`** : Supprime les avertissements d'un utilisateur.\n"
                    "**`derank`** : Retire tous les rôles d'un utilisateur.\n"
                    "**`addrole`** : Ajoute un rôle à un utilisateur.\n"
                    "**`delrole`** : Retire un rôle d'un utilisateur.\n"
                    "**`timeout`** : Met un utilisateur en timeout.\n"
                    "**`kick`** : Expulse un utilisateur du serveur."
                ),
                color=dynamic_color
            )
            await interaction.response.edit_message(embed=mod_embed, view=view)
        elif select.values[0] == "Utilitaire":
            util_embed = discord.Embed(
                title="Commandes Utilitaires",
                description=(
                    "**`clear`** : Supprime un nombre défini de messages.\n"
                    "**`renew`** : Recrée un salon en le remettant à neuf.\n"
                    "**`massiverole`** : Ajoute un rôle à tous les membres du serveur."
                ),
                color=dynamic_color
            )
            await interaction.response.edit_message(embed=util_embed, view=view)
        elif select.values[0] == "Réglage":
            settings_embed = discord.Embed(
                title="Commandes de Réglage",
                description=(
                    "**`prefix`** : Change le préfixe du bot.\n"
                    "**`owner`** : Ajoute un propriétaire.\n"
                    "**`unowner`** : Retire un propriétaire.\n"
                    "**`name`** : Change le nom du bot.\n"
                    "**`setpic`** : Change l'avatar du bot.\n"
                    "**`theme`** : Change la couleur des embeds.\n"
                    "**`statuts`** : Affiche le statut actuel du bot.\n"
                    "**`activity`** : Change l'activité du bot (jeu, écoute, etc.)."
                ),
                color=dynamic_color
            )
            await interaction.response.edit_message(embed=settings_embed, view=view)

    select.callback = callback
    view = View()
    view.add_item(select)
    await ctx.send(embed=embed, view=view)

@bot.command()
@is_owner()
async def statuts(ctx):
    status = bot.presence.activity  # Accéder à l'activité actuelle du bot
    if status is None:
        await ctx.send("Le bot n'a actuellement aucune activité définie.")
    else:
        await ctx.send(f"Le statut actuel du bot est : {status.name} ({status.type})")


@bot.command()
@is_owner()
async def activity(ctx, type: str, *, name: str):
    """Change l'activité du bot."""
    valid_types = ['playing', 'listening', 'watching', 'streaming']
    type = type.lower()

    if type not in valid_types:
        await ctx.send(f"Type d'activité invalide. Choisissez parmi : {', '.join(valid_types)}.")
        return

    if type == "streaming":
        # Le type "streaming" nécessite une URL de stream
        url = "https://www.twitch.tv/yourstream"  # Vous pouvez modifier l'URL du stream
        await bot.change_presence(activity=discord.Streaming(name=name, url=url))
        await ctx.send(f"Le bot est maintenant en streaming avec l'activité : {name}.")
    else:
        await bot.change_presence(activity=discord.Activity(type=getattr(discord.ActivityType, type), name=name))
        await ctx.send(f"L'activité du bot a été changée en {type} : {name}.")




@bot.command()
async def helpstatuts(ctx):
    embed = discord.Embed(
        title="Aide pour la commande `statuts`",
        description=(
            "**`statuts`** : Cette commande permet d'afficher le statut actuel du bot.\n\n"
            "Le statut est l'activité à laquelle le bot participe (ex : 'Playing', 'Listening', etc.).\n\n"
            "Syntaxe :\n"
            "`+statuts`\n\n"
            "Cela vous montrera l'activité actuelle du bot, ou vous informera si aucune activité n'est définie."
        ),
        color=dynamic_color
    )
    await ctx.send(embed=embed)

@bot.command()
async def helpactivity(ctx):
    embed = discord.Embed(
        title="Aide pour la commande `activity`",
        description=(
            "**`activity`** : Cette commande permet de changer l'activité du bot.\n\n"
            "Vous pouvez choisir parmi plusieurs types d'activités : 'playing', 'listening', 'watching', et 'streaming'.\n\n"
            "Syntaxe :\n"
            "`+activity <type> <nom de l'activité>`\n\n"
            "Types d'activités disponibles :\n"
            "- `playing` : Le bot joue à un jeu.\n"
            "- `listening` : Le bot écoute quelque chose (ex. de la musique).\n"
            "- `watching` : Le bot regarde quelque chose (ex. un film).\n"
            "- `streaming` : Le bot diffuse en direct (ex. sur Twitch).\n\n"
            "Exemples d'utilisation :\n"
            "`+activity playing Un jeu génial`\n"
            "`+activity listening De la musique`\n"
            "`+activity watching Un film cool`\n"
            "`+activity streaming Ma diffusion en direct`\n\n"
            "Si vous utilisez `streaming`, vous devez spécifier une URL de diffusion, comme `https://www.twitch.tv/yourstream`."
        ),
        color=dynamic_color
    )
    await ctx.send(embed=embed)





bot.run("TON TOKEN")

