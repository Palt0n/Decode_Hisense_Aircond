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
                list_values_x.append("8")
            else:
                raise ValueError("Value: {} doesn't match any conditions".format(value))
        return "".join(list_values_x)
    
    def get_list_pulse(self):
        list_pulse = []
        string_bit = self.get_binary()
        count_bit = 0
        for bit in string_bit:
            bit = string_bit[count_bit]
            count_bit += 1
            if bit == "0":
                pulse = Average_Y_for_X_1
            elif bit == "1":
                pulse = Average_Y_for_X_2
            elif bit == "8":
                pulse = Average_Y_for_X_8
            else:
                raise ValueError("Expected 0,1,8 not {} {}".format(bit, type(bit)))
            list_pulse.append(pulse)
        return list_pulse

    def get_binary_encoded(self):
        """
        Get pulse length encoded
        """
        binary_string = self.get_binary()
        binary_string = binary_string[1::2] # Get only even bits
        return binary_string
        # return self.get_binary()
    
    def is_ok(self):
        return len(self.get_binary_encoded()) == 170

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

    def generate_conf(self):
        """
        irsend SEND_ONCE MY_REMOTE MY_TEST
        """
        list_pulse = self.get_list_pulse()
        list_pulse = [9000, 4470] + list_pulse
        list_line_pulse = []
        for i in range(0, len(list_pulse), 6):
            sublist_pulse = list_pulse[i:i + 6]
            list_string_pulse = []
            for pulse in sublist_pulse:
                string_pulse = "{:9}".format(pulse)
                list_string_pulse.append(string_pulse)
            list_line_pulse.append("".join(list_string_pulse))
        string_line_pulse = "\n".join(list_line_pulse)
        template = """begin remote

   name  MY_REMOTE
   flags RAW_CODES
   eps            30
   aeps          100

  ptrail          0
  repeat     0     0
  gap    107325

       begin raw_codes

           name MY_TEST
{raw_code}

    end raw_codes
end remote""".format(raw_code=string_line_pulse)

        return template
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
    if raw.is_ok():
        print(raw.generate_conf())

