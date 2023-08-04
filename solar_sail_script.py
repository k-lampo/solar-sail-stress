import math
import matplotlib as plt

#-----USER-INPUTTED VALUES-----

#Reference: Types of Untapered Ribbon
#  Same Velocity - This type of untapered ribbon achieves the same maximum velocity as the tapered ribbon, but does so at the cost of increased material and mass.
#  Same Mass - This type of untapered ribbon has the same mass and amount of material as the tapered ribbon, but is unable to reach the same maximum velocity.

#display options (1 for yes, 0 for no)
displayUserInputs = 0 #prints out user-inputted values
displayTaperSections = 0 #prints out width & material for each taper section
displaySummary = 1 #prints out summary statistics

#paddle properties
paddleWidth = 100 #meters
paddleThickness = 0.01 #meters
paddleHeight = 200 #meters
paddleTensileStrength = 63000000000 #Pa
paddleMaterialDensity = 1380 #kg m^-3
paddleMass = paddleWidth * paddleThickness * paddleHeight * paddleMaterialDensity #kg
linearPaddleDensity = paddleMass / paddleHeight #kg m^-1

#ribbon properties
ribbonThickness = 0.01 #meters
ribbonLength = 200 #meters
ribbonTensileStrength = 63000000000 #Pa
ribbonMaterialDensity = 1380 #kg m^-3

#desired angular velocity
angularVelocity = 35 #rad s^-1
linearVelocity = angularVelocity * (ribbonLength / 2 + paddleHeight) /1000 #km s^-1

#number of taper sections (for one half of the ribbon)
numberSections = 100

#----END OF USER-INPUTTED VALUES-----





#display user-defined values
if(displayUserInputs == 1):
  print("-----User-Defined Values-----")
  print ("{:<25} {:<12} {:<10}".format("ATTRIBUTE", "VALUE", "DIMENSION"))
  
  print ("{:<25} {:<12} {:<10}".format("Paddle Width", paddleWidth, "meters"))
  print ("{:<25} {:<12} {:<10}".format("Paddle Thickness", paddleThickness, "meters"))
  print ("{:<25} {:<12} {:<10}".format("Paddle Height", paddleHeight, "meters"))
  print ("{:<25} {:<12} {:<10}".format("Paddle Tensile Strength", paddleTensileStrength, "Pa"))
  print ("{:<25} {:<12} {:<10}".format("Paddle Material Density", paddleMaterialDensity, "kg m^-1"))
  
  print()
  
  print ("{:<25} {:<12} {:<10}".format("Ribbon Thickness", ribbonThickness, "meters"))
  print ("{:<25} {:<12} {:<10}".format("Ribbon Length", ribbonLength, "meters"))
  print ("{:<25} {:<12} {:<10}".format("Ribbon Tensile Strength", ribbonTensileStrength, "Pa"))
  print ("{:<25} {:<12} {:<10}".format("Ribbon Material Density", ribbonMaterialDensity, "kg m^-1"))
  
  print()
  
  print ("{:<25} {:<12} {:<10}".format("Angular Velocity", angularVelocity, "rad s^-1"))
  print ("{:<25} {:<12} {:<10}".format("(Linear Velocity)", format(linearVelocity,".4f"), "km s^-1"))
  
  print()





#-----UNTAPERED RIBBON CALCULATIONS-----
#calculate untapered width needed to reach specified angular velocity
neededUntaperedWidth = (linearPaddleDensity * (paddleHeight**2 + ribbonLength * paddleHeight)) / (ribbonThickness * (2 * ribbonTensileStrength / angularVelocity**2 - ribbonMaterialDensity * (ribbonLength**2 / 4))) #m

#calculate untapered material needed
untaperedMaterialNeeded = neededUntaperedWidth * ribbonLength * ribbonThickness #m^3

#calculate untapered mass
untaperedMass = untaperedMaterialNeeded * ribbonMaterialDensity #kg





#-----FRIST TAPER SECTION CALCULATIONS-----
#create array with taper sections using ribbon length & number of sections
stepSize = (ribbonLength / 2) / numberSections
currentValue = ribbonLength / 2
sectionList = [currentValue]
i = numberSections
while i > 0:
  currentValue = currentValue - stepSize
  sectionList.append(currentValue)
  i = i - 1

