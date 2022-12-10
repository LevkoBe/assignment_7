import argparse  
parser = argparse.ArgumentParser() 
parser.add_argument('infile', type=argparse.FileType('r')) 
parser.add_argument('-medals', dest='medals', nargs=2, required=True) 
parser.add_argument('-output', '--output', type=argparse.FileType('w', encoding='UTF-8'))  

args = parser.parse_args() 
print(args.medals)    

with args.infile as file:   
    next_line = file.readline()   
    store = []   
    while next_line:       
        # do stuff with line       
        next_line = file.readline()
        data = [next_line.split('\t')]  

        amount_of_people = 0

        if args.medals[0] in data and args.medals[1] in data:
            if amount_of_people < 10 and ('Gold\n' in data or 'Silver\n' in data or 'Bronze\n' in data):
                store += f'{data[1]}, {data[-1]}\n'
                amount_of_people += 1
        


if args.output is not None:  
    args.output.writelines(f'{store[0]}\n')

print(store)