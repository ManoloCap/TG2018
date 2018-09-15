"""
Algoritmo Genético Prueba Problema de "Lunes"

"""
import random
# objeto Curso definido
class course:
    
    def __init__(self,name,periods,code):
        
        self.name = name
        self.periods = periods
        self.code = code

class teacher:

    def __init__(self,name,maxCourses):
        
        self.name = name
        self.maxCourses = maxCourses
    
# Objetos Curso a programar
circuitos_1 = course("Circuitos 1",2,1)
digital = course("Digital", 2, 2)
micro = course("Microcontroladores", 3,3)
maxCode = 3
# Objetos Profesor a programar
M = teacher("M",99)
K = teacher("K",99)
P = teacher("P",99)

# Lista de cursos a programar
coursesList = [circuitos_1, digital, digital, micro, micro] 


# Muestra nombres de los cursos a programar
"""
print "Los cursos a programar son: "

for i in range(len(coursesList)):
    print(coursesList[i].name+",  ")
"""

# Inicialización de poblacion en funcion de los periodos y tamaño de población ( 0 significa que el periodo está libre )
totalPeriods = 17
population = 100
mondayVector = []
mondayVectorList = []

for i in range(population):
    for i in range(totalPeriods):
        mondayVector.append(random.randrange(0,4,1))
    mondayVectorList.append(mondayVector)
    #print mondayVector #print de individuo
    mondayVector = []

#Calculo de Periodos necesitados
usedPeriods = 0
for i in range(len(coursesList)):
    usedPeriods = usedPeriods + coursesList[i].periods
emptyPeriods = totalPeriods - usedPeriods


# Se calculan cuantos periodos se necesitna de cada curso
totalPeriodsList = {}
for i in range(len(coursesList)):
    #Se suman cuantos periodos se necesitan de cada curso
    if(coursesList[i].code in totalPeriodsList):
        totalPeriodsList[coursesList[i].code] = totalPeriodsList[coursesList[i].code] + coursesList[i].periods
    elif( coursesList[i].code != totalPeriodsList):
        totalPeriodsList.update({coursesList[i].code : coursesList[i].periods } )
        
            
# Funcion de aptitud
def fitnessF(mondayVector, teacher, coursesList , emptyPeriods, totalPeriodsList):
    points = 0
    
    
    for i in range(len(coursesList)):
                 
        #print(totalPeriodsList)
        
        #Puntos por tener la misma cantidad de periodos de un curso específico
        #if(mondayVector.count(coursesList[i].code) == coursesList[i].periods):
            #points = points + 100
        
        #Puntos por tener periodos seguidos de un curso en específico
        #for e in range(len(mondayVector)-2):
            #if((mondayVector[e] == mondayVector[e+1]) and (mondayVector[e] == coursesList[i].code) ):
                #points = points + 5
            #else:
                #points = points - 10
        #Puntos por tener periodos seguidos de un curso en específico v2        
        mondayVectorCounter = 0       
        for e in range(len(mondayVector)-1):
            if(mondayVector[e] == coursesList[i].code):
                points = points + 10
                mondayVectorCounter = mondayVectorCounter + 1
                if(mondayVector[e+1] == coursesList[i].code and coursesList[i].code >= 2):
                    points = points + 10
                if(mondayVectorCounter == coursesList[i].periods):
                    points = points + 120
                    break
            else:
                mondayVectorCounter = 0
            
            if(e == len(mondayVector)-2) :
                points = points - 120
                
            
    for n in range(1 , max(totalPeriodsList) + 1):
        #print n
        if( mondayVector.count(n) == totalPeriodsList[n] ):
            #print "Sume puntos por totalPeriodsList: "+str( mondayVector.count(n) ) + " : " + str( totalPeriodsList[n])
            points = points + 300
        else:
            #print "NO Sume puntos por totalPeriodsList: "+str( mondayVector.count(n) ) + " : " + str( totalPeriodsList[n])
            points = points - 300
    

    if( mondayVector.count(0) == emptyPeriods):
        points = points + 150
    else:
        points = points - 50 

    return points

#  -------------------  ALGORITMO GENÉTICO ---------------------------
#print totalPeriodsList #print del total de periodos necesitado

nGenMax = 100            # Número máximo de Iteraciones
showUpThan =  1000     # Número máximo para mostrar individuos
printWithPoints = 1 # Activar print de resultados
for f in range(nGenMax):
    #Vectorde Puntos para cada individuo de la población
    pointsList = []
   
    for i in range(len(mondayVectorList)):
        pointsList.append(0)
    
    
    
    # EVALUACIÓN
    for i in range(len(mondayVectorList)):
        pointsList[i] = fitnessF(mondayVectorList[i], 1, coursesList, emptyPeriods, totalPeriodsList)
        if(pointsList[i] > showUpThan and printWithPoints == True):
            print "puntos "+str(pointsList[i])
            print mondayVectorList[i]
            print "codigo 1:  "+str(mondayVectorList[i].count(1))
            print "codigo 2:  "+str(mondayVectorList[i].count(2))
            print "codigo 3:  "+str( mondayVectorList[i].count(3))
    
    #print str(pointsList)
    
    # SELECCIÓN
    maxNumber = 3
    minNumber = 1
    new_mondayVectorList = []
    bestLocation = 0

    # SE DEJARÁN CIERTO NUMERO DE MEJORES INDIVIDUOS Y CIERTO NUMERO DE PEORES INDIVIDUOS
    
    # los maxNumber sobrevivientes
    for i in range(maxNumber):
        m = max(pointsList)
        location = [n for n, j in enumerate(pointsList) if j == m][0]
        new_mondayVectorList.append(mondayVectorList[location])
        # SE GUARDA LA LOCALIDAD DE LA MEJOR SOLUCION
        if(i == 0):
            bestLocation = location
        del mondayVectorList[location]
        del pointsList[location]
        #print location
    
    # Los minNumber sobrevivientes
    for i in range(minNumber):
        m = min(pointsList)
        location = [i for i, j in enumerate(pointsList) if j == m][0]
        new_mondayVectorList.append(mondayVectorList[location])
        del mondayVectorList[location]
        del pointsList[location]
        #print location
        
    #print len(new_mondayVectorList)
    
    #print bestLocation
    # REPRODUCCION
    originalLen = len(new_mondayVectorList)
    for i in range(len(new_mondayVectorList), population):
        new_mondayVectorList.append(new_mondayVectorList[random.randrange(0,originalLen,1)])
    
    mondayVectorList = new_mondayVectorList
    #print new_mondayVectorList
        
    # CROSSORVER
    #Numero maximo de movimientos
    maxMovements = 4
    maxMovementAmount = 4
    movement = []
    randomNumbers = [0,1]
    selectedMonday = [0,1]
    for i in range(maxMovements):
        randomNumbers[0] = random.randrange(0,maxMovementAmount,1)
        randomNumbers[1] = random.randrange(0,maxMovementAmount,1)
        selectedMonday[0] = random.randrange(0,population,1)
        selectedMonday[1] = random.randrange(0,population,1)
        #print selectedMonday
        
        movement = mondayVectorList[selectedMonday[0]][min(randomNumbers):max(randomNumbers)]
        #print movement
        # si no es la mejor solucion hasta el momento, puede hacer el crossover
        #if(selectedMonday[0] != bestLocation):
        mondayVectorList[selectedMonday[0]][min(randomNumbers):max(randomNumbers)] = mondayVectorList[selectedMonday[1]][min(randomNumbers):max(randomNumbers)]
           
        #if( selectedMonday[1] != bestSolutionLocation):
        mondayVectorList[selectedMonday[1]][min(randomNumbers):max(randomNumbers)] = movement
            
    #print mondayVectorList
            
    # MUTACION
    maxMutations = 5
    
    for i in range(maxMutations):
        mondayVectorList[random.randrange(0,population,1)][random.randrange(0,totalPeriods,1)] = random.randrange(0,maxCode,1)
    
    #print mondayVectorList