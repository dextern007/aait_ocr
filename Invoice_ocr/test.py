T = int(input())

for i in range(T):
    M = input().split(" ")
    N = input().split(" ")
    res = []
    for j in range(int(M[0])):
        if j+1 == int(M[0]):
            res.append(int(N[j])+int(N[0])/int(M[1]))
        
        else:
            res.append(int(N[j])+int(N[j+1])/int(M[1]))
            
    print(max(res))