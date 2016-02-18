#!/usr/bin/python3

# Factorizing numbers.
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

class Polynomial:
	def __init__(self, a):
		if(type(a) == float):
			a = int(a)

		if(type(a) == str and "x" not in a):
			self.data = int(a,2)
		elif(type(a) == str):
			self.data = 0
			a = a + "+"

			if("1+" in a):
				self.data |= 1
				a = a.replace("1+", "")
			if("x+" in a):
				self.data |= 2
				a = a.replace("x+", "")
			
			i = 2
			while(len(a) > 0):
				searchstring = "x^" + str(i) + "+"
				if(searchstring in a):
					self.data |= 2 ** i
					a = a.replace(searchstring, "")
					
				i += 1
				if(i > 1000):
					raise ValueError("Failed to parse polynomial")
		elif(type(a) == int):
			self.data = a
		else:
			print(a, type(a))
			raise ValueError("Unkown polynomial")

		self.degree = self.data.bit_length() - 1
	
	def __str__(self):
		# Print the polynomial as a string.
		s = ""
		for i in range(0, self.degree + 2):
			if(self.data & 2 ** i):
				if(len(s) > 0):
					s = "+" + s
				if(i > 1):
					s = "x^" + str(i) + s
				elif(i == 1):
					s = "x" + s
				else:
					s = "1" + s			
		if(len(s) == 0):
			s = '0'
		return s
	
	def deg(self):
		# Calculate the polynomial degree.
		i = 0
		while(2**i <= self.data):
			i += 1
		return i - 1
	
	def modulo(self, other):
		# When dividing a small A on a large B, A is the rest without any
		# processing...
		if (self.data < other.data):
			return self

		# While the rest-degree i larger than the other polynomial, divide
		# again.
		work = self
		while(work.degree >= other.degree):
			diff = work.degree - other.degree

			#rest = work.data
			## Hacks which works for polynomials in GF(2).
			#for i in range(0, self.degree + 1):
			#	if(other.data & 2**i):
			#		rest = rest ^ (2 ** (i+diff))
			#	i += 1
			
			# Optimiztion: Create a polynomial which is diff degree higher than
			# what you divide with, and do a bitwise XOR. Works in GF(2)... :)
			l = other.data << diff
			rest = l ^ work.data

			work = Polynomial(rest)
		return work
	
	def euclidean(self, other):
		# Make sure which polynomial is of highest degree before start.
		if(self.data > other.data):
			big, small = self, other
		else:
			small, big = other, self

		# While we cannot get a clean division, store the results and divide
		# again.
		results = [big, small]
		while(results[-1].data > 0):
			results.append(results[-2].modulo(results[-1]))
		
		# Return the second to last result, as the last result always are 0.
		return results[-2]

	def irreducible(self):
		# Calculate the required k-values
		kvalues = [i+1 for i in range(0, int(self.degree/2))]
		
		# Run euclidean for all k-values. If something else than 1 is returned,
		# the polynomial is not irreducible. If all the tests goes ok, the
		# polynomial is irreducible.
		for k in kvalues:
			a = self.euclidean(Polynomial((2 ** (2 ** k)) | 2))
			if a.data != 1:
				return False
		return True

	def primitive(self):
		# Test for odd number of factors
		a = bin(self.data)
		if(not a.count('1') % 2):
			return False

		# Test if it is irreducible
		if(not self.irreducible()):
			return False
		
		# If mersenne prime, skip last check
		if(self.degree in [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 
		607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 
		9941, 11213, 19937]):
			return True

		# Test x^(2^n-1/p) prime-factor stuff.
		n = (2 ** self.degree) - 1
		factors = prime_factors(n)

		if(len(factors) == 1):
			return True
		else:
			factors = set(factors)
		
		for factor in factors:
			p = Polynomial(2 ** int(n / factor))
			if(p.modulo(self).data == 1):
				return False
		return True 
