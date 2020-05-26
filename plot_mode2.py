"""
Used to obtain the values (used in parse_mode2.py):
Average_Y_for_X_1 = 573
Average_Y_for_X_2 = 1620
Average_Y_for_X_8 = 7900

By fitting the values to a linear equation.

source env/Scripts/activate
"""
import matplotlib.pyplot as plt 
import numpy as np
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()
print(args.path)

assert os.path.isfile(args.path), "Path: {} is not a valid path"

def strip_line(line):
    if line == "":
        return None
    else:
        return line.strip()

def get_r2_numpy(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    r_squared = 1 - (sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
    return r_squared

class ClassMode2Raw:
    def __init__(self, head, body):
        self.head = head
        self.body = body
    
    def get_values(self):
        list_values = self.body
        list_values = list_values[2:]
        list_values = list_values[:-1]
        if "-" in list_values[-1]:
            list_values = list_values[:-1]
        list_values_int = []
        for value in list_values:
            list_values_int.append(int(value))
        return list_values_int
    
    def __str__(self):
        return "{} [ {} ]".format(self.head, ", ".join(self.body))
    
    @classmethod
    def from_raw(cls, line_head, list_line_body):
        line_head_split = line_head.split("-")
        assert len(line_head_split) in [1,2]
        head = line_head_split[0]
        list_values = []
        for line_body in list_line_body:
            line_body_split = line_body.split(" ")
            for value in line_body_split:
                if value != "":
                    list_values.append(value)
        body = list_values
        return cls(head, body)

list_raw = []
with open(args.path) as fh:
    while True:
        line = strip_line(fh.readline())
        line_head = line
        if line is None:
            break
        line = strip_line(fh.readline())
        assert line == ""
        list_line_body = []
        while True:
            line = strip_line(fh.readline())
            if line is None or line == "":
                list_raw.append(ClassMode2Raw.from_raw(line_head, list_line_body))
                break
            else:
                list_line_body.append(line)
list_values = []
for raw in list_raw:
    list_values.extend(raw.get_values())

# frequencies 
list_values_y = sorted(list_values)
list_values_x = []
for value in list_values_y:
    if value < 1000:
        list_values_x.append(1)
    elif value < 2000:
        list_values_x.append(2)
    elif value > 7000 and value < 8000:
        # 7 => R^2: 0.9878334119285562
        # 8 => R^2: 0.9924577962150835
        # 9 => R^2: 0.9902343396521045
        list_values_x.append(8)
    else:
        raise ValueError("Shouldn't come here")
print("MAX: {}".format(max(list_values_y)))
# setting the ranges and no. of intervals 
list_values_y = np.array(list_values_y)
list_values_x = np.array(list_values_x)

m, b = np.polyfit(list_values_x, list_values_y, 1)
list_values_y_predicted = m*list_values_x + b
print("Linear Equation: {} x + {}".format(m, b))
print("R square: {}".format(get_r2_numpy(list_values_y, list_values_y_predicted)))
print("X = 1: Y = {}".format(int(m*1 + b)))
print("X = 2: Y = {}".format(int(m*2 + b)))
print("X = 8: Y = {}".format(int(m*8 + b)))
# plotting a histogram 
# plt.hist(list_values_y, bins=50)
plt.plot(list_values_x, list_values_y_predicted)
plt.scatter(list_values_x, list_values_y)

# x-axis label 
plt.xlabel('age') 
# frequency label 
plt.ylabel('No. of people') 
# plot title 
plt.title('My histogram') 
  
# function to show the plot 
plt.show() 