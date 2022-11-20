from create_bot import con

async def check_user(ID):
    with con.cursor() as cur:
        cur.execute(f"SELECT * FROM `users` WHERE `id`={ID}")
        rows = cur.fetchall()

        if not rows:
            return False
        else:
            return True