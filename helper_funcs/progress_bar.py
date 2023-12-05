from tqdm import tqdm

def create_tqdm_progress_bar(list):
    global tqdm_object
    global message

    symbol_list = list
    tqdm_object = tqdm(symbol_list, colour='green')

    if tqdm_object.total < 500:
        message = "Calling API for {}"
        tqdm_object.bar_format = '{l_bar}{bar:50}{r_bar}{bar:-10b}'
    else:
        message = "Processing contracts"
        description = message.ljust(35,'.')
        tqdm_object.set_description(description)
        tqdm_object.bar_format = '{l_bar}{bar:50}{r_bar}{bar:-10b}'
    return tqdm_object

def update_tqdm_progress_bar(symbol):
    description = message.format(symbol).ljust(35,'.')
    tqdm_object.set_description(description)

def main():
    message = "Calling API for {}"
    description = message.format("AAPL")
    description = description.ljust(30,'.')
    print(description)

if __name__ == "__main__":
    main()