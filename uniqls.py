#uniqls

def uniqls(vals):
    ls = []
    tmp = []
    cascade1(tmp, vals, ls)
    return ls

def used(val, vals):
    tmp = vals[:len(vals)]
    tmp.remove(val)
    return tmp

def cascade1(tmp, vals, ls):
    if len(vals)==0:
        ls.append(tmp[:len(tmp)])
    for a in vals:
        tmp.append(a)
        cascade1(tmp,used(a, vals), ls)
        tmp.pop()
        
def cascade2(tmp, vals, ls, i):
    if i==len(vals):
        ls.append(tmp[:len(tmp)])
    else:
        for a in vals[len(vals)-i-1]:
            tmp.append(a)
            cascade2(tmp,vals, ls, i+1)
            tmp.pop()

def uniqbs(vals): #rows with r[0] being bottom instead of top
    ls = []
    tmp = []
    cascade2(tmp, vals, ls, 0)
    return ls
