import database.db as db

class ShopService:
    async def list_products(self):
        async with db.pool.acquire() as c:
            return await c.fetch('SELECT * FROM products WHERE status=true')

    async def redeem(self,user_id,product_id):
        async with db.pool.acquire() as c:
            product=await c.fetchrow('SELECT * FROM products WHERE id=$1 AND status=true',product_id)
        if not product:
            return False,'Product not found'
        return True,'Redeem request created'
