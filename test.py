import numpy as np

titles01 = ['Paul Garner HAMADI - Freelance Python Developer - Depop | LinkedIn',
            'Rob Young - Python Developer',
            'Paul Garner - Freelance Python Developer - Depop | LinkedIn']
name = []
job = []
company = []
for i in titles01:
    slots = i.split(' - ')
    print(len(slots))
    if len(slots) == 3:
        name.append(i.split('-', 10)[0])
        job.append(i.split('-', 10)[1])
        company.append(i.split('-', 10)[2])
    elif len(slots) != 3:
        name.append(i.split('-', 10)[0])
        job.append(i.split('-', 10)[1])
        company.append(None)

print(name)
print(job)
print(company)
