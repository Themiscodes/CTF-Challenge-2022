
# simple prime checker
def prime_check(x):
    if x > 1:
        # until x/2 is enough
        for i in range(2, int(x/2)+1):
            if (x % i) == 0:
                return False
        return True
    else:
        return False

N=127670779

myfactors=[]
for i in range(1,N+1):
    if N%i ==0 and prime_check(i):
        myfactors.append(i)

p = myfactors[0]
q = myfactors[1]
print("p: ",p)
print("q: ",q)
phi = (p-1) * (q-1)
print("phi: ",phi)
e = 7

# what we're looking for is 𝑑 ≡ 𝑒^−1(mod𝜙(𝑛))
d=0
for d in range(1, phi):
    if (((e%phi) * (d%phi)) % phi == 1):
        break

print("d: ", d)

# x =(E(x)^d) mod N
Ex = 32959265
x= pow(Ex, d, N)
print("x = ", x)

# y =(E(x)^d) mod N
Ey = 47487400
y= pow(Ey, d, N)
print("y = ", y)

# so the final link should be
link="http://aqwlvm4ms72zriryeunpo3uk7myqjvatba4ikl3wy6etdrrblbezlfqd.onion/"+str(y)+str(x)+str(y)+str(x)+".txt"

print(link)