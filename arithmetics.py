# Calculate the circumference of a circle given its radius
import math
# radius = float(input("Radius of circle in cm: "))
# C = math.ceil(2 * math.pi * radius)

# Calculate the area of a circle given the formula A=C^2/4pi
# A = math.ceil((pow(C,2))/(4*math.pi))

# Using the radius calculate the area of circule
# A = math.ceil(math.pi * pow(radius, 2))

# print(f"The circumference of the circle is {C}cm")
# print(f"The area of the cirtcle is {A}cm^2")

#Find the hypoptenuse of a triangle using c = sqrt a^2 + b^2'
a = int(input("Enter the length of the triangle (in cm): "))
b = int(input("Enter the width of the triangle (in cm): "))

c = math.sqrt(pow(a, 2) + pow(b, 2))
print(f"The length of the hypotenuse is {c}cm.")