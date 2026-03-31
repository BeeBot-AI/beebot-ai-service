import redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=2)
    print("Ping:", r.ping())
except Exception as e:
    print("Error:", e)
