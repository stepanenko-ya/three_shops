
def writer(result_list):
    with open('result_data.csv', 'a+') as file:
        file.write(result_list)


def main():
    dirty_file = open("allegro.csv").readlines()
    title = open("poland items.csv").readlines()
    writer("".join(title[2]))
    for el in dirty_file:
        lst = el.split("|")
        lst[3] = '/'.join(lst[3:6]).replace('"', '')
        lst[4] = ""

        del lst[5:6]
        print(lst)
        y = "|".join(lst)
        writer(y)
main()



