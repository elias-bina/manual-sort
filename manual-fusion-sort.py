#! /usr/bin/python3
import sys

def tri_fusion(liste):
	n = len(liste)
	if n == 1:
		return liste
	else:
		return fusion([tri_fusion(liste[:n//2]),tri_fusion(liste[n//2:])])

def fusion(lists):
	liste_res = []
	idxs = [0, 0]
	while(len(lists[0]) > idxs[0] and len(lists[1]) > idxs[1]):
		res = get_comp(lists, idxs)
		if(res == "y"):
			liste_res.append(lists[0][idxs[0]])
			idxs[0] +=1
		else:
			liste_res.append(lists[1][idxs[1]])
			idxs[1] +=1

	for j in range(2):
		for i in range(idxs[j], len(lists[j])):
			liste_res.append(lists[j][i])

	print(f"Intermediate res:{liste_res}\n")

	return liste_res

def get_comp(lists, idxs):
	res = input(f"Le meilleur entre {lists[0][idxs[0]]} et {lists[1][idxs[1]]}:\nY - {lists[0][idxs[0]]}\n? - {lists[1][idxs[1]]}\n").lower()
	if(res == "y"):
		print(f"\nChoose {lists[0][idxs[0]]}\n")
	else:
		print(f"\nChoose {lists[1][idxs[1]]}\n")
	return res

print("/!\\ This sort doesn't have the new CLI because it is too flawed and I don't want to switch from 'get_comp' to 'vote_for' for a 10 lines algorithm /!\\\n")

file_src = open(sys.argv[1], 'r')
data = file_src.read().splitlines() 
file_src.close()

sorted_data = tri_fusion(data)

print("\n\n================= FINAL RESULTS =================\n\n")
for elem in sorted_data:
	print(elem)



















