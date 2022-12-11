import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('-medals', nargs=2, required=True)
parser.add_argument('-output', '--output', type=argparse.FileType('w', encoding='UTF-8'))
parser.add_argument('-total', type=str)
parser.add_argument('-overall', nargs="*")

args = parser.parse_args()

with args.infile as file:
    next_line = file.readline()
    store = ''

    amount_of_gold = 0
    amount_of_silver = 0
    amount_of_bronze = 0

    amount_of_people = 0

    countries = {}
    if args.overall:
        o_countries = [{} for x in args.overall]

    while next_line:
        next_line = file.readline()
        data = next_line.split('\t')

        if args.overall and data[-1] != 'NA\n':
            for i, country in enumerate(args.overall):
                if country in data:
                    if data[9] not in o_countries[i]:
                        o_countries[i][data[9]] = 1
                    else:
                        o_countries[i][data[9]] += 1

        if args.total and args.total in data and data[-1] != 'NA\n':
            if data[6] not in countries:
                countries[data[6]] = [0, 0, 0]

            if 'Gold\n' in data:
                countries[data[6]][0] += 1
            elif 'Silver\n' in data:
                countries[data[6]][1] += 1
            elif 'Bronze\n' in data:
                countries[data[6]][2] += 1

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

all_countries = f'In {args.total} such countries won medals:\n'
for country in countries:
    all_countries += f'{country} - {countries[country][0]} - {countries[country][1]} - {countries[country][2]}\n'


all_text = f'{store}\n{args.medals[0]}, year {args.medals[1]}.\n\n'\
               f'Gold: {amount_of_gold};\nsilver: {amount_of_silver};\nbronze: {amount_of_bronze}.'
if args.total:
    all_text += f'\n\n{all_countries}'
if args.overall:
    overall_countries = ''
    for i in range(len(o_countries)):
        values = [int(o_countries[i][x]) for x in o_countries[i]]
        numbers_of_medals = [int(x) for x in o_countries[i].values()]
        max_value = max(numbers_of_medals)
        years_of_medals = [x for x in o_countries[i].keys()]
        year = years_of_medals[numbers_of_medals.index(max_value)]
        overall_countries += f'{args.overall[i]} - year {year} - {max_value} medals\n'

    all_text += f'\n\n{overall_countries}'


if args.output is not None:
    args.output.writelines(all_text)

print(all_text)
# python main.py "oa.tsv" -medals UKR 2004 -total 2000 -overall USA UKR -output "new"
