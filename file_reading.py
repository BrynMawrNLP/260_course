import csv
import numpy as np

# three ways to read a file

# 1) read line by line
def line_by_line():
    fb_file = open("data/facebook_users.csv", 'r') # 'r' for read mode
    for line in fb_file:
        tokens = line.split(",") # split on comma
        year = int(tokens[0])
        num_users = int(tokens[1])
        print(year, num_users)
    fb_file.close()
    print("\n")

# 2) csv reader
def csv_reader():
    with open("data/facebook_users.csv", 'r') as fb_file:
        reader = csv.reader(fb_file)
        for line in reader:
            print(line)
    print("\n")

# 3) load into numpy array
def numpy_array():
    data = np.loadtxt("data/facebook_users.csv", dtype=int, delimiter=",")
    print(data)

def main():
    line_by_line()
    #csv_reader()
    #numpy_array()

if __name__ == "__main__":
    main()
