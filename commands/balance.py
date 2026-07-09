def register(tree):
    @tree.command(name='balance',description='View points')
    async def balance(interaction):
        await interaction.response.send_message('Balance command loaded')
