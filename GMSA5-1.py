
# coding: utf-8

# In[ ]:


import random
import time
import speech_recognition as sr


## Register ##
class LFSR:

    def __init__(self,i,length,clockingBit,tappedBits): 
        self.i= i
        self.length= length
        self.register= [0]*length
        self.clockingBit= clockingBit
        self.tappedBits = tappedBits
    def _getID(self):
        return self.i
    def _getRegister(self):
        return self.register
    def _getBit(self,i):
        return self.register[i]
    def _getLength(self):
        return self.length
    def _getClockingBit(self): 
        return self.register[self.clockingBit]
    def _getTappedBits(self): 
        return self.tappedBits
    
    def _setID(self,i):
        self.i = i
    def _setLength(self,length):
        self.length = length
    def _setRegister(self,register):
        self.register = register
    def _setClockingBit(self,clockingBit):
        self.clockingBit = clockingBit
    def _setTappedBits(self,tappedBits):  
        self.tappedBits = tappedBits


## Utils ##
def xor(x,y): return 0 if x==y else 1

def stepOne(): return (LFSR(1,19,8,[13,16,17,18]),LFSR(2,22,10,[20,21]),LFSR(3,23,10,[7,20,21,22]))

def stepTwo(lfsrOne,lfsrTwo,lfsrThree,sessionKey):
    for bit in sessionKey:
        bit = int(bit)
        # LFSRONE #
        nMsb = xor(xor(xor(xor(lfsrOne._getBit(13),lfsrOne._getBit(16)),lfsrOne._getBit(17)),lfsrOne._getBit(18)),bit)	
        lfsrOne._setRegister([nMsb]+lfsrOne._getRegister()[0:lfsrOne._getLength()-1])
        # LFSRTWO #
        nMsb = xor(xor(lfsrTwo._getBit(20),lfsrTwo._getBit(21)),bit)
        lfsrTwo._setRegister([nMsb]+lfsrTwo._getRegister()[0:lfsrTwo._getLength()-1])
        # LFSRTHREE #
        nMsb = xor(xor(xor(xor(lfsrThree._getBit(7),lfsrThree._getBit(20)),lfsrThree._getBit(21)),lfsrThree._getBit(22)),bit)
        lfsrThree._setRegister([nMsb]+lfsrThree._getRegister()[0:lfsrThree._getLength()-1])


def stepFour(lfsrOne,lfsrTwo,lfsrThree):
    for i in range(80):
        clockingBits = [lfsrOne._getClockingBit(),lfsrTwo._getClockingBit(),lfsrThree._getClockingBit()]
        oneCount,zeroCount = clockingBits.count(1),clockingBits.count(0)
        majorityBit  = 1 if max(oneCount,zeroCount)==oneCount else 0
        # LFSRONE #
        if lfsrOne._getClockingBit()==majorityBit:
            nMsb = xor(xor(xor(lfsrOne._getBit(13),lfsrOne._getBit(16)),lfsrOne._getBit(17)),lfsrOne._getBit(18))
            lfsrOne._setRegister([nMsb]+lfsrOne._getRegister()[0:lfsrOne._getLength()-1])
            # LFSRTWO #
        if lfsrTwo._getClockingBit()==majorityBit:
            nMsb = xor(lfsrTwo._getBit(20),lfsrTwo._getBit(21))
            lfsrTwo._setRegister([nMsb]+lfsrTwo._getRegister()[0:lfsrTwo._getLength()-1])
        # LFSRTHREE #
        if lfsrThree._getClockingBit()==majorityBit:
            nMsb = xor(xor(xor(lfsrThree._getBit(7),lfsrThree._getBit(20)),lfsrThree._getBit(21)),lfsrThree._getBit(22))
            lfsrThree._setRegister([nMsb]+lfsrThree._getRegister()[0:lfsrThree._getLength()-1])

