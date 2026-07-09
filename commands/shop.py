def register(tree,service):
    @tree.command(name='shop',description='Open shop')
    async def shop(interaction):
        items=await service.products()
        await interaction.response.send_message(f'Shop products: {len(items)}')
