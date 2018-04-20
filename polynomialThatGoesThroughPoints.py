import math

#the way this algoritm works is for each point
#in a list of points, a polynomial is made with
#a root at the x-value of all the other points
#in the list, and is then multiplied by a scalar
#such that it passes through the point in question.
#All these polynomials are added together, and
#since for any given point in the list, the graph
#would pass through the x-axis except for one
#additive polynomial that passes through the 
#correct point, the sum would pass through
#all required points.

#run the function graph with a list of points 
#to get the equation of a polynomial that goes
#through all of them
def main(points): 
	assert(isFunction(points))
	curr = [0] * len(points)
	for point in points:
		roots = getRoots(points, point)
		newGraph = getGraphWithRootsAndPoint(roots, point)
		curr = add(curr, newGraph)
	return translate(curr)
	

#makes sure the list of points make a function
def isFunction(points):
	xValues = []
	for point in points:
		if point[0] in xValues:
			return False
		xValues.append(point[0])
	return True

#gets a list of roots needed for the resulting additive polynomial
def getRoots(points, point):
	roots = []
	for p in points:
		if p[0] != point[0]:
			roots.append(p[0])
	return roots

#makes a polynomial with a given list of roots
#and one point to cross through
def getGraphWithRootsAndPoint(roots, point):
	foilMultiplicands = []
	for root in roots:
		foilMultiplicands.append([1, -root],)
	product = multiply(foilMultiplicands)
	currVal = f(product, point[0])
	graph = foil([product, [1.0 * point[1] / currVal],])
	return graph

#multiplies a list of polynomials together
def multiply(multiplicands):
	if len(multiplicands) <= 1:
		return multiplicands[0]
	elif len(multiplicands) == 2:
		return foil(multiplicands)
	else:
		newMultiplicands = [foil([multiplicands[0], multiplicands[1]])]
		for x in xrange(2, len(multiplicands)):
			newMultiplicands.append(multiplicands[x],)
		return multiply(newMultiplicands)

#multiplies two polynomials together
def foil(multiplicands):
	product = [0] * (len(multiplicands[0]) + len(multiplicands[1]) - 1)
	for x in xrange(len(multiplicands[0])):
		for y in xrange(len(multiplicands[1])):
			product[x + y] += 1.0 * multiplicands[0][x] * multiplicands[1][y]
	return product

#finds the y-value for a specific x-value of a polynomial
def f(function, x):
	val = 0
	for term in xrange(len(function)):
		power = len(function) - term - 1
		val += 1.0 * (function[term] * (x ** power))
	return val

#adds two polynomials of the same degree
def add(poly1, poly2):
	result = [0] * len(poly1)
	for x in xrange(len(poly1)):
		result[x] = poly1[x] + poly2[x]
	return result

#translate the result from a list of 
#values into a polynomial
def translate(graph):
	function = "" 
	for term in xrange(len(graph)):
		power = len(graph) - term - 1
		if (graph[term] != 0):
			if (function == ""):
				function += str(graph[term])
			else:
				function += str(math.fabs(graph[term]))
			if (power > 0):
				function += "x"
				if (power > 1):
					function += "^" + str(power)
			nxtTerm = nextTerm(graph, term)
			if (nxtTerm == 0):
				return function
			else:
				if nxtTerm < 0:
					function += " - "
				else:
					function += " + "
	return function

#finds the next non-zero term in a polynomial
def nextTerm(f, term):
	while (True):
		term = term + 1
		if (term >= len(f)):
			return 0
		elif (f[term] != 0):
			return f[term]
	return 0
