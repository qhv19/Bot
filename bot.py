import discord
from discord.ext import commands
from discord.ui import View, Button

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class Ticket1View(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="الدعم الفني", style=discord.ButtonStyle.secondary, emoji="⚙️", custom_id="ticket_support")
    async def support_callback(self, interaction: discord.Interaction, button: Button):
        await create_ticket(interaction, "الدعم الفني")

    @discord.ui.button(label="طلب رتبه", style=discord.ButtonStyle.secondary, emoji="🏷️", custom_id="ticket_role")
    async def role_callback(self, interaction: discord.Interaction, button: Button):
        await create_ticket(interaction, "طلب رتبه")

    @discord.ui.button(label="طلب تعويض", style=discord.ButtonStyle.secondary, emoji="🏷️", custom_id="ticket_comp")
    async def comp_callback(self, interaction: discord.Interaction, button: Button):
        await create_ticket(interaction, "طلب تعويض")

    @discord.ui.button(label="طلب سيناريو", style=discord.ButtonStyle.secondary, emoji="📋", custom_id="ticket_scenario")
    async def scenario_callback(self, interaction: discord.Interaction, button: Button):
        await create_ticket(interaction, "طلب سيناريو")

    @discord.ui.button(label="شكوى على اداري / رقابي", style=discord.ButtonStyle.danger, emoji="⚠️", custom_id="ticket_admin_complaint")
    async def admin_comp_callback(self, interaction: discord.Interaction, button: Button):
        await create_ticket(interaction, "شكوى على اداري")


class Ticket2View(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="طلب فك باند", style=discord.ButtonStyle.danger, emoji="🔨", custom_id="ticket_unban")
    async def unban_callback(self, interaction: discord.Interaction, button: Button):
        await create_ticket(interaction, "طلب فك باند")

    @discord.ui.button(label="شكوى على لاعب", style=discord.ButtonStyle.danger, emoji="🔨", custom_id="ticket_player_complaint")
    async def player_comp_callback(self, interaction: discord.Interaction, button: Button):
        await create_ticket(interaction, "شكوى على لاعب")

    @discord.ui.button(label="اعتراض على باند", style=discord.ButtonStyle.danger, emoji="🔨", custom_id="ticket_ban_appeal")
    async def ban_appeal_callback(self, interaction: discord.Interaction, button: Button):
        await create_ticket(interaction, "اعتراض على باند")


async def create_ticket(interaction: discord.Interaction, ticket_type: str):
    guild = interaction.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }
    
    # تقدر تعدل اسم الكاتيجوري أو تحذفه لو ما تبيه
    category = discord.utils.get(guild.categories, name="TICKETS")
    
    channel = await guild.create_text_channel(
        name=f"tkt-{interaction.user.name}-{ticket_type}",
        overwrites=overwrites,
        category=category
    )
    
    embed = discord.Embed(
        title=f"تذكرة: {ticket_type}",
        description=f"مرحباً {interaction.user.mention}\nتم فتح التذكرة بنجاح. اكتب مشكلتك أو طلبك هنا، وانتظار رد الإدارة.",
        color=discord.Color.blue()
    )
    
    view = CloseTicketView()
    await channel.send(embed=embed, view=view)
    await interaction.response.send_message(f"تم فتح تذكرتك بنجاح: {channel.mention}", ephemeral=True)


class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="إغلاق التذكرة", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket")
    async def close_callback(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("جاري إغلاق التذكرة...")
        await interaction.channel.delete()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
@commands.has_permissions(administrator=True)
async def settickets(ctx):
    # رسالة اللوحة الأولى
    embed1 = discord.Embed(
        title="التذكرة",
        description="يرجى مناقشة قوانين التذكره قبل فتحها\n\n**القائمة الأولى:**",
        color=discord.Color.dark_theme()
    )
    embed1.set_image(url="حط_رابط_الصورة_هنا") # حط رابط صورتك الأولى هنا
    await ctx.send(embed=embed1, view=Ticket1View())

    # رسالة اللوحة الثانية
    embed2 = discord.Embed(
        title="التذكرة",
        description="يرجى مناقشة قوانين التذكره قبل فتحها\n\n**القائمة الثانية:**",
        color=discord.Color.dark_theme()
    )
    embed2.set_image(url="حط_رابط_الصورة_الثانية_هنا") # حط رابط صورتك الثانية هنا
    await ctx.send(embed=embed2, view=Ticket2View())


bot.run("MTU2NzAwNjM2NjIzMTU2NDM3OQ.G0Tk-J.leFC8l3PMaWOLYM0D8aVzWVk1JpmcNEizmEJwU")
