
def exists(data, group):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if(str(data[i][j]).startswith(group)):
                return i, j
    return False