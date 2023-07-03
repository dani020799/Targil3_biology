import sys
#import numpy as np
import random


lines1=[]
lines2=[]

class  prigma:
    def __init__ (self,wights,n1,n2):
        self.wights=wights
        self.nuro1= nuroin(n1)
        self.nuro2 = nuroin(n2)
        self.andgate= nuroin(-150)
        self.fitnees=0


    def calculatefittnes(self,bits,expected):

      nuro1result=self.nuro1.output(bits,[ a for (a,b) in self.wights])
      nuro2result = self.nuro2.output(bits,[ b for (a,b) in self.wights])
      result=self.andgate.output([nuro1result,nuro2result],[100,100])
      if result== expected:
          self.fitnees=self.fitnees+1

    def test (self,bits,expected):
        nuro1result = self.nuro1.output(bits, [a for (a, b) in self.wights])
        nuro2result = self.nuro2.output(bits, [b for (a, b) in self.wights])
        result = self.andgate.output([nuro1result, nuro2result], [100, 100])
        return (result == expected)

    def run(self,bits):
        nuro1result = self.nuro1.output(bits, [a for (a, b) in self.wights])
        nuro2result = self.nuro2.output(bits, [b for (a, b) in self.wights])
        result = self.andgate.output([nuro1result, nuro2result], [100, 100])
        return result



class nuroin :

     def __init__(self, bias ):
        self.bias=bias


     def  sigmoid(self,x):
        """Sigmoid function"""
        return (x>0)
       # return (1.0 / (1.0 + np.exp(-x)))

     def output (self,inp,whights):
         w=0
         j=0
         for i in inp:

             w=w+ i*whights[j]
             j=j+1
         sig=( w + self.bias)
         return self.sigmoid(sig)





def read_files(file1, file2):
    global  lines1, lines2

    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            lines1 = [line.rstrip() for line in f1]
            lines2 = [line.rstrip() for line in f2]
            #print(f"Contents of {file1}:")
           # print(lines1)
           # print(f"\nContents of {file2}:")
           # print(lines2)

    except FileNotFoundError:
        print("One or both files could not be found.")
    except IOError:
        print("An error occurred while reading the files.")




def cross(p1,p2):

    neww=[]
    for i in range(16):
        (a,b)=p1.wights[i]
        (c, d) = p2.wights[i]
        newww=float((b+d)/2)+random.randint(-3,3)
        w= (-1*newww,newww)
        neww.append(w)
    newn2bias = float((p1.nuro2.bias + p2.nuro2.bias) / 2.0)
    newn1bias = float((p1.nuro1.bias + p2.nuro1.bias) / 2.0)
    newp=prigma(neww,newn1bias, newn2bias)

    return newp

def cross2(p1,p2):

    crossover_point = random.randint(1, 16 - 1)
    neww=p1.wights[:crossover_point] + p2.wights[crossover_point:]
    for i in range(16):
        (a,b)=neww[i]
        b=b+ random.randint(-3,3)
        neww[i]= (-1*b,b)
    newn2bias = float((p1.nuro2.bias + p2.nuro2.bias) / 2.0)
    newn1bias = float((p1.nuro1.bias + p2.nuro1.bias) / 2.0)
    newp=prigma(neww,newn1bias, newn2bias)

    return newp


def createnewp():
    random.seed(a=None, version=2)
    whights=[]
    for i in range(16):
        r = random.uniform(0, 100)

        whights.append((-1.0*r,r))
    arraysum=0
    for w in whights:
        (a,b) =w
        arraysum=arraysum +b
    bais1= float(random.randint(0, int(arraysum)) )
    bais2 = -1*float(random.randint(0, int(arraysum)))
    return prigma(whights,bais1,bais2)