#calculate necessary width for the first (outermost) section
necessaryWidth = (linearPaddleDensity * (paddleHeight**2 + ribbonLength * paddleHeight)) / (ribbonThickness * (2 * ribbonTensileStrength / angularVelocity**2 - ribbonMaterialDensity * (ribbonLength**2 / 4 - sectionList[1]**2))) #m

#calculate tension at the innermost edge of this section
newTension = 0.5 * angularVelocity**2 * (linearPaddleDensity * (paddleHeight**2 + ribbonLength * paddleHeight) + ribbonMaterialDensity * ribbonThickness * necessaryWidth * (ribbonLength**2 / 4 - sectionList[1]**2))

#calculate material used for the first section
materialUsed = necessaryWidth * stepSize * ribbonThickness

#append these values to the output array
outputArray = [[1,sectionList[1],necessaryWidth,materialUsed]]





#-----TAPERED RIBBON CALCULATIONS (SAME VELOCITY)-----
#repeat for all sections
j = 1
while j < numberSections:
  #calculate necessary width for this section
  necessaryWidth = newTension / (ribbonThickness * (ribbonTensileStrength - 0.5 * ribbonMaterialDensity * angularVelocity**2 * (sectionList[j]**2 - sectionList[j+1]**2)))

  #calculate tension at the innermost edge of this section
  newTension = newTension + 0.5 * ribbonMaterialDensity * ribbonThickness * necessaryWidth * angularVelocity**2 * (sectionList[j]**2 - sectionList[j+1]**2)

  #calculate material used for this section
  materialUsed = necessaryWidth * stepSize * ribbonThickness
  
  #append these values to the output array
  outputArray.append([j + 1,sectionList[j + 1],necessaryWidth,materialUsed])
  
  j = j +1

#calculate tapered material needed
taperedMaterialNeeded = 0
for x in outputArray:
  taperedMaterialNeeded = taperedMaterialNeeded + x[3]
taperedMaterialNeeded = taperedMaterialNeeded * 2 #m^3

#calculate tapered mass
taperedMass = taperedMaterialNeeded * ribbonMaterialDensity #kg





#-----TAPERED RIBBON CALCULATIONS (SAME MASS)-----
#calculate width of an untapered system with the same mass as the tapered one
sameMassTaperedWidth = taperedMass / (ribbonThickness * ribbonLength * ribbonMaterialDensity)

#calculate the angular velocity of that system
sameMassTaperedAngularVelocity = math.sqrt((2 * sameMassTaperedWidth * ribbonThickness * ribbonTensileStrength) / (linearPaddleDensity * (paddleHeight**2 + ribbonLength * paddleHeight) + ribbonMaterialDensity * ribbonThickness * sameMassTaperedWidth * (ribbonLength**2 * 0.25)))

#calculate the linear velocity of that system
sameMassTaperedLinearVelocity = sameMassTaperedAngularVelocity * (ribbonLength * 0.5 + paddleHeight) / 1000





#-----RESULTS-----
if(displayTaperSections == 1):
  #display taper results
  print("-----Taper Sections-----")
  print("Number of Sections: ", numberSections)
  print("Section Size: ", format(stepSize,".2f"), "meters")
  
  print()
  
  print ("{:<10} {:<18} {:<18} {:<18}".format("SECTION", "MIN. RADIUS (m)", "WIDTH (m)", "MATERIAL USED (m^3)"))
  
  k = 0
  while k < numberSections:
    print ("{:<10} {:<18} {:<18} {:<18}".format(outputArray[k][0], outputArray[k][1], format(outputArray[k][2],".4f"), format(outputArray[k][3],".4f")))
    k = k + 1
  
  print()

#display summary

