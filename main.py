import argparse  
parser = argparse.ArgumentParser() 
parser.add_argument('infile', type=argparse.FileType('r')) 
parser.add_argument('-medals', dest='medals', nargs=2, required=True) 
parser.add_argument('-output', '--output', type=argparse.FileType('w', encoding='UTF-8'))  

args = parser.parse_args() 
print(args.medals)    

with args.infile as file:   
    next_line = file.readline()   
    store = [next_line]   
    while next_line:       
        # do stuff with line       
        next_line = file.readline()       
        store.append(next_line)  
        
if args.output is not None:  
    args.output.writelines(f'{store[0]}\n')
