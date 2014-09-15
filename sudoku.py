"""
Implementation of Sudoku problem.

This is not the fastest Sudoku solver, but it shows how general the framework is
"""
from zwicky import MorphologicalAnalysis

class Sudoku(MorphologicalAnalysis):
	# the variables are each cell, which can take the value 1-9
	indices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	values = indices
	board = [('%d-%d' % (i, j), values) for i in indices for j in indices]

	# the rules are:
	# each row    must only contain each value once
	# each column must only contain each value once
	# each block  must only contain each value once
	@staticmethod
	def is_same_block((i, j), (k, l)):
		same_row = (i - 1) / 3 == (k - 1) / 3
		same_col = (j - 1) / 3 == (l - 1) / 3
		return same_row and same_col
	
	def __init__(self, exclusions = []):
		# each row
		indices, values = Sudoku.indices, Sudoku.values
		for i in indices:
			for j in indices:
				for k in indices:
					if j < k:
						exclusions += [('%d-%d' % (i, j), v, '%d-%d' % (i, k), v, 'row constraint') for v in values]
						# do columns the same, just transposed
						exclusions += [('%d-%d' % (j, i), v, '%d-%d' % (k, i), v, 'column constraint') for v in values]
				# now for the blocks
					for l in indices:
						if Sudoku.is_same_block((k, l), (i, j)) and (k > i or l > j):
							exclusions += [('%d-%d' % (i, j), v, '%d-%d' % (k, l), v, 
								'block constraint block %d-%d' % ((i - 1)/3, (j - 1)/3)) for v in values]
		MorphologicalAnalysis.__init__(self, Sudoku.board, exclusions)
	
	@staticmethod
	def generate_from_text(text):
		l = 0
		indices, values = Sudoku.indices, Sudoku.values
		text = text.replace('0', '.')
		assert len(text) == 81, len(text)
		exclusions = []
		for i in indices:
			for j in indices:
				if text[l] != '.':
					# exclude all other values
					exclusions += [('%d-%d' % (i, j), v, 'start value %s' % text[l]) for v in values if text[l] != ('%d' % v)]
				l += 1
		return Sudoku(exclusions)
	@staticmethod
	def print_solution(sol):
		indices, values = Sudoku.indices, Sudoku.values
		for i in indices:
			line = ' '
			for j in indices:
				line += '%1d' % sol['%d-%d' % (i, j)]
				if j == 3 or j == 6: 
					line += ' | '
				else:
					line += ' '
			print line
			if i == 3 or i == 6:
				line = ' '
				for j in indices:
					line += '-'
					if j == 3 or j == 6: 
						line += '-+-'
					else:
						line += '-'
				print line
		print
	@staticmethod
	def solution_to_text(self, sol):
		l = 0
		text = ''
		for i in Sudoku.indices:
			for j in Sudoku.indices:
				text += sol['%d-%d' % (i, j)]
		return text

if __name__ == '__main__':
	# now, give some preconditions
	# some examples
	grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
	grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
	hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
	# take from first argument
	import sys
	problem = Sudoku.generate_from_text(sys.argv[1])

	# run analysis and print solutions
	# set verbose=True if you want to follow the reasoning process
	for sol in problem.search(verbose=False):
		print 'SOLUTION:'
		print
		Sudoku.print_solution(sol)
	"""
	Example output:
	-------
	SOLUTION:

	 4 8 3 | 9 2 1 | 6 5 7 
	 9 6 7 | 3 4 5 | 8 2 1 
	 2 5 1 | 8 7 6 | 4 9 3 
	 ------+-------+-------
	 5 4 8 | 1 3 2 | 9 7 6 
	 7 2 9 | 5 6 4 | 1 3 8 
	 1 3 6 | 7 9 8 | 2 4 5 
	 ------+-------+-------
	 3 7 2 | 6 8 9 | 5 1 4 
	 8 1 4 | 2 5 3 | 7 6 9 
	 6 9 5 | 4 1 7 | 3 8 2 



	"""

