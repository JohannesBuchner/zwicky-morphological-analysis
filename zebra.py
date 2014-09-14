"""
Implementation of the `Zebra puzzle <https://en.wikipedia.org/wiki/Zebra_Puzzle>`_
"""

# categories of the houses
# we will make each color, nationality, etc. a variable, with possible values 1-5
categories = [
	('Color', 'Yellow	Blue	Red	Ivory	Green'.split('\t')),
	('Nationality', 'Norwegian	Ukrainian	Englishman	Spaniard	Japanese'.split('\t')),
	('Drink', 'Water	Tea	Milk	Orange juice	Coffee'.split('\t')),
	('Smoke', 'Kools	Chesterfield	Old Gold	Lucky Strike	Parliament'.split('\t')),
	('Pet', 'Fox	Horse	Snails	Dog	Zebra'.split('\t')),
]

indices = [1, 2, 3, 4, 5]
# board of variables
board = []
for catname, options in categories:
	for i, value in enumerate(options):
		board.append((value, indices))

relation_same = lambda i1, i2: i1 == i2
relation_rightof = lambda i1, i2: i1 == i2 + 1
relation_nextto = lambda i1, i2: abs(i1 - i2) == 1

def add_combination(k1, v1, k2, v2, relation=relation_same):
	return [(v1, i1, v2, i2) for i1 in indices for i2 in indices if not relation(i1, i2)]

exclusions = []
# what is known about the problem
exclusions += add_combination('Nationality', 'Englishman', 'Color', 'Red')
exclusions += add_combination('Nationality', 'Spaniard', 'Pet', 'Dog')
exclusions += add_combination('Color', 'Green', 'Drink', 'Coffee')
exclusions += add_combination('Nationality', 'Ukrainian', 'Drink', 'Tea')
exclusions += add_combination('Color', 'Green', 'Color', 'Ivory', relation=relation_rightof)
exclusions += add_combination('Smoke', 'Old Gold', 'Pet', 'Snails')
exclusions += add_combination('Smoke', 'Kools', 'Color', 'Yellow')
exclusions += [('Milk', k) for k in [1, 2, 4, 5]]
exclusions += [('Norwegian', k) for k in [2, 3, 4, 5]]
exclusions += add_combination('Smoke', 'Chesterfield', 'Pet', 'Fox', relation=relation_nextto)
exclusions += add_combination('Smoke', 'Kools', 'Pet', 'Horse', relation=relation_nextto)
exclusions += add_combination('Smoke', 'Lucky Strike', 'Drink', 'Orange juice')
exclusions += add_combination('Nationality', 'Japanese', 'Smoke', 'Parliament')
exclusions += add_combination('Nationality', 'Norwegian', 'Color', 'Blue', relation=relation_nextto)

# mutually exclusive criterion nothing must appear twice
for catname, options in categories:
	for i, value in enumerate(options):
		for value2 in options[:i]:
			for k in indices:
				exclusions.append((value, k, value2, k))

# run analysis and print solutions
from zwicky import MorphologicalAnalysis
# set verbose=True if you want to follow the reasoning process
for sol in MorphologicalAnalysis(board, exclusions).search(verbose=False):
	print 'SOLUTION:'
	for catname, options in categories:
		print '%12s' % catname,
		for o in sorted(options, key=lambda o: sol[o]):
			print '|%12s' % o,
		print

"""
Output:
-------
SOLUTION:
       Color |      Yellow |        Blue |         Red |       Ivory |       Green
 Nationality |   Norwegian |   Ukrainian |  Englishman |    Spaniard |    Japanese
       Drink |       Water |         Tea |        Milk |Orange juice |      Coffee
       Smoke |       Kools |Chesterfield |    Old Gold |Lucky Strike |  Parliament
         Pet |         Fox |       Horse |      Snails |         Dog |       Zebra


"""

