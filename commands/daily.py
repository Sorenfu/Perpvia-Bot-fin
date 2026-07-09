def register(tree):
    @tree.command(name='daily',description='Daily checkin')
    async def daily(interaction):
        await interaction.response.send_message('Daily command loaded')
