# author:Mike
# -*- coding=UTF-8 -*-
import json
import os
import csv
import time
import pysnooper
class Jsontool:
    def __init__(self,csvpath,filepath):
        self.csvpath = csvpath
        self.filepath = filepath
    def dict_generator(self,indict,pre=None):
        pre = pre if pre else []
        if isinstance(indict, dict):
            for key, value in indict.items():
                if isinstance(value, dict):
                    if len(value) == 0:
                        yield pre + [key, '{}']
                    else:
                        for d in self.dict_generator(value, pre + [key]):
                            yield d
                elif isinstance(value, list):
                    if len(value) == 0:
                        yield pre + [key, '[]']
                    else:
                        for v in value:
                            for d in self.dict_generator(v, pre + [key]):
                                yield d
                elif isinstance(value, tuple):
                    if len(value) == 0:
                        yield pre + [key, '()']
                    else:
                        for v in value:
                            for d in self.dict_generator(v, pre + [key]):
                                yield d
                else:
                    yield pre + [key, value]
        else:
            yield pre + [indict]


    def fileop(self,filepath):
        global filenames,basic_list
        filenames = []
        basic_list = ['dut_id', 'station_id', 'outcome', 'test_mode', 'slot', 'start_time_millis', 'end_time_millis']
        for i in os.listdir(filepath):
            if not i.endswith('.json'):
                continue
            filenames.append(i)
        return filenames


    def csvop(self,csvpath):
        global csvfile
        csvname_time = time.strftime("%m-%d_%H-%M", time.localtime(int(time.time())))
        csvname = 'log' + csvname_time + '.csv'
        csvfile = os.path.join(csvpath, csvname)
        return csvfile

    # @pysnooper.snoop()
    #输出所有的测项
    def general(self,filepath,csvpath):
        self.fileop(filepath)
        self.csvop(csvpath)
        global basic_list
        output_list = []
        key_list = []
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
                    for i in self.dict_generator(data):
                        if h == i[0]:
                            key_list.append(i[0])
                            output_list.append(i[-1])
                #时间转换＆计算cycletime
                key_list[-2] = self.time_trans(float(output_list[-2]))
                key_list[-1] = self.time_trans(float(output_list[-1]))
                cycletime = (float(output_list[-1]) - float(output_list[-2]))/1000
                key_list.append('clcletime')
                output_list.append(cycletime)
                for i in self.dict_generator(data):
                    if i[0] == 'phases' and i[-2] == 'measured_value':
                        key_list.append(i[-3])
                        output_list.append(i[-1])
                #第一行只需写一次
                if m == 0:
                    result_write.writerow(key_list)
                result_write.writerow(output_list)
                output_list = []
                key_list = []
            print('OK!!')
            return csvfile
    #输出指定的测项
    def guest(self,csvpath,filepath):
        self.fileop(filepath)
        self.csvop(csvpath)
        global basic_list
        output_list = []
        key_list = []
        #此处输入你所需的测项
        need = ['POS0_ACCEL_MEAN_X','POS0_GYRO_STDEV_X','POS0_ACCEL_STDEV_Z','POS1_ACCEL_MEAN_X','POS1_GYRO_MEAN_X']
        with open(csvfile, 'w+', newline='') as result:
            result_write = csv.writer(result, delimiter=',')
            count = 0
            for filename, m in zip(filenames, range(len(filenames))):
                print(filename)
                with open(os.path.join(filepath, filename), 'r') as fs:
                    data_read = fs.read()
                    data = json.loads(data_read)
                count += 1
                print(count)
                for h in basic_list:
                    for i in self.dict_generator(data):
                        if h == i[0]:
                            key_list.append(i[0])
                            output_list.append(i[-1])
                for j in need:
                    for i in self.dict_generator(data):
                        if i[0] == 'phases' and i[-2] == 'measured_value' and i[-3] == j:
                            key_list.append(i[-3])
                            output_list.append(i[-1])

                if m == 0:
                    result_write.writerow(key_list)
                result_write.writerow(output_list)
                output_list = []
                key_list = []
            print('OK!!')
            return csvfile
    #计算所有phase的时间
    def phasetime(self,csvpath,filepath):
        self.fileop(filepath)
        self.csvop(csvpath)
        global basic_list
        output_list = []
        key_list = []
        time_list = []
        start_time = []
        end_time = []
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
                    for i in self.dict_generator(data):
                        if h == i[0]:
                            key_list.append(i[0])
                            output_list.append(i[-1])
                #时间转换＆计算cycletime
                key_list[-2] = self.time_trans(float(output_list[-2]))
                key_list[-1] = self.time_trans(float(output_list[-1]))
                cycletime = (float(output_list[-1]) - float(output_list[-2]))/1000
                key_list.append('clcletime')
                output_list.append(cycletime)
                for i in self.dict_generator(data):
                    if i[0] == 'phases' and i[1] == 'start_time_millis' :
                        start_time.append(i[-1])
                    if i[0] == 'phases' and i[1] == 'end_time_millis':
                        end_time.append(i[-1])
                for l in range(len(end_time)):
                    time_list.append(abs(float(end_time[l]) - float(start_time[l]))/1000)
                start_time = []
                end_time = []
                for i in self.dict_generator(data):
                    if i[0] == 'phases' and i[1] == 'name':
                        key_list.append(i[-1])
                #第一行只需写一次
                if m == 0:
                    result_write.writerow(key_list)
                result_write.writerow(output_list+time_list)
                output_list = []
                key_list = []
                time_list = []
            print('OK!!')
            return csvfile

    def time_trans(self,timedata):
        if len(str(int(timedata))) == 10:
            timeStamp = float(timedata)
        else:
            timeStamp = float(timedata) / 1000
        timeArray = time.localtime(timeStamp)
        timestyle = time.strftime("%y-%m-%d,%H:%M:%S", timeArray)
        return timestyle


def main():
    # global filepath
    # global csvpath
    filepath = r'C:\Users\Administrator\Desktop\json_to_excel'
    csvpath = r'C:\Users\Administrator\Desktop\json_to_excel'

    gua = Jsontool(csvpath,filepath)
    gua.phasetime(csvpath,filepath)


if __name__ == '__main__':
    main()
