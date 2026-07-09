import os,asyncpg
pool=None
async def init_db():
 global pool
 pool=await asyncpg.create_pool(os.getenv('DATABASE_URL'))
 print('Database Connected')
