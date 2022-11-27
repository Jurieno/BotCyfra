from create_bot import con

async def check_user(ID):
    
    rows = await con(f"SELECT * FROM `users` WHERE `id`={ID}")
    if not rows:
        return False
    else:
        return True

       