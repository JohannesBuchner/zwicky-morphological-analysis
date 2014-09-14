"""
Python Implementation of Zwickys General Morphological analysis
"""
class MorphologicalAnalysis(object):
	"""
	:param board: 
	   List of all variables to consider, with a list of their respective possible values.
	   Example: board=[('Color', ['Red', 'Yellow', 'Green'], ('Speed', ['Fast', 'Standing'])]
	
	:param exclusions:
	   List of impossible combinations. Each item is
	     ('Variable1', 'Value1', 'Variable2', 'Value2', ..., 'Some Comment')
	     The last entry is a free-text comment.
	   These can be concerning a single variable whose value is forbidden
	     Example: ('Color', 'Red', 'Ugly colour')
	   or a combination of two
	     Example: ('Color', 'Red', 'Speed', 'Fast', 'Unsafe, Regulation A38')
	   or more.
	
	To indicate start values for the search, add them as exclusions.
	"""
	def __init__(self, board, exclusions):
		relevant_exclusions = {}
		for e in exclusions:
			assert len(e) % 2 == 1, ('Incorrect format for exclusion', e)
			assert len(e) > 0, ('Exclusion is empty')
			for k, v in zip(e[:-1:2], e[1:-1:2]):
				l = relevant_exclusions.get(k, [])
				l.append(e)
				relevant_exclusions[k] = l

		for k in relevant_exclusions.keys():
			assert any([k == k1 for k1, _ in board]), k
			relevant_exclusions[k].sort(key=lambda e: len(e))
		self.relevant_exclusions = relevant_exclusions
		self.board = board
	
	"""
	Performs the search and returns all possible solutions.
	
	:param verbose:
	   If True, the reasoning process is documented (e.g. which criterion lead to rejection of a branch)
	"""
	def search(self, parent=dict(), depth=0, verbose=True):
		if len(self.board) <= depth:
			yield parent
			return
		variablename, options = self.board[depth]
		# go through exclusions mentioning this parameter
		for o in options:
			prohibited = False
			child = dict(**parent)
			child[variablename] = o
			for e in self.relevant_exclusions[variablename]:
				exclusion_applies = 0
				for k, v in zip(e[:-1:2], e[1:-1:2]):
					if k in child and child[k] == v:
						#print 'criterion ', e, 'applies through', k, v
						exclusion_applies += 1
			
				if exclusion_applies == (len(e) - 1) / 2:
					if len(e) > 2 + 1:
						if verbose: print '%s%s=%s REJECTED by ' % ('  '*depth, variablename, o), e
					prohibited = True
					break
			if not prohibited:
				#print '  found allowed: ', o
				if verbose: print '%sLets assume %s=%s.' % (' '*depth, variablename, o)
				for solution in self.search(child, depth + 1, verbose=verbose):
					yield solution
				if verbose: print

