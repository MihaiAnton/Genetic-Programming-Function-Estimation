
def getData(fileName):
    file = open(fileName, "r")

    line = file.readline()
    X = []
    Y = []

    while line:

        parts = line.split(",")
        parts = [float(part) for part in parts[:]]
        X.append(parts[:-1])
        Y.append(parts[-1])

        line = file.readline()


    file.close()

    return X,Y
