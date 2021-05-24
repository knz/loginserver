import cloud

conmgr = cloud.open()
conn = conmgr.connect()

cur = conn.cursor()
cur.execute("SELECT version()")
print("response: ", cur.fetchone())

