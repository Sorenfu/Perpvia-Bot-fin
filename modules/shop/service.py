class ShopService:
    def __init__(self,db,points):
        self.db=db
        self.points=points

    async def products(self):
        return await self.db.fetch('SELECT * FROM products WHERE status=true')

    async def redeem(self,user_id,product_id):
        product=await self.db.fetchrow('SELECT * FROM products WHERE id=$1 AND status=true',product_id)
        if not product:
            return False,'Product unavailable'
        ok=await self.points.spend(user_id,product['price'],'shop',product['name'])
        if not ok:
            return False,'Insufficient points'
        await self.db.execute('INSERT INTO orders(user_id,product_id,status) VALUES($1,$2,$3)',user_id,product_id,'created')
        return True,'Redeemed'
