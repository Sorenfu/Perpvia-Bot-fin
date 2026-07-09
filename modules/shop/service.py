class ShopService:
    async def redeem(self,user_id,product_id):
        return {'status':'created','product':product_id}
