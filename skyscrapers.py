#skyscrapers
import uniqls

def solve(rules):
    dim = len(rules[0])
    #rules are in form [[top],[right],[bottom],[left]]
    #rules[0],rules[1],rules[2],rules[3] : top, right, bottom, left
    uls = uniqls.uniqls(range(1,dim+1))
    
    knlist = [] #(n,x,y)
    klist = []
    
    poscs = []  #possible columns
    posrcs = [] #possible reverse columns (upside down)
    posrs = []  #possible rows
    posrrs = [] #possible reverse rows (right to left)
    fill(poscs, dim)
    fill(posrcs, dim)
    fill(posrs, dim)
    fill(posrrs, dim)
    
    for i,r in enumerate(rules[0]):
        for l in uls:
            if check(r, l):
                poscs[i].append(l)
                    
    for i,r in enumerate(rules[1]):
        for l in uls:
            if check(r, l):
                posrrs[i].append(l)

    for i,r in enumerate(rules[2]):
        for l in uls:
            if check(r, l):
                posrcs[i].append(l)
                
    for i,r in enumerate(rules[3]):
        for l in uls:
            if check(r, l):
                posrs[i].append(l)

        
    for i, c in enumerate(poscs):
        poscs[i] = sift(c, posrcs[dim-i-1])

    for i, r in enumerate(posrs):
        posrs[i] = sift(r, posrrs[dim-i-1])

    prev = size(posrs)
    while size(posrs) > 1:
        print size(posrs)
        print size(poscs)
        update(rules,klist,knlist,posrs,poscs)
        if size(posrs) == prev or size(posrs)==0:
            update(rules,klist,knlist,posrs,poscs)
            update(rules,klist,knlist,posrs,poscs)
            update(rules,klist,knlist,posrs,poscs)
            update(rules,klist,knlist,posrs,poscs)
            update(rules,klist,knlist,posrs,poscs)
            if size(posrs)!=prev and size(posrs)!=0:
                print "updated"
            elif size(posrs)<10000000 and size(posrs)!=0:
                return hardsolve(rules,posrs)
            else:
                print "I can't solve this"
                return False
        prev = size(posrs)
    board = []
    i = 0
    
    while i<dim:
        for l in posrs[dim-i-1]:
            board.append(l)
            print l
        i = i+1
    print solved(rules, board)

def check(r, line): #returns if the rule r is satisfied
    unique = len(line)==len(set(line))
    if r == 0:
        return unique
    if r == 1:
        return line[0]==len(line) and unique
    count = 0
    height = 0
    maxh = len(line)
    i = 0
    while i<len(line):
        if count>r: #too many
            return False
        curh = line[i]
        if height == maxh: #can't count anymore
            return count==r
        if curh==height: #repeat number
            return False
        if curh>height: #counts and sets new height
            count=count+1
            height = line[i]
        i= i+1
    return count==r and unique

#ruls taken as an array of arrays of size 4,
#each array is the set of rules for the side of the board starting with the top going clockwise
def reverse(line):
    tmp = []
    i = 0
    while i<len(line):
        tmp.append(line[len(line)-i-1])
        i = i+1
    return tmp
        
def solved(ruls, board): #board taken as array of rows, array[0] is top row
    dim = len(board[0])-1
    for i, r in enumerate(ruls[0]):
        if not check(r, zip(*board)[i]): #zip(*board) is array of columns, array[0] is first column
            return False
    for i, r in enumerate(ruls[1]):
        tmp = board[i][:dim+1]
        tmp.reverse()
        if not check(r, tmp):
            return False
    for i, r in enumerate(ruls[2]):
        tmp = zip(*board)[dim-i][:dim+1]
        tmp = reverse(tmp)
        if not check(r, tmp):
            return False
    for i, r in enumerate(ruls[3]):
        if not check(r, board[dim-i]):
            return False
    return True
def fill(pos, size):
    i = 0
    while i<size:
        pos.append([])
        i =i+1
def contains(ls,item):
    for x in ls:
        if x==item:
            return True
    return False

def sift(lines, rlines):
    sifted = []
    for l in lines:
        tmp = l[:len(l)]
        tmp.reverse()
        if contains(rlines, tmp):
            sifted.append(l)
    return sifted

def frequency(i, pos, place, ls):
    c = 0
    for l in ls:
        if l[pos]==i:
            c = c+1
    return c/(len(ls)*1.00)
    #print "frequency of {i} in position {pos} of {place} is {f}".format(i=i, pos=pos, place=place, f=c/(len(ls)*1.00))
    #if c/(len(ls)*1.00)==0.0:
     #   print "frequency of {i} in position {pos} of {place} is {f}".format(i=i, pos=pos, place=place, f=c/(len(ls)*1.00))

def size(poss):
    a=1
    for l in poss:
        #print(len(l))
        a=a*len(l)
    #print "possible column combinations: {a}".format(a=a)
    return a


def knfilt(i,x,y,pos): #rows, for columns do len-y-1 and swap with x
    for l in pos[y]:
        if l[x]==i:
            pos[y].remove(l)
def kfilt(i,x,y,pos): #rows
    for l in pos[y]:
        if l[x]!=i:
            pos[y].remove(l)
def change(klist, knlist, posrs, poscs):
    for s in (knlist):
        knfilt(s[0],s[1],s[2], posrs)
    for s in (klist):
        kfilt(s[0],s[1],s[2], posrs)
    for s in (knlist):
        knfilt(s[0],len(poscs)-s[2]-1,s[1], poscs)
    for s in (klist):
        kfilt(s[0],len(poscs)-s[2]-1,s[1], poscs)
    
def update(rules, klist, knlist, posrs, poscs):
    a = range(len(rules[0]))
    b = range(1,len(rules[0])+1)
    for i, c in enumerate(poscs):
        for n in b:
                for n2 in a:
                        if frequency(n, n2, i, c)==0 and not contains(knlist, (n,i,len(rules[0])-n2-1)):
                            knlist.append((n,i,len(rules[0])-n2-1))
                        elif frequency(n,n2,i,c)==1.0 and not contains(klist, (n,i,len(rules[0])-n2-1)):
                            klist.append((n,i,len(rules[0])-n2-1))

    for i, c in enumerate(posrs):
        for n in b:
                for n2 in a:
                        if frequency(n, n2, i, c)==0 and not contains(knlist, (n,n2,i)):
                            knlist.append((n,n2,i))
                        elif frequency(n,n2,i,c)==1.0 and not contains(klist, (n,n2,i)):
                            klist.append((n,n2,i))

    change(klist, knlist, posrs, poscs)

def hardsolve(rules, posrs):
    boards = uniqls.uniqbs(posrs)
    print "starting hard solve"
    for board in boards:
        if solved(rules, board):
            for l in board:
                print l
            print "solved!"
            return True
    print "I can't solve this"
    return False
    

