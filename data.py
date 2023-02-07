import util


def get_data():
    with open("data.txt", "r+") as f:
        read = f.read()
        f.truncate(0)
        f.close()
        x = int(read)
        file = open("data.txt", "a")
        file.write(str(x + 1))
        file.close()
        return x


def getData_without_increase():
    with open("data.txt", "r+") as f:
        read = f.read()
        f.truncate(0)
        f.close()
        x = int(read)
        file = open("data.txt", "a")
        file.write(str(x))
        file.close()
        return x

def generate_name():
    with open("name.txt", "r+") as f:
        f.truncate(0)
        f.close()
        file = open("name.txt", "a")
        x = util.Upper_Lower_string(10)
        file.write(x)
        file.close()
        return x

def setup_name():
    with open("data.txt", "r+") as f:
        read = f.read()
        f.truncate(0)
        f.close()
        x = int(read)
        file = open("data.txt", "a")
        file.write(str(x + 1))
        file.close()
        return x


def return_normal():
    open('data.txt', 'w').close()
    file = open("data.txt", "a")
    file.write(str(2))
    file.close()
