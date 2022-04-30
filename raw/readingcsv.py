import csv

kategori = "difabel"
list_link = []
with open(f"link_{kategori}.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            print(row[2])
            list_link.append(row[2])
            line_count += 1
    print(f'Processed {line_count} lines.')
    print(len(list_link))
    print(list_link[0])
    print(list_link[2])
