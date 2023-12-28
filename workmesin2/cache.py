import redis 

r = redis.Redis(host='redis', port=6379)

r.set("France", "Paris")

france_capital = r.get("France")
print(france_capital)