import database.db as db
class PointEngine:
 async def balance(self,user):
  async with db.pool.acquire() as c:
   row=await c.fetchrow('SELECT points FROM users WHERE discord_id=$1',user)
  return row['points'] if row else 0
 async def add(self,user,amount,source,reason):
  async with db.pool.acquire() as c:
   await c.execute('INSERT INTO users(discord_id,points) VALUES($1,$2) ON CONFLICT(discord_id) DO UPDATE SET points=users.points+$2',user,amount)
