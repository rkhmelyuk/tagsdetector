

def find(list, function):
    for each in list:
        if function(each):
            return each

    return None