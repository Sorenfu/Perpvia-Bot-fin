import discord
from modules.shop.service import ShopService

def register(tree):
    service=ShopService()
    @tree.command(name='shop',description='Open point shop')
    async def shop(interaction):
        products=await service.list_products()
        if not products:
            await interaction.response.send_message('🛒 Shop is empty')
            return
        embed=discord.Embed(title='🛒 Point Shop')
        for p in products:
            embed.add_field(name=p['name'],value=f"{p['price']} Points")
        await interaction.response.send_message(embed=embed)
