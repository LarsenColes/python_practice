
def get_coins(amount):
    quarters = 0
    while (quarters + 1) * 25 <= amount:
        quarters += 1
    next_coins =  get_dimes(amount - (quarters * 25))
    data = {"quarters": quarters}
    data.update(next_coins)
    return data

def get_dimes(amount):
    dimes = 0
    while (dimes + 1) * 10 <= amount:
        dimes += 1

    next_coins = get_nickels(amount - (dimes * 10))
    data = {"dimes": dimes}
    data.update(next_coins)
    return data


def get_nickels(amount):
    nickels = 0
    while (nickels + 1) * 5 <= amount:
        nickels += 1

    next_coins = get_pennies(amount - (nickels * 5))
    data = {"nickels": nickels}
    data.update(next_coins)
    return data


def get_pennies(amount):
    pennies = 0
    while pennies + 1 <= amount:
        pennies += 1
    data = {"pennies": pennies}
    return data

def display_graph(data):
    #Get the maximum column height
    max_height = 0

    for key in data:
       if data[key] > max_height:
           max_height = data[key]

    for i in range(max_height):
        if i == 0:
            print("+---------+")
        display = ""
        for key in data:
            if i >= max_height - (data[key]):
                display = display + " ■"
            else:
                display = display + "  "

        line = "|" + display + " |"
        print(line)
    print("+---------+")
    print("  Q D N P  ")


def get_distribution(data):
    #Data must be converted to total coins
    distribution = {}
    for key in data:
        if data[key] in distribution:
            distribution[data[key]] += 1
        else:
            distribution[data[key]] = 1

    return distribution


def get_dataset(number):
    data = {}
    for i in range(number):
        data[i] = get_coins(i)
    return data

def dynamic_graph(data):
    #Data must be converted to total coins
    max_height = 0
    max_width = 0
    label_line = ""
    for key in data:
        if data[key] > max_height:
            max_height = data[key]
        label_line += f" {str(key).title()}"
    max_width = len(label_line)



    for i in range(max_height):
        if i == 0:
            print(f"{' '*6}+{ '-' * max_width}-+")
        display = ""
        for key in data:
            if i >= max_height - (data[key]):
                display = display + f"{' ' * len(str(key))}■"
            else:
                display = display + f"{' ' * len(str(key))} "

        line = f"{max_height - i }{' ' * (6 - len(str(max_height - i)))}|{display} |"
        print(line)
    print(f"{' '*6}+{ '-' * max_width}-+")
    print(f"{' '*6} {label_line}  ")


def convert_to_total(data):
    for key in data:
        total_coins = 0
        for coin in data[key]:
            total_coins += data[key][coin]
        data[key] = total_coins

    return data

def max_coins(amount):
    most_coins_count = 0
    most_coins_number = 0
    for i in range(amount):
        total_coins = 0
        result = get_coins(i)
        for key in result:
           total_coins += result[key]
        if total_coins > most_coins_count:
            most_coins_number = i
            most_coins_count = total_coins

    print(most_coins_number)
    print(most_coins_count)

number = int(input("What number do you want to check? \n"))
dynamic_graph(get_distribution(convert_to_total(get_dataset(number))))
dynamic_graph(convert_to_total(get_dataset(number)))
dynamic_graph(get_coins(number))