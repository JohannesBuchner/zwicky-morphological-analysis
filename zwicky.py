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
	
	def prone_option(self, parent, variablename, o, depth=0, verbose=False):
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
		if prohibited:
			return None
		else:
			return child
	
	def choose_option(self, parent, depth, verbose):
		# choose a free variable with the fewest of possible options
		branches = []
		for i, (variablename, options) in enumerate(self.board):
			if variablename in parent: continue
			remainder = [self.prone_option(parent, variablename, o, depth=depth, verbose=False) for o in options]
			ngood = sum([r is not None for r in remainder])
			if ngood == 0 or ngood == 1:
				# take immediately: if no other choice left, we must assume this value
				return i, remainder
			
			ntotal = len(options)
			#print '  Option %s: %d of %d remaining' % (variablename, ngood, ntotal)
			branches.append((i, remainder, ngood, ntotal))
		
		# sort by reduction
		branches.sort(key=lambda (i, remainder, ngood, notal): -1 if ngood < 1 else 0 if ngood == 1 else ngood * 1. / ntotal)
		# choose variable with highest reduction
		choice, remainder, ngood, ntotal = branches[0]
		#print '%s-->' % (' '*depth), self.board[choice][0], ' (%d options of %d)' % (ngood, ntotal)
		return choice, remainder
	
	"""
	Performs the search and returns all possible solutions.
	
	:param verbose:
	   If True, the reasoning process is documented (e.g. which criterion lead to rejection of a branch)
	"""
	def search(self, parent=dict(), depth=0, verbose=True):
		if len(self.board) <= depth:
			yield parent
			return
		choice, remainder = self.choose_option(parent, depth=depth, verbose=verbose)
		variablename, options = self.board[choice]
		# go through exclusions mentioning this parameter
		for o, r in zip(options, remainder):
			# we do this again for the sake of verbose output
			if verbose:
				child = self.prone_option(parent, variablename, o, depth=depth, verbose=verbose)
			else:
				child = r
			if child is None: continue
			#print '  found allowed: ', o
			if verbose: print '%sLets assume %s=%s.' % (' '*depth, variablename, o)
			for solution in self.search(child, depth + 1, verbose=verbose):
				yield solution
			if verbose: print


