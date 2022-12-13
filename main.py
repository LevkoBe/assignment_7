import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)
parser.add_argument('-medals', nargs=2, required=True)
parser.add_argument('-output', '--output', type=argparse.FileType('w', encoding='UTF-8'))
parser.add_argument('-total', type=str)
parser.add_argument('-overall', nargs="*")
parser.add_argument('-interactive', action='store_true')

args = parser.parse_args()

def value_of_medals(line,gold,silver,bronze):

    if 'Gold\n' in line:
        gold += 1
    elif 'Silver\n' in line:
        silver += 1
    elif 'Bronze\n' in line:
        bronze += 1   

    return gold, silver, bronze 


def interactive_mode():
    current_country = input("Enter country: ")
    while current_country:

        with open(args.infile, 'r') as current_file:
            current_line = current_file.readline()

            years = {}
            first_time = 3000
            place = None

            while current_line:
                current_line = current_file.readline()
                current_data = current_line.split('\t')
                if current_country in current_data:
                    current_year = current_data[9]
                    if current_year not in years:
                        years[current_year] = [0, 0, 0, 0]
                    if current_data[-1] != 'NA\n':
                        years[current_year][3] += 1
                        
                        years[current_year][0],years[current_year][1],years[current_year][2] \
                        = value_of_medals(current_data,years[current_year][0],years[current_year][1],years[current_year][2])   

                    if int(current_year) < first_time:
                        first_time = int(current_year)
                        place = current_data[-4]

            all_years = [x for x in years.keys()]
            all_medals = [x[3] for x in years.values()]
            the_best = all_medals.index(max(all_medals))
            the_worst = all_medals.index(min(all_medals))

            print(f"The first participation in Olympiad was in {first_time} year, in {place}.")
            print(f"The most successful participation was in {all_years[the_best]} with {all_medals[the_best]} medals.")
            print(f"The least successful participation was in {all_years[the_worst]} with {all_medals[the_worst]} medals.")

            for the_year in years:
                print(f"In {the_year} was won {years[the_year][0]} gold, "
                      f"{years[the_year][1]} silver and {years[the_year][2]} bronze medals.")
        current_country = input("Enter country: ")


with open(args.infile, 'r') as file:
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

            countries[data[6]][0],countries[data[6]][1],countries[data[6]][2] \
            =value_of_medals(data,countries[data[6]][0],countries[data[6]][1],countries[data[6]][2])

        if args.medals[0] in data and args.medals[1] in data:
            if amount_of_people < 10 and ('Gold\n' in data or 'Silver\n' in data or 'Bronze\n' in data):
                store += f'{data[1]}, {data[-1]}'
                amount_of_people += 1

            amount_of_gold, amount_of_silver, amount_of_bronze \
            =value_of_medals(data,amount_of_gold, amount_of_silver, amount_of_bronze)           

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

if args.interactive:
    interactive_mode()
# python main.py "oa.tsv" -medals UKR 2004 -total 2000 -overall USA UKR -output "new" -interactive
