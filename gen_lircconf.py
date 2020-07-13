"""
Returns binary code from parsing the LIRC mode2 output

source env/Scripts/activate
python parse_mode2.py Hisense_Aircond_Power.mode2.example
"""
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()
print(args.path)

assert os.path.isfile(args.path), "Path: {} is not a valid path"

Average_Y_for_X_1 = 573
Average_Y_for_X_2 = 1620
Average_Y_for_X_8 = 7900

def strip_line(line):
    if line == "":
        return None
    else:
        return line.strip()

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
    
    def get_binary(self):
        list_values_x = []
        for value in self.get_values():
            if (value > Average_Y_for_X_1 - 250) and (value < Average_Y_for_X_1 + 250):
                list_values_x.append("0")
            elif (value > Average_Y_for_X_2 - 150) and (value < Average_Y_for_X_2 + 150):
                list_values_x.append("1")
            elif (value > Average_Y_for_X_8 - 100) and (value < Average_Y_for_X_8 + 100):
                list_values_x.append("X")
            else:
                raise ValueError("Value: {} doesn't match any conditions".format(value))
        return "".join(list_values_x)

    def get_binary_encoded(self):
        """
        Get pulse length encoded
        """
        binary_string = self.get_binary()
        binary_string = binary_string[1::2] # Get only even bits
        return binary_string
        # return self.get_binary()
    
    def is_ok(self):
        return len(self.get_binary_encoded() == 170)

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
        assert line == "", "Expected empty line at: {}".format(line)
        list_line_body = []
        while True:
            line = strip_line(fh.readline())
            if line is None or line == "":
                list_raw.append(ClassMode2Raw.from_raw(line_head, list_line_body))
                break
            elif "-space" in line and len(list_line_body) == 0:
                print("Overwriting head: {} with {}".format(line_head, line))
                line_head = line
                line = strip_line(fh.readline())
                assert line == "", "Expected empty line at: {}".format(line)
                line = strip_line(fh.readline())
            else:
                list_line_body.append(line)
list_values = []
for raw in list_raw:
    binary = raw.get_binary()
    print("{} = {}".format(raw.head, raw.get_binary_encoded()))