if(displaySummary == 1):
  print("----Summary-----")
  
  print ("{:<22} {:<15} {:<15} {:<17} {:<20} {:<20}".format("TYPE", "MAX WIDTH (m)", "MASS (kg)", "MATERIAL (m^3)", "ANG. VEL. (rad/s)", "LIN. VEL. (km/s)"))
  
  print ("{:<22} {:<15} {:<15} {:<17} {:<20} {:<20}".format("Tapered", format(outputArray[numberSections-1][2],".4f"), format(taperedMass,".4f"), format(taperedMaterialNeeded,".4f"), angularVelocity, linearVelocity))
  
  print ("{:<22} {:<15} {:<15} {:<17} {:<20} {:<20}".format("Untapered (same vel.)", format(neededUntaperedWidth,".4f"), format(untaperedMass,".4f"), format(untaperedMaterialNeeded,".4f"), angularVelocity, linearVelocity))
  
  print ("{:<22} {:<15} {:<15} {:<17} {:<20} {:<20}".format("Untapered (same mass)", format(sameMassTaperedWidth,".4f"), format(taperedMass,".4f"), format(taperedMaterialNeeded,".4f"), format(sameMassTaperedAngularVelocity,".4f"), format(sameMassTaperedLinearVelocity,".4f")))
  
  print()
  
  print("Untapered, Same Velocity")
  print("Mass Saved by Tapered Ribbon: ", format(untaperedMass - taperedMass, ".4f"), "kg /", format((untaperedMass - taperedMass) / untaperedMass * 100, ".4f"), "%")
  print("Material Saved by Tapered Ribbon: ", format(untaperedMaterialNeeded - taperedMaterialNeeded, ".4f"), "m^3 /", format((untaperedMaterialNeeded - taperedMaterialNeeded) / untaperedMaterialNeeded * 100, ".4f"), "%")
  
  print()
  
  print("Untapered, Same Mass")
  print("Angular Velocity Improvement with Tapered Ribbon: ", format(angularVelocity - sameMassTaperedAngularVelocity, ".4f"), "rad/s /", format((angularVelocity - sameMassTaperedAngularVelocity) / sameMassTaperedAngularVelocity * 100, ".4f"), "%")
  print("Linear Velocity Improvement with Tapered Ribbon: ", format(linearVelocity - sameMassTaperedLinearVelocity, ".4f"), "km/s /", format((linearVelocity - sameMassTaperedLinearVelocity) / sameMassTaperedLinearVelocity * 100, ".4f"), "%")




  
#-----GRAPH-----
# values for the tapered curve
cap = ribbonLength / 2
step = cap * (-1)
x = []
while step <= cap:
  x.append(step)
  step = step + stepSize

step = step - stepSize
while step >= cap * (-1):
  x.append(step)
  step = step - stepSize


i = 0
y = []
while i <= len(outputArray) - 1:
  y.append(outputArray[i][2] / 2)
  i = i + 1

i = i - 1
y.append(outputArray[i][2] / 2)

while i >= 0:
  y.append(outputArray[i][2] / 2)
  i = i - 1

i = 0
while i <= len(outputArray) - 1:
  y.append(outputArray[i][2] / (-2))
  i = i + 1

i = i - 1
y.append(outputArray[i][2] / (-2))

while i >= 0:
  y.append(outputArray[i][2] / (-2))
  i = i - 1


#values for the untapered curves
x1 = [cap * (-1), cap, cap, cap * (-1)]
y1 = [neededUntaperedWidth / 2, neededUntaperedWidth / 2, neededUntaperedWidth * (-0.5), neededUntaperedWidth * (-0.5)]

x2 = [cap * (-1), cap, cap, cap * (-1)]
y2 = [sameMassTaperedWidth / 2, sameMassTaperedWidth / 2, sameMassTaperedWidth * (-0.5), sameMassTaperedWidth * (-0.5)]
  
# plotting the points 
#plt.plot(x1, y1, linewidth = 2, color = 'red', label = "Untapered Ribbon (Same Velocity)")
#plt.plot(x2, y2, linewidth = 2, color = 'blue', label = "Untapered Ribbon (Same Mass)")
#plt.plot(x, y, linewidth = 2, color = 'black', label = "Tapered Ribbon")
  
# setting x and y axis range
#plt.ylim(neededUntaperedWidth / 2 * (-1.1), neededUntaperedWidth / 2 * 1.1)
#plt.xlim(cap * (-1), cap)
  
#adding labels to the plot
#plt.legend()
#plt.xlabel('Distance from Center (m)')
#plt.ylabel('Ribbon Width Boundaries (m)')
#plt.title('Ribbon Taper Visualization')
#plt.show()
