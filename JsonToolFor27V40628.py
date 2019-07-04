# -*- coding=UTF-8 -*
# author:超-
import json
import os
import csv
import time
class Jsontool(object):
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
    def general(self,csvpath,filepath):
        self.fileop(filepath)
        self.csvop(csvpath)
        global basic_list
        output_list = []
        key_list = []
        #for python2.7
        with open(csvfile, 'wb') as result:
        #for python3
        # with open(csvfile, 'w+', newline='') as result:
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
                cycletime = (float(output_list[-1]) - float(output_list[-2]))/1000
                output_list[-2] = self.time_trans(float(output_list[-2]))
                output_list[-1] = self.time_trans(float(output_list[-1]))
                key_list.append('cycletime')
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
    def guest(self,csvpath,filepath,need):
        self.fileop(filepath)
        self.csvop(csvpath)
        self.need = need
        global basic_list
        output_list = []
        key_list = []
        #此处输入你所需的测项
        
        #for python2.7
        with open(csvfile, 'wb') as result:
        #for python3
        #with open(csvfile, 'w+', newline='') as result:
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
                cycletime = (float(output_list[-1]) - float(output_list[-2]))/1000
                output_list[-2] = self.time_trans(float(output_list[-2]))
                output_list[-1] = self.time_trans(float(output_list[-1]))
                for j in self.need:
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
        #for python2.7
        with open(csvfile, 'wb') as result:
        #for python3
        #with open(csvfile, 'w+', newline='') as result:
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
                cycletime = (float(output_list[-1]) - float(output_list[-2]))/1000
                output_list[-2] = self.time_trans(float(output_list[-2]))
                output_list[-1] = self.time_trans(float(output_list[-1]))
                key_list.append('cycletime')
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
    def failfilter(self,csvpath,filepath):
        self.fileop(filepath)
        self.csvop(csvpath)
        global basic_list
        output_list = []
        key_list = []
        fail_list = []
        spec_list = ['spec'] + [' '] * 7
        #for python2.7
        with open(csvfile, 'wb') as result:
        #for python3
        # with open(csvfile, 'w+', newline='',encoding='UTF-8') as result:
            result_write = csv.writer(result, delimiter=',')
            count = 0
            for filename, m in zip(filenames, range(len(filenames))):
                # print(filename)
                with open(os.path.join(filepath, filename), 'r') as fs:
                    data_read = fs.read()
                    data = json.loads(data_read)
                    if not data['outcome'] == 'PASS' :
                        print(filename)
                        for i in self.dict_generator(data):     
                            if i[0] == 'phases' and i[-2] == 'outcome' and not i[-1] == 'PASS':
                                fail_list.append(i[-3])
                        for h in basic_list:
                            for i in self.dict_generator(data):
                                if h == i[0]:
                                    key_list.append(i[0])
                                    output_list.append(i[-1])
                        #时间转换＆计算cycletime
                        cycletime = (float(output_list[-1]) - float(output_list[-2]))/1000
                        output_list[-2] = self.time_trans(float(output_list[-2]))
                        output_list[-1] = self.time_trans(float(output_list[-1]))
                        key_list.append('cycletime')
                        output_list.append(cycletime)
                        for j in fail_list:
                            for i in self.dict_generator(data):
                                if i[0] == 'phases' and i[-2] == 'validators' and i[-3] == j:
                                    # spec_list.append('spec')
                                    #加引号，要不spec显示在Excel会出现#NAME错误
                                    a = "'" + i[-1] + "'"
                                    spec_list.append(a)                               
                                if i[0] == 'phases' and i[-2] == 'measured_value' and i[-3] == j:
                                    key_list.append(i[-3])
                                    output_list.append(i[-1])

                        if m == 0:            
                            info = ['fail items show']
                            result_write.writerow(info)                           
                        result_write.writerow(key_list)
                        result_write.writerow(output_list)
                        result_write.writerow(spec_list) 
                        spec_list = ['spec'] + [' '] * 7
                        key_list = []
                        output_list = []
                        fail_list = []
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
    #需要的测项
    need = ['POS0_ACCEL_MEAN_X','POS0_GYRO_STDEV_X','POS0_ACCEL_STDEV_Z','POS1_ACCEL_MEAN_X','POS1_GYRO_MEAN_X']
    #json文件的地址
    filepath = r'C:\Users\tony\Desktop\imu6_fail_rate_analysis\json_input\pass\production'
    #csv输出的地址
    csvpath = r'C:\Users\tony\Desktop\IMU6'

    gua = Jsontool(csvpath,filepath)
    gua.failfilter(csvpath,filepath)


if __name__ == '__main__':
    main()
