import pandas as pd


def XScoulmtranging(data, rows):
    yes = 0
    no = 0
    for i in rows:
        if data[i][-1] == "yes":
            yes += 1
        else:
            no += 1
    ansn = no / (yes + no)
    ansy = yes / (yes + no)
    return ansy, ansn, yes, no


def NaiveBayes(data, rows, columns, X):
    ansy, ansn, yes, no = XScoulmtranging(data, rows)
    mulyes = 1
    mulno = 1
    list_count_yes = []
    list_count_no = []
    count0y = 0
    count0n = 0
    for j in columns:
        countyes = 0
        countno = 0
        key = X[list(X)[j]]
        for i in rows:
            if data[i][j] == key:
                if data[i][-1] == "yes":
                    countyes += 1
                else:
                    countno += 1
        list_count_yes.append(countyes)
        list_count_no.append(countno)
    for i in range(0, len(list_count_yes)):
        if list_count_yes[i] == 0:
            count0y += 1
    for i in range(0, len(list_count_no)):
        if list_count_no[i] == 0:
            count0n += 1
    for i in range(0, len(list_count_yes)):
        if count0y == 0:
            mulyes *= list_count_yes[i] / yes
        else:
            mulyes *= (1 + list_count_yes[i])/(yes + len(X))
    for i in range(0, len(list_count_no)):
        if count0n == 0:
            mulno *= list_count_no[i] / no
        else:
            mulno *= (1 + list_count_no[i])/(no + len(X))
    p_yes = mulyes * ansy
    p_no = mulno * ansn
    print("Người X có khả năng mua máy tính không?")
    if p_yes > p_no:
        print("CÓ")
    else:
        print("KHÔNG")


if __name__ == '__main__':
    df = pd.read_csv('buylaptop.csv')
    data = df.iloc[:, 1:].values
    attribute_list = ['Tuoi', 'Thu nhap', 'Sinh vien', 'Danh gia tin dung']
    X = {'Tuoi': 'youth', 'Thu nhap': 'medium', 'Sinh vien': 'yes', 'Danh gia tin dung': 'fair'}
    rows = [i for i in range(0, 14)]
    columns = [i for i in range(0, 4)]
    NaiveBayes(data, rows, columns, X)
