# author:Mike
# -*- coding=UTF-8 -*-
import json
import os
import csv
import time
import pysnooper
class Jsontool:
    @classmethod
    def dict_generator(cls,indict,pre=None):
        pre = pre if pre else []
        if isinstance(indict, dict):
            for key, value in indict.items():
                if isinstance(value, dict):
                    if len(value) == 0:
                        yield pre + [key, '{}']
                    else:
                        for d in cls.dict_generator(value, pre + [key]):
                            yield d
                elif isinstance(value, list):
                    if len(value) == 0:
                        yield pre + [key, '[]']
                    else:
                        for v in value:
                            for d in cls.dict_generator(v, pre + [key]):
                                yield d
                elif isinstance(value, tuple):
                    if len(value) == 0:
                        yield pre + [key, '()']
                    else:
                        for v in value:
                            for d in cls.dict_generator(v, pre + [key]):
                                yield d
                else:
                    yield pre + [key, value]
        else:
            yield pre + [indict]


def fileop(filepath):
    global filenames
    filenames = []
    for i in os.listdir(filepath):
        if not i.endswith('.json'):
            continue
        filenames.append(i)
    return filenames


def csvop(csvpath):
    global csvfile
    csvname_time = time.strftime("%m-%d_%H-%M", time.localtime(int(time.time())))
    csvname = 'log' + csvname_time + '.csv'
    csvfile = os.path.join(csvpath, csvname)
    return csvfile

# @pysnooper.snoop()
def general(filepath,csvpath):
    fileop(filepath)
    csvop(csvpath)
    output_list = []
    key_list = []
    basic_list = ['dut_id', 'station_id', 'outcome', 'test_mode', 'slot', 'start_time_millis', 'end_time_millis']
    with open(csvfile, 'w+', newline='') as result:
        result_write = csv.writer(result, delimiter=',')
        count = 0
        for filename, m in zip(filenames, range(len(filenames))):
            print(filename)
            with open(os.path.join(filepath, filename), 'r') as fs:
                data_read = fs.read()
                data = json.loads(data_read)
            count+=1
            print(count)
            for h in basic_list:
                for i in Jsontool.dict_generator(data):
                    if h == i[0]:
                        key_list.append(i[0])
                        output_list.append(i[-1])

            for i in Jsontool.dict_generator(data):
                if i[0] == 'phases' and i[-2] == 'measured_value':
                    key_list.append(i[-3])
                    output_list.append(i[-1])

            if m == 0:
                result_write.writerow(key_list)
            result_write.writerow(output_list)
            output_list = []
            key_list = []
        print('OK!!')
        return csvfile

def main():
    # global filepath
    # global csvpath
    filepath = r'C:\Users\Administrator\Desktop\json_to_excel'
    csvpath = r'C:\Users\Administrator\Desktop\json_to_excel'

    general(filepath,csvpath)


if __name__ == '__main__':
    main()
