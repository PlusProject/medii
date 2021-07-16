clinicalTrialsQuery = [1,2,3,4,5]

cid_dict = { trial: [] for trial in clinicalTrialsQuery }

for cid in cid_dict:
    participateSet = [1,2]
    for pid in participateSet:
        cid_dict[cid].append(pid)
        a = 3

print(a)


a = [1,2,3]
b = [1,2,5]
pid_list = sorted(set(a).intersection(b))
print(sorted(set(a).intersection(b)))
print(pid_list)