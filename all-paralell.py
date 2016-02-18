#!/usr/bin/python3

import sys
import redis
import concurrent.futures
 
from polynomial import Polynomial

r = redis.Redis()

def check_server():
	try:
		r.info()
	except redis.exceptions.ConnectionError:
		print >>sys.stderr, "Error: cannot connect to redis server. Is the server running?"
		sys.exit(1)

def work(n):
	p = Polynomial(n)
	if(p.primitive()):
		print(n, p)
		r.rpush("primitive", n)
 
def main():
	with concurrent.futures.ProcessPoolExecutor(max_workers=32) as executor:
		for i in range(2 ** int(sys.argv[1]), 2 ** (int(sys.argv[2]) + 1)):
			executor.submit(work, i)

	print(r.lrange("primitive", 0, -1))
 
if __name__ == "__main__":
	print("Starting up")
	if(len(sys.argv) > 2):
		check_server()
		r.delete("primitive")
		main()
	print("Done")
