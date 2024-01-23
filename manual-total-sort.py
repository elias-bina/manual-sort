#! /usr/bin/python3
import sys
import random

file_src = open(sys.argv[1], 'r')
data = file_src.read().splitlines() 
file_src.close()


def vote_for(l_sort, idx1, idx2, l_score):
    res = input(f"\nChoose the best between {l_sort[idx1]} and {l_sort[idx2]}\nY - {l_sort[idx1]}\n? - {l_sort[idx2]}\n").lower()
    print()
    if(res == "y"):
        l_score[idx1]  += 1
        print(f"{l_sort[idx1]} Chosen")
    else:
        l_score[idx2]  += 1
        print(f"{l_sort[idx2]} Chosen")
        

def sort_like(list_sort):
    length = len(list_sort)
    list_battles = [ (i, j) for i in range(length) for j in range(length) if i < j ]
    random.shuffle(list_battles)
    l_score = [0 for i in range(length)]
    print(list_battles)
    
    for idx1, idx2 in list_battles:
        vote_for(list_sort, idx1, idx2, l_score)
    
    for i in range(length):
        print(f"{list_sort[i]} won {l_score[i]} fights")
     
    return [x for _,x in sorted(zip(l_score, list_sort))]
     
    
l = ["Pokemon", "Mario", "Sonic","Palworld", "Isaac"]

l_sorted = sort_like(data)
l_sorted.reverse()

print("\n\n================= FINAL RESULTS =================\n\n")
for elem in l_sorted:
	print(elem)