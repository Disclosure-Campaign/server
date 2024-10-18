# conda list -e > requirements.txt

input_file = open('requirements.txt', mode='r')
output_file = open('fixed_requirements.txt', 'w')


for line in input_file:
    line = line.replace('\n', '')
    requirement = line.split('==py')[0]
    requirement = requirement.split('==h')[0]

    output_file.write(requirement + '\n')

