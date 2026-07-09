from modules.daily.service import DailyService

def register(tree):
    service=DailyService()
    @tree.command(name='daily',description='Daily check in')
    async def daily(interaction):
        ok,msg=await service.checkin(interaction.user.id)
        await interaction.response.send_message(msg)
