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

def random_choice(): #added this so that there are more random choices for e
    options = [0,1,2,3,4]
    return random.choice(options)

def choose_e(n, phi):
    #choosing encryption variable e
    print('Finding random public key...')
    e = 1
    e_list = []
    while (e < phi):
        if (is_coprime(e,n) and is_coprime(e,phi) and e!=1 and random_choice() == 1):
            #print('adding')
            e_list.append(e)
        else:
            #print('skipping')
            pass

        if (len(e_list) == 10000): #limits amount of possible e's, just for testing purposes
            print('Hit limit -- stopping...')
            break
        e+=1

    #print("All possible encryption variables e: ",e_list)
    
    return e_list
    
    
def encryption(ascII_list, encryption_key, n):
    encrypted_list = []
    
    length = len(ascII_list)
    for i in range(length):
        temp_int = int(ascII_list[i])
        encrypted_num = fast_mod(temp_int, encryption_key,n)
        encrypted_list.append(encrypted_num)
        
        #print('Current encrypted number:',encrypted_num)

    return encrypted_list

def decryption(encrypted_list, decryption_key, n):
    decrypted_list = []
    
    length = len(encrypted_list)
    for i in range(length):
        temp_int2 = int(encrypted_list[i])
        decrypted_num = fast_mod(temp_int2, decryption_key,n)
        decrypted_list.append(decrypted_num)

        #print('Current decrypted number:',decrypted_num)
    return decrypted_list


#----------------------------------------------------------------------------------#  
# Main Program    
p = 1298149 #must be prime
q = 1299827 #must be prime
n = p*q
phi = (p-1)*(q-1)

public_key = random.choice(choose_e(n,phi))
print("\nEncrpytion / public key:",'(',public_key,',',n,')')

#selecting private key for decryption using function d = (k* phi(N) +1) / e, where k is some integer
private_key = calculate_d(phi, public_key)
print('Decryption / private Key:','(',private_key,',',n,')')


#gathering plain text
plain_text = str(input('\nPlease enter a string\n'))

#converting and storing string in ASCII values
ascII_list = [str(ord(element)) for element in plain_text] #list comprehension
print("\nPlain text converted to ascII:",ascII_list)


#using formula for encryption: c = plain_text^public_key mod N, where N = p * q
encrypted_num_list = encryption(ascII_list, public_key, n)
print( "\nEncrypted numbers:",encrypted_num_list)

#using formula for decryption: m = cipher_text^private_key mod N, where N = p * q
decrypted_num_list = decryption(encrypted_num_list, private_key, n)
print("\nDecrypted numbers:",decrypted_num_list)
