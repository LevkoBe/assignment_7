import argparse

parser = argparse.ArgumentParser() 
parser.add_argument('infile', type=argparse.FileType('r')) 
parser.add_argument('-medals', dest='medals', nargs=2, required=True) 
parser.add_argument('-output', '--output', type=argparse.FileType('w', encoding='UTF-8'))  

args = parser.parse_args() 
print(args.medals)    



with args.infile as file:   
    next_line = file.readline()   
    store = ''
     
    amount_of_gold = 0
    amount_of_silver =0
    amount_of_bronze = 0

    amount_of_people = 0
    

    while next_line:       
        # do stuff with line       
        next_line = file.readline()
        data = next_line.split('\t')
        
        
        if args.medals[0] in data and args.medals[1] in data:
            if amount_of_people < 10 and ('Gold\n' in data or 'Silver\n' in data or 'Bronze\n' in data):
                store += f'{data[1]}, {data[-1]}'
                amount_of_people += 1

            if 'Gold\n' in data:
                amount_of_gold += 1
            elif 'Silver\n' in data:
                amount_of_silver += 1                       
            elif 'Bronze\n' in data:
                amount_of_bronze += 1
                               
        
if args.output is not None:  
    args.output.writelines(f'{store}{amount_of_gold}\n{amount_of_silver}\n{amount_of_bronze}\n')
print(store)

print (amount_of_gold , amount_of_silver , amount_of_bronze)