def main():
    global lines1, lines2
    random.seed(a=None, version=2)
    populationnum=150
    if len(sys.argv) == 3:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        read_files(file1, file2)
    else:
        print("Please provide two file names as command-line arguments.")

    trainlines=[ ]
    testlines=[]
    for l in lines1:
        splitt= l.split("   ")
        bits=[int(bit) for bit in splitt[0]]
        expected=int(splitt[1])
        trainlines.append((bits,expected))
    for l in lines2:
        splitt = l.split("   ")
        bits = [int(bit) for bit in splitt[0]]
        expected = int(splitt[1])
        testlines.append((bits, expected))
    population=[]

    for i in range(populationnum):
        #r=  random.randint(0,16)*100 +50
       # r1 = random.randint(-16, 0)*100 -50
      #  p= prigma([(float (1/r), float (1/r1)) for _ in range(16)],random.randint(0, 16),random.randint(0, 16))
        #p = prigma([(-100, 100) for _ in range(16)], r, r1)
        population.append(createnewp())

    bestfittnes=population[0].fitnees
    bestp = population[0]
    generation=1
    bestlist=[]
    avglist=[]
    lineslen= len(trainlines)
    l=0
    while (bestfittnes<lineslen*0.99):
        avg=0
        for l in range(lineslen):
           # print(trainlines[l])
            (a,b) =trainlines[l]
            for index in range(populationnum):
             avg2 =0
             if generation ==2:
              t=5
             myp=population[index]
             try:
               myp.calculatefittnes(a,b)

             except:
                 h=5
             #avg2=avg2+myp.fitnees
             if bestfittnes < myp.fitnees:
                bestfittnes=myp.fitnees
                bestp=myp
           # avg=avg +float(avg2/populationnum)
        for index in range(populationnum):
            avg=avg+population[index].fitnees

        avg=float(avg/populationnum)
        population=sorted(population, key=lambda p: -1*p.fitnees)
        bestlist.append(bestfittnes)
        avglist.append(avg)

        whights=[p.fitnees  for p in population]
        population[0].fitnees = 0
        newpopulation=[]
        population[0].fitnees=0
        newpopulation.append(population[0])
        l=0

        while len(newpopulation) <populationnum:
            if  len(newpopulation)<populationnum/8:
                r=random.randint(0,15)
                r1 = random.randint(0,15)
                p1=population[r]
                p2 = population[r1]

               # newwights=[]
              #  for (a1,b1) in p1.wights:
                   # (a2,b2) =p2.wights
                   # neww= (((a1+a2)/2),((b1+b2)/2))
                   # newwights.append(neww)

                newp= cross(p1,p2)
                newpopulation.append(newp)
                newpopulation.append(cross2(p1,p2))
            elif  float(populationnum/8)<float(len(newpopulation)<populationnum/3) <float((populationnum*9)/10):

                newpopulation.append(cross(random.choices(population, whights)[0]),cross(random.choices(population, whights)[0]))
                newpopulation.append(cross2(random.choices(population, whights)[0]),   cross(random.choices(population, whights)[0]))


            else:
                newpopulation.append(createnewp())

        population= newpopulation
        generation =generation +1
      #  print(l)
        print ("\nbest fit: " +str(bestfittnes)+ "\n")
        print("\navg fit: " + str(avg) + "\n")
        print(bestp.wights)
        print(bestp.nuro1.bias)
        print(bestp.nuro2.bias)

    counter=0
    for l in testlines:
            (a, b) = l

            if bestp.test(a,b):
                counter=counter+1
    i=1
    '''
    with open('bestfit.csv', 'w') as file:
        for best in bestlist:
            file.writelines(str(i)+","+str(best)+"\n")
            i=i+1
    i = 1
    with open('avgfit.csv', 'w') as file:
        for avg in avglist:
            file.writelines(str(i) + "," + str(avg) + "\n")
            i = i + 1
    '''



    print (float(counter/len(testlines)))
    with open('wnet0.txt', 'w') as file:
        for (a,b) in bestp.wights:
            file.writelines(str(b)+'\n')

        file.writelines(str(bestp.nuro1.bias)+"\n"+str(bestp.nuro2.bias))







if  __name__ == '__main__':
    main()