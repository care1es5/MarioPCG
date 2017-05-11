import os
for filename in os.listdir('./data_set'):
    with open('./data_set/' + filename, 'r') as r:
        lines = r.readlines()

    second_start_tick = None
    for i in range(len(lines)):
        if len(lines[i].split('\t')[1]) > 6 and i > 0 and not second_start_tick:
            second_start_tick = i

    print "Index of final start tick in {0}: {1}".format(filename, second_start_tick)

    if second_start_tick:
        lines = lines[:second_start_tick]

    last_line = lines[-1]
    last_similarity = len(lines)-1
    for i in range(len(lines)-1, 0, -1):
        if "\t".join(lines[i].split('\t')[4:]) == "\t".join(last_line.split('\t')[4:]):
            last_similarity = i
        else:
            break

    print "Index of last similarity in {0}: {1}".format(filename, last_similarity)

    with open('./data_set_processed/' + filename, 'w') as w:
        w.write(''.join(lines[:last_similarity]))

    print "Writing processed data to ./data_set_processed/{0}".format(filename)

    print "============================================="


