import random

from libs.comparisons_management import vote_for

def full_manual_sort(list_sort):
	"""
		Create a sort with all comparisons between the elements of a list
	"""
	length = len(list_sort)
	list_battles = [ (i, j) for i in range(length) for j in range(length) if i < j ]
	random.shuffle(list_battles)
	l_score = [0 for i in range(length)]
	
	for idx1, idx2 in list_battles:
		vote_for(l_score, list_sort, [idx1, idx2])
	
	return [x for _,x in sorted(zip(l_score, list_sort))]
