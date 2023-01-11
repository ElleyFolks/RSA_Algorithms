import random
import subprocess

class RSA:
    def __init__(self):
        self.ascII_list = []
        self.encrypted_list = []
        self.decrypted_list = []

        self.name ='elley' #used to specify name for specific file path on each user's device

        self.ascII_to_char = []
        self.ascII_string = ""
        self.p = 1299827 #p and q must both be prime, suggested to be two digits or larger
        self.q = 1299817
        self.n = 0   
        self.phi = 0
        
        self.e_list = []  
        self.public_key = 0
        self.private_key = 0

        #friend keys for encrypting messages to be sent to them
        self.friend_public_key = 0
        self.friend_n = 0

    def copy2clip(self,txt):
        cmd='echo '+txt.strip()+'|clip'
        return subprocess.check_call(cmd, shell=True)
        
    def fast_mod(self,x,y,n): #following formula x**y mod n
        p = 1 #holds partial result
        s = x #holds current x^2^j
        r = y #used to compute binary expnasion of y

        while (r > 0):
            if (r % 2 != 0): #multiply p and s and mod by n if r is odd
                p = (p * s) % n
            s = (s * s) % n
            r = r // 2
            
        return p

    def euclid_algo(self,x,y):
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
        
    def is_coprime(self,a, b):
        gcd = self.euclid_algo(a,b)

        if (gcd == 1):
            return True
        else:
            return False

    #choosing encryption variable e when generating a new public / private key pair
    def choose_e (self): 
        e = 1
        e_values_list = []
        while (e < self.phi):
            if (self.is_coprime(e,self.n) and self.is_coprime(e,self.phi) and e!=1):
                
                include_value = random.getrandbits(1) #randomly picks if value is included in possible e values list.
                if (include_value == 1):
                    e_values_list.append(e)
                    #print("added")

                else:
                    #print("skipped")
                    pass

            if (len(e_values_list) == 10000): #limits range, useful for testing larger primes
                print("Choosing from 10K different options for encrytption variable / public key...")
                break
            e+=1
        return e_values_list

    #calculating private key for decryption using function d = (k* phi(N) +1) / e, where k is some integer
    def calculate_d(self):
        k = 0
        calc_mod = 1
        while True:
            calc_mod = ((k * self.phi) + 1) % self.public_key
            
            k+=1 #will need to subtract 1 later because it increments 1 value higher than needed to calcualte d

            if (k!=self.public_key and calc_mod == 0):
                break  

            calc_mod = ((k * self.phi) + 1) % self.public_key

        d = (((k-1) * self.phi + 1)) // self.public_key
        return d

    def generate_keys(self):
        self.n = self.p*self.q
        
        self.phi = (self.p-1)*(self.q-1)
        print("\nFinding public encryption key...")
        
        #e will be encryption / public key
        self.e_list = self.choose_e()

        #print("Encryption variables e: ",self.e_list, "\n")

        #randomly selecting public key from possible options
        self.public_key = random.choice(self.e_list)
        print("Encrpytion / public key:",'(',self.public_key,',',self.n,')')

        self.private_key = self.calculate_d()
        print('Decryption / private Key:','(',self.private_key,',',self.n,')')
        
    def encrypt(self):
        #using formula for encryption: ciphertext = (plain_text^public_key) mod N, where N = p * q
        
        length = len(self.ascII_list)
        for i in range(length):
            temp_int = int(self.ascII_list[i])
            encrypted_num = self.fast_mod(temp_int, self.public_key,self.n)
            self.encrypted_list.append(encrypted_num)
            
            #print('Current encrypted number:',encrypted_num)
            
    def encrypt(self, ascII_list, pub_key, n_value):
        #use for more specific cases where public key and n value are being read instead of generated and saved.
        
        length = len(ascII_list)
        for i in range(length):
            temp_int = int(ascII_list[i])
            encrypted_num = self.fast_mod(temp_int, pub_key, n_value)
            self.encrypted_list.append(encrypted_num)
            
            #print('Current encrypted friend number:',encrypted_num)
            
    def get_encrypted_list(self):
        return self.encrypted_list

    def decrypt(self):
        #using formula for decryption: plaintext = (ciphertext ^ private_key) mod N, using modular exponentiation.
        
        length = len(self.encrypted_list)
        for i in range(length):
            temp_int2 = int(self.encrypted_list[i])
            decrypted_num = self.fast_mod(temp_int2, self.private_key,self.n)
            self.decrypted_list.append(decrypted_num)

            #print('Current decrypted number:', decrypted_num)
    
    def get_decrypted_list(self):
        return self.decrypted_list

    def input_to_ASCII(self): 
        #gathering plain text
        plain_text = str(input('\nPlease enter a string\n'))

        #converting and storing string in ASCII values
        self.ascII_list = [str(ord(element)) for element in plain_text] #list comprehension
        print("Plain text converted to ascII:",self.ascII_list)

    def get_char_output(self):#converts ASCII back to characters for user's convienence
    
        temp_len = len(self.decrypted_list)
        
        for i in range(temp_len): #converting every element in decrypted_list to char
            self.ascII_to_char.append(chr(self.decrypted_list[i])) #short way to convert ascII values back to characters
        
        self.ascII_string = "".join(self.ascII_to_char) #combining all elements in decrypted_list back to normal string
        print("ASCII to string:", self.ascII_string)

    def save_keys(self):
        print('\nSaving keys to desktop...')
        privatepath = r"C:/Users/"+self.name+"/Desktop/myprivate.txt"
        private = open(privatepath,"w+") #"w+" is for overwriting previous contents
        private.write(str(self.private_key))
        private.close()

        npath = r"C:/Users/"+self.name+"/Desktop/myN.txt"
        n = open(npath,"w+")
        n.write(str(self.n))
        n.close()

        publicpath = r"C:/Users/"+self.name+"/Desktop/mypublic.txt"
        public = open(publicpath,"w+")
        public.write(str(self.public_key))
        public.close()
    
    def read_keys(self):
        print('\nReading keys from desktop...')
        privatepath = r"C:/Users/"+self.name+"/Desktop/myprivate.txt"
        private = open(privatepath,"r") #"w+" is for overwriting previous contents
        self.private_key = int(private.readline())
        private.close()
        print("Read private key:",self.private_key)

        npath = r"C:/Users/"+self.name+"/Desktop/myN.txt"
        n = open(npath,"r")
        self.n = int(n.readline())
        n.close()
        print("Read n value:", self.n)
        
        publicpath = r"C:/Users/"+self.name+"/Desktop/mypublic.txt"
        public = open(publicpath,"r")
        self.public_key = int(public.readline())
        public.close()
        print("Read public key:",self.public_key)


    def read_friend_keys(self):
        npath = r"C:/Users/"+self.name+"/Desktop/myfriendN.txt"
        n = open(npath,"r")
        self.friend_n = int(n.readline())
        n.close()
        print("Read friend n value:", self.friend_n)
        
        publicpath = r"C:/Users/"+self.name+"/Desktop/myfriendpublic.txt"
        public = open(publicpath,"r")
        self.friend_public_key = int(public.readline())
        public.close()
        print("Read friend public key:",self.friend_public_key)


    def encrypt_with_friend_key(self):#encrypts a message with a friend's public key for them to decrypt and read later.
        self.read_friend_keys()
        
        self.input_to_ASCII() #gathers input to be used for message

        self.encrypt(self.ascII_list, self.friend_public_key, self.friend_n)
        
        
        print('\nSaving message to desktop...')
        mypath = r"C:/Users/"+self.name+"/Desktop/friendmsg.txt"
        msg = open(mypath,"w+") #"w+" is for overwriting previous contents
    
        temp_len = len(self.encrypted_list)
        templst=[]
        for i in range(temp_len): #converting every element in encrypted_list to str
            templst.append(str(self.encrypted_list[i]))
        formatted_output = " ".join(templst)
        msg.writelines(formatted_output)
        msg.close()

        print('Copying to clipboard...')
        self.copy2clip(formatted_output)

    def decrypt_friend_msg_from_file(self):
        print('\nReading my keys...')
        self.read_keys()
        
        print('\nOpening encrypted message from friend...')
        mypath = r"C:/Users/"+self.name+"/Desktop/friendmsg.txt"
        friendmsg = open(mypath,"r")
        templst = friendmsg.readline() #reading in
        templst = templst.split(' ') #splitting at whitespaces
        #print(templst)
        temp_len = len(templst) 
        for i in range(temp_len): #converting every element in decrypted_list to int
            self.encrypted_list.append(int(templst[i]))
        
        #print(self.encrypted_list)
        self.decrypt()
        self.get_char_output()

    def decrypt_friend_msg_from_terminal(self):
        print('\nReading my keys...')        
        self.read_keys()
        user_input = input('Please enter your encrypted message\n')
        user_input = user_input.split(' ')

        temp_len = len(user_input) 

        for i in range(temp_len): #converting every element in decrypted_list to int
            self.encrypted_list.append(int(user_input[i]))

        self.decrypt()
        self.get_char_output()
        
        
    #fine tuning for later:
    #   had self variable for RSA class that is self.e_limiter for the e finding function  
#----------------------------------------------------------------------------------#  
# Main Program
rsa_algo = RSA()

#----------------Generating new public and private keys, not necessary for every run---------#
#rsa_algo.generate_keys()#only use when you want new keys
#rsa_algo.save_keys()
#rsa_algo.read_keys()


#----------------Encrypting a personal message with own public key---------#
#rsa_algo.encrypt()
#encrypted_num = rsa_algo.get_encrypted_list()
#print( "\nEncrypted numbers:",encrypted_num)

#----------------Decrypting a personal message with own private key---------#
#rsa_algo.decrypt()
#decrypted_num = rsa_algo.get_decrypted_list()
#print("\nDecrypted numbers:",decrypted_num)
#rsa_algo.get_char_output()


#----------------Encrypting message for a friend to read---------#
#rsa_algo.encrypt_with_friend_key()

#-------------Reading encrypted friend messages with your private key---------------------------#
#rsa_algo.decrypt_friend_msg_from_file() #used to decrypt encrypted text files
#rsa_algo.decrypt_friend_msg_from_terminal() #decrypts a message copied and pasted into terminal
