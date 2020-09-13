import copy
import pandas as pd
import math


class Node:
    def __init__(self):
        self.value = "Không biết"
        self.decision = None
        self.childs = None


def MaxcountYN(data, rows):
    maxcount = 0
    value = -1
    myset = {}
    for i in rows:
        key = data[i][-1]
        if key in myset:
            myset[key] += 1
        elif key not in myset:
            myset[key] = 1
    for i in myset:
        if maxcount < myset[i]:
            maxcount = myset[i]
            value = i
    return value


def findEntropy(data, rows):
    yes = 0
    no = 0
    ans = -1
    entropy = 0
    index = -1
    for i in rows:
        if data[i][index] == "yes":
            yes += 1
        else:
            no += 1
    x = yes / (yes + no)
    y = no / (yes + no)
    if x != 0 and y != 0:
        entropy = -x * math.log2(x) - y * math.log2(y)
    elif x == 1:
        ans = 1
    elif y == 1:
        ans = 0
    return entropy, ans


def findMaxGain(data, rows, columns):
    maxgain = 0
    indexclm = -1
    entropy, ans = findEntropy(data, rows)
    if entropy == 0:
        return maxgain, indexclm, ans
    for j in columns:
        myset = {}
        for i in rows:
            key = data[i][j]
            if key in myset:
                myset[key] += 1
            else:
                myset[key] = 1
        gain = entropy
        for key in myset:
            yes = 0
            no = 0
            for i in rows:
                if data[i][j] == key:
                    if data[i][-1] == "yes":
                        yes += 1
                    else:
                        no += 1
            x = yes / (yes + no)
            y = no / (yes + no)
            if x != 0 and y != 0:
                gain += (myset[key] * (x * math.log2(x) + y * math.log2(y))) / (len(rows))
            elif x == 0:
                ans = 1
            elif y == 0:
                ans = 0
        if maxgain < gain:
            maxgain = gain
            indexclm = j
    return maxgain, indexclm, ans


def buildtree(data, rows, columns, attribute_list):
    maxgain, indexclm, ans = findMaxGain(data, rows, columns)
    root = Node()
    root.childs = []
    #### Cùng thuộc 1 nhãn C => trả về cây có lá là N và có giá trị là nhãn C
    if maxgain == 0:
        if ans == 1:
            root.value = "YES"
        elif ans == 0:
            root.value = "NO"
        return root
    #### Nếu attribute_list rỗng thì trả về cây có lá là N cà có giá trị là nhãn xuất hiện nhiều nhất
    if attribute_list == []:
        root.value = MaxcountYN(data, rows)
        return root
    #### Trường hợp còn lại
    root.value = attribute_list[indexclm]
    myset = {}
    for i in rows:
        key = data[i][indexclm]
        if key in myset:
            myset[key] += 1
        else:
            myset[key] = 1
    newcoloums = copy.deepcopy(columns)
    newcoloums.remove(indexclm)
    for key in myset:
        newrows = []
        for i in rows:
            if key == data[i][indexclm]:
                newrows.append(i)
        newtree = buildtree(data, newrows, newcoloums, attribute_list)
        newtree.decision = key
        root.childs.append(newtree)
    return root


def printreverse(root):
    print("[Decision]: " + root.decision)
    print("[Value of decision " + root.decision+  "]: " + root.value)
    if len(root.childs) > 0:
        for i in range(0, len(root.childs)):
            printreverse(root.childs[i])


if __name__ == '__main__':
    df = pd.read_csv('buylaptop.csv')
    data = df.iloc[:, 1:].values
    attribute_list = ['Tuoi', 'Thu nhap', 'Sinh vien', 'Danh gia tin dung']
    rows = [i for i in range(0, 14)]
    columns = [i for i in range(0, 4)]
    root = buildtree(data, rows, columns, attribute_list)
    root.decision = "ROOT"
    printreverse(root)