def stepFive(lfsr1,lfsr2,lfsr3):
    keyStream = ""
    keyStream += str(lfsrOne._getBit(lfsrOne._getLength()-1)^lfsrTwo._getBit(lfsrTwo._getLength()-1)^lfsrThree._getBit(22))	
    for i in range(63):
        clockingBits = [lfsrOne._getClockingBit(),lfsrTwo._getClockingBit(),lfsrThree._getClockingBit()]
        oneCount,zeroCount = clockingBits.count(1),clockingBits.count(0)
        majorityBit  = 1 if max(oneCount,zeroCount)==oneCount else 0
        # LFSRONE #
        if lfsrOne._getClockingBit()==majorityBit:
            nMsb = xor(xor(xor(lfsrOne._getBit(13),lfsrOne._getBit(16)),lfsrOne._getBit(17)),lfsrOne._getBit(18))
            lfsrOne._setRegister([nMsb]+lfsrOne._getRegister()[0:lfsrOne._getLength()-1])	
        # LFSRTWO #
        if lfsrTwo._getClockingBit()==majorityBit:
            nMsb = xor(lfsrTwo._getBit(20),lfsrTwo._getBit(21))
            lfsrTwo._setRegister([nMsb]+lfsrTwo._getRegister()[0:lfsrTwo._getLength()-1])
        # LFSRTHREE #
        if lfsrThree._getClockingBit()==majorityBit:
            nMsb = xor(xor(xor(lfsrThree._getBit(7),lfsrThree._getBit(20)),lfsrThree._getBit(21)),lfsrThree._getBit(22))
            lfsrThree._setRegister([nMsb]+lfsrThree._getRegister()[0:lfsrThree._getLength()-1])
        keyStream += str(lfsrOne._getBit(lfsrOne._getLength()-1)^lfsrTwo._getBit(lfsrTwo._getLength()-1)^lfsrThree._getBit(22))	
    return keyStream

Start_time = time.time()
r= sr.Recognizer()
def header():
    print ("well come to python ")
    
with sr.Microphone() as source:
    print ("Say somethings :")
    audio_1= r.listen(source)
    print (time.time()-Start_time)
    
    print ("Done!")
   # audio_2 = r.listen(source)
    
   # print ("Done!")
    
try: 
    result1 = r. recognize_google(audio_1)
   # result2 = r. recognize_google(audio_2)
    print (result1)
    
    #print (result2)
except Exception as e:
    print (e)
def stepSix(plainText,keyStream): return "".join([str(xor(keyStream[i%64],plainText[i])) for i in range(len(plainText))])

def padding64(plainText):
    while len(plainText)%64!=0: plainText += "1"
    return plainText

if __name__ == "__main__":
    header()
    d= {result1}
    plainText= padding64(result1)
    print(" Plaintext String : " + result1)
    # Step One #
    print ("\nInitializing LFSR...") 
    lfsrs = stepOne()
    lfsrOne,lfsrTwo,lfsrThree = lfsrs[0],lfsrs[1],lfsrs[2]
    # Step Two #
    number = random.randint(1,10)
    str_number = str(number)
    sessionKey = padding64(str_number)
    print("64 bits key: "+ str_number)
    stepTwo(lfsrOne,lfsrTwo,lfsrThree,sessionKey)
    print( "\nLFSR after step two:")
    print (lfsrOne._getRegister())
    print (lfsrTwo._getRegister())
    print ( lfsrThree._getRegister())
    print ("\n\n")
    # Step Three #
    print ("LFSR after step three:")
    print (lfsrOne._getRegister())
    print (lfsrTwo._getRegister())
    print (lfsrThree._getRegister())
    print ("\n\n")
    # Step Four  #
    print ("LFSR after step four:")
    #lfsrThree._setRegister([0,0,0,0,1,0,1,1,0,0,0,1,1,0,0,1,1,0,1,0,0,1,0])
    stepFour(lfsrOne, lfsrTwo, lfsrThree)
    print (lfsrOne._getRegister())
    print (lfsrTwo._getRegister())
    print (lfsrThree._getRegister())    
    #lfsrThree._setRegister([0,0,0,0,1,0,1,1,0,0,0,1,1,0,0,1,1,0,1,0,0,1,0])
    #print (lfsrThree._getRegister())  
    print ("\n\n")
    # Step Five #
    print ("KeyStream 64b generated:")
    keyStream  = stepFive(lfsrOne,lfsrTwo,lfsrThree)
    print (keyStream)
    # Step Six  #
    print ("\nCipher text:")
    cipherText = stepSix(plainText,keyStream)
    print (cipherText,"\n\n")

