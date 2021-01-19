import numpy as np
from bitarray import bitarray

def write(array, number, lenght):
    first = "{0:b}".format(number)
    for i in range(lenght-len(first)):
        array.append(0)
    for i in range(len(first)):
        if(first[i] == '1'):
            array.append(1)
        else:
            array.append(0)

def shift(number, neg, pos):
    if(number<0):
        return number+neg
    return number+pos

def re_shift(number, neg, pos, half):
    if(number<half):
        return number-neg
    return number-pos


def repeats(array, number):
    array.append(0)
    array.append(1)
    write(array, number-1, 3)

def MM(string):
    seznam = np.array([])
    for i in range (len(string)):
        seznam = np.append(seznam,  ord(string[i]))
    seznam = seznam.astype(int)

    for i in range(seznam.shape[0]-1, 0, -1):
        seznam[i] = seznam[i] - seznam[i-1]   
    out = bitarray()
    counter = 0

    write(out, seznam[0], 8)
    for i in range(1, seznam.shape[0]):
        if not (seznam[i] == 0):
            if(counter != 0):
                repeats(out, counter)
                counter = 0
            
            if(abs(seznam[i])<=30):
                out.append(0)
                out.append(0)
                if(abs(seznam[i])<=2):
                    out.append(0)
                    out.append(0)
                    write(out, shift(seznam[i], 2, 1),2)
                elif (abs(seznam[i])<=6):
                    out.append(0)
                    out.append(1)
                    write(out, shift(seznam[i], 6, 1),3)
                elif (abs(seznam[i])<=14):
                    out.append(1)
                    out.append(0)
                    write(out, shift(seznam[i], 14, 1),4)
                elif (abs(seznam[i])<=30):
                    out.append(1)
                    out.append(1)
                    write(out, shift(seznam[i], 30, 1),5)
            else:
                out.append(1)
                out.append(0)
                if(seznam[i]>=0):
                    out.append(0)
                else:
                    out.append(1)
                write(out, seznam[i], 8)
        else:
            counter = counter + 1
            if(counter == 8):
                repeats(out, counter)
                counter = 0

    if(counter != 0):
        repeats(out, counter)
    out.append(1)
    out.append(1)
    return out

def bin_to_int(array):
    x = 0
    for bit in array:
        x = (x << 1) | bit 
    return x

def IMM(input):
    out = np.array([])
    out = np.append(out, bin_to_int(input[0:8]))
    
    i = 8
    while(True):
        if(input[i:i+2] == bitarray('00')):
            i += 2
            if(input[i:i+2] == bitarray('00')):
                i += 2
                out = np.append(out, re_shift(bin_to_int(input[i:i+2]), 2, 1, 2))
                i += 2
            elif(input[i:i+2] == bitarray('01')):
                i += 2
                out = np.append(out, re_shift(bin_to_int(input[i:i+3]), 6, 1, 4))
                i += 3
            elif(input[i:i+2] == bitarray('10')):
                i += 2
                out = np.append(out, re_shift(bin_to_int(input[i:i+4]), 14, 1, 8))
                i += 4
            elif(input[i:i+2] == bitarray('11')):
                i += 2
                out = np.append(out, re_shift(bin_to_int(input[i:i+5]), 30, 1, 16))
                i += 5#kodeiranje

        elif(input[i:i+2] == bitarray('01')):
            #ponovitve ničel
            i += 2
            out = np.append(out, np.zeros(1+(bin_to_int(input[i:i+3]))))
            i += 3

        elif(input[i:i+2] == bitarray('10')):
            i += 2
            x = bin_to_int(input[i+1:i+9])
            if(input[i]):
                x = -x
            out = np.append(out, x)
            i += 9
        elif(input[i:i+2] == bitarray('11')):
            break

    for i in range(1, out.shape[0]):
        out[i] = out[i] + out[i-1]
    out = out.astype(np.int)

    string = ""
    for i in range(len(out)):
        string += chr(out[i])
    
    return string