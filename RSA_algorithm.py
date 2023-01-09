import random

def fast_mod(x,y,n): #following formula x**y mod n
    p = 1 #holds partial result
    s = x #holds current x^2^j
    r = y #used to compute binary expnasion of y

    while (r > 0):
        if (r % 2 != 0): #multiply p and s and mod by n if r is odd
            p = (p * s) % n
        s = (s * s) % n
        r = r // 2
        
    return p


def euclid_algo(x,y):
    #x must be less than y for algorithm to work properly
    if (y<x):
        temp_1 = x
        temp_2 = y
        y = temp_1
        x = temp_2

    remainder = y % x 

    #algorithm to find GCD
    while (remainder != 0):
        y = x
        x = remainder
        remainder = y % x
    return x
    
def is_coprime(a, b):
    gcd = euclid_algo(a,b)

    if (gcd == 1):
        return True
    else:
        return False

def calculate_d(phi, e):
    k = 0
    calc_mod = 1
    while True:
        calc_mod = ((k * phi) + 1) % e
        
        k+=1 #will need to subtract 1 later because it increments 1 value higher than needed to calcualte d

        if (k!=e and calc_mod == 0):
            break  

        calc_mod = ((k * phi) + 1) % e

    d = (((k-1) * phi + 1)) // e
    return d

def encryption(ascII_list, encryption_key, n):
    encrypted_list = []
    
    length = len(ascII_list)
    for i in range(length):
        temp_int = int(ascII_list[i])
        encrypted_num = fast_mod(temp_int, encryption_key,n)
        encrypted_list.append(encrypted_num)
        
        print('Current encrypted number:',encrypted_num)

    return encrypted_list

def decryption(encrypted_list, decryption_key, n):
    decrypted_list = []
    
    length = len(encrypted_list)
    for i in range(length):
        temp_int2 = int(encrypted_list[i])
        decrypted_num = fast_mod(temp_int2, decryption_key,n)
        decrypted_list.append(decrypted_num)

        print('decrypted value:', decrypted_num)
   
    return decrypted_list

#choosing encryption variable e
def choose_e (phi_value): 
    e = 1
    e_values_list = []
    while (e < phi):
        if (is_coprime(e,n) and is_coprime(e,phi) and e!=1):
            
            include_value = random.getrandbits(1) #randomly picks if value is included in possible e values list.
            if (include_value == 1):
                e_values_list.append(e)
                print("added")

            else:
                print("skipped")
                pass

        if (len(e_values_list) == 10000): #useful for testing larger primes
            print("\nHit 10K different options for encrytption variable.\n")
            break
        e+=1
    return e_values_list


#----------------------------------------------------------------------------------#  
# Main Program    
p = 1299827 #p and q must both be prime, suggested to be two digits or larger
q = 1299817
n = p*q
phi = (p-1)*(q-1)
print("Finding public encryption key...")
#e will be encryption / public key
e_list = choose_e (phi)

print("A resonable amount of encryption variables e: ",e_list, "\n")

#randomly selecting public key from possible options
public_key = random.choice(e_list)
print("Encrpytion / public key:",'(',public_key,',',n,')')

#calculating private key for decryption using function d = (k* phi(N) +1) / e, where k is some integer
private_key = calculate_d(phi, public_key)
print('Decryption / private Key:','(',private_key,',',n,')')

#gathering plain text
plain_text = str(input('\nPlease enter a string\n'))

#converting and storing string in ASCII values
ascII_list = [str(ord(element)) for element in plain_text] #list comprehension
print("plain text converted to ascII:",ascII_list)

#using formula for encryption: ciphertext = (plain_text^public_key) mod N, where N = p * q
encrypted_num = encryption(ascII_list, public_key, n)
print( "encrypted number:",encrypted_num)

#using formula for decryption: plaintext = (ciphertext ^ private_key) mod N, using modular exponentiation.
decrypted_num = decryption(encrypted_num, private_key, n)
print("decrypted number:",decrypted_num)