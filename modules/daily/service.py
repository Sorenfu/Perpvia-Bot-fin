from datetime import datetime,timedelta
from database.db import pool
from core.points import PointEngine

class DailyService:
    async def checkin(self,user_id):
        async with pool.acquire() as c:
            last=await c.fetchval('SELECT created_at FROM daily_checkins WHERE user_id=$1 ORDER BY created_at DESC LIMIT 1',user_id)
        if last and datetime.utcnow()-last < timedelta(hours=12):
            return False,'Daily cooldown active'
        await PointEngine().add(user_id,20,'daily','Daily Check-in')
        async with pool.acquire() as c:
            await c.execute('INSERT INTO daily_checkins(user_id,reward) VALUES($1,$2)',user_id,20)
        return True,'🎉 Daily +20 Points'
