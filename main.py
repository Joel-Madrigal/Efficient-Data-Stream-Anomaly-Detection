import random

def data_stream(size, base, alternate):
    data_holder = []
    alter = True
    for i in range(size + 1):
        curr_num = base
        if alter == True:
            i += curr_num + alternate
        else:
            i -= curr_num + alternate

        alter = False
        data_holder.append(i)

    return data_holder
print(data_stream(1000, 500, 10))