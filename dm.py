import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


def draw_pic(row_data, name):
    plt.figure(figsize=(20, 20))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文无法显示的问题
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.hist(row_data, bins=5)
    plt.xticks(rotation=90)  # bins表示分为5条直方，可以根据需求修改
    plt.savefig('./figs/{}.jpg'.format(name))
    plt.close('all')


def fiveNumber(nums):
    # 五数概括 Minimum（最小值）、Q1、Median（中位数、）、Q3、Maximum（最大值）
    Minimum = min(nums)
    Maximum = max(nums)
    Q1 = np.percentile(nums, 25)
    Median = np.median(nums)
    Q3 = np.percentile(nums, 75)

    IQR = Q3 - Q1

    return [Minimum, Q1, Median, Q3, Maximum]


def draw_num(row_data, name):
    plt.figure(figsize=(20, 20))
    df = pd.DataFrame(row_data)

    df.plot.box(title=" ")
    plt.grid(linestyle="--", alpha=0.3)
    plt.savefig('./figs/{}.jpg'.format(name))
    plt.close('all')


# 原始数据统计
def row_data_deal(data):
    for index, row in data.iteritems():
        counter = pd.value_counts(row)

        row = list(row)
        flag = 'none'
        for i in range(len(row)):
            if isinstance(row[i], str):
                flag = 'str'
                break
            elif np.isnan(row[i]):
                continue
            else:
                flag = 'int'

        if flag == 'str':
            for i in range(len(row)):
                if row[i] not in list(counter[:20].keys()):
                    row[i] = 'OTHERS'

            draw_pic(list(row), index + 'row')
        elif flag == 'int':
            nan_num = 0
            line = []
            for i in row:
                if np.isnan(i):
                    nan_num += 1
                else:
                    line.append(i)
            print('nan number = ', nan_num)
            draw_num(line, index + 'row')
            five = fiveNumber(line)
            print(five)

        print(flag)


# 缺失值剔除
def one(data):
    nan_row_idx = []
    for index, row in data.iterrows():
        row = list(row)
        # print(np.isnan(row[0]))
        # print(row)
        for i in row:
            if isinstance(i, str):
                continue
            if np.isnan(i):
                nan_row_idx.append(index)
                break
        # break
    print(nan_row_idx)
    data.drop(index=nan_row_idx, inplace=True)

    for index, row in data.iteritems():
        counter = pd.value_counts(row)

        row = list(row)
        flag = 'none'
        for i in range(len(row)):
            if isinstance(row[i], str):
                flag = 'str'
                break
            elif np.isnan(row[i]):
                continue
            else:
                flag = 'int'

        if flag == 'str':
            line = []
            for i in range(len(row)):
                if row[i] not in list(counter[:20].keys()):
                    row[i] = 'OTHERS'
                line.append(row[i])
            draw_pic(list(row), index + '1')
        elif flag == 'int':
            nan_num = 0
            line = []
            for i in row:
                if np.isnan(i):
                    nan_num += 1
                else:
                    line.append(i)
            print('nan number = ', nan_num)
            draw_num(line, index + '1')
            five = fiveNumber(line)
            print(five)


# 用高频数据补充
def two(data):
    for index, row in data.iteritems():
        counter = pd.value_counts(row)

        row = list(row)
        flag = 'none'
        for i in range(len(row)):
            if isinstance(row[i], str):
                flag = 'str'
                break
            elif np.isnan(row[i]):
                continue
            else:
                flag = 'int'

        if flag == 'str':
            line = []
            for i in range(len(row)):
                if not isinstance(row[i], str) and np.isnan(row[i]):
                    if not np.isnan(list(counter[:20].keys())[0]):
                        row[i] = list(counter[:20].keys())[0]
                    else:
                        row[i] = list(counter[:20].keys())[1]

                if row[i] not in list(counter[:20].keys()):
                    row[i] = 'OTHERS'
                line.append(row[i])
            draw_pic(list(row), index + '2')
        elif flag == 'int':
            nan_num = 0
            line = []
            for i in row:
                if np.isnan(i):
                    if not np.isnan(list(counter[:2].keys())[0]):
                        i = list(counter[:2].keys())[0]
                    else:
                        i = list(counter[:2].keys())[1]
                    line.append(i)
                else:
                    line.append(i)
            print('nan number = ', nan_num)
            draw_num(line, index + '2')
            five = fiveNumber(line)
            print(five)


def find_lcsubstr(s1, s2):
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]  # 生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax = 0  # 最长匹配的长度
    p = 0  # 最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
    return mmax  # 返回最长子串及其长度


def three(data):
    names = data.columns.values
    for index, row in data.iterrows():
        row = list(row)

        for i in range(len(row)):
            if names[i] != 'Area Id':
                continue
            if isinstance(row[i], str):
                continue
            if np.isnan(row[i]):
                replace_idx, max_len = 0, -10
                for delta in range(-15, 16):
                    if delta == 0 or index + delta < 0 or index + delta >= data.shape[0]:
                        continue
                    if not isinstance(list(data.iloc[index + delta])[i - 1], str) and np.isnan(
                            list(data.iloc[index + delta])[i - 1]):
                        continue
                    if not isinstance(list(data.iloc[index + delta])[i], str) and np.isnan(
                            list(data.iloc[index + delta])[i]):
                        continue

                    list_lenth = find_lcsubstr(row[i - 1], list(data.iloc[index + delta])[i - 1])
                    if list_lenth == max_len and abs(delta) < abs(replace_idx):
                        replace_idx = delta
                    if list_lenth > max_len:
                        replace_idx = delta
                        max_len = list_lenth
                data.loc[index, names[i]] = list(data.iloc[index + replace_idx])[i]

        # break
    for index, row in data.iteritems():
        counter = pd.value_counts(row)
        if index != 'Area Id':
            continue

        row = list(row)
        flag = 'none'
        for i in range(len(row)):
            if isinstance(row[i], str):
                flag = 'str'
                break
            elif np.isnan(row[i]):
                continue
            else:
                flag = 'int'

        if flag == 'str':
            line = []
            for i in range(len(row)):
                if row[i] not in list(counter[:20].keys()):
                    row[i] = 'OTHERS'
                line.append(row[i])
            draw_pic(list(row), index + '3')
        elif flag == 'int':
            nan_num = 0
            line = []
            for i in row:
                if np.isnan(i):
                    nan_num += 1
                else:
                    line.append(i)
            print('nan number = ', nan_num)
            draw_num(line, index + '3')
            five = fiveNumber(line)
            print(five)


def cal_lenth(l1, l2):
    num = 0
    for i in range(len(l1)):
        if not isinstance(l1[i], str) and np.isnan(l1[i]):
            continue
        if not isinstance(l2[i], str) and np.isnan(l2[i]):
            continue
        if l1[i] == l2[i]:
            num += 1
    return num


def four(data):
    print(data.columns.values)
    names = data.columns.values
    for index, row in data.iterrows():
        row = list(row)
        for i in range(len(row)):
            if isinstance(row[i], str):
                continue
            if np.isnan(row[i]):
                replace_idx, max_len = 0, -10
                for delta in range(-15, 16):
                    if delta == 0 or index + delta < 0 or index + delta >= data.shape[0]:
                        continue
                    if not isinstance(list(data.iloc[index + delta])[i], str) and np.isnan(
                            list(data.iloc[index + delta])[i]):
                        continue

                    list_lenth = cal_lenth(row, list(data.iloc[index + delta]))
                    if list_lenth == max_len and abs(delta) < abs(replace_idx):
                        replace_idx = delta
                    if list_lenth > max_len:
                        replace_idx = delta
                        max_len = list_lenth
                data.loc[index, names[i]] = list(data.iloc[index + replace_idx])[i]

    for index, row in data.iteritems():
        counter = pd.value_counts(row)

        row = list(row)
        flag = 'none'
        for i in range(len(row)):
            if isinstance(row[i], str):
                flag = 'str'
                break
            elif np.isnan(row[i]):
                continue
            else:
                flag = 'int'

        if flag == 'str':
            line = []
            for i in range(len(row)):
                if row[i] not in list(counter[:20].keys()):
                    row[i] = 'OTHERS'
                line.append(row[i])
            draw_pic(list(row), index + '4')
        elif flag == 'int':
            nan_num = 0
            line = []
            for i in row:
                if np.isnan(i):
                    nan_num += 1
                else:
                    line.append(i)
            print('nan number = ', nan_num)
            draw_num(line, index + '4')
            five = fiveNumber(line)
            print(five)


if __name__ == "__main__":
    # data = pd.read_csv('Oakland_Crime_Statistics/records-for-2011.csv')       #读入数据
    data = pd.read_csv('MLB/2019_atbats.csv')
    row_data_deal(data)
    one(data)
    two(data)
    # three(data)
    four(data)
