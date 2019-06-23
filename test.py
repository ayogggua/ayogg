import json

def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre+[key, '{}']
                else:
                    for d in dict_generator(value, pre + [key]):
                        yield d
            elif isinstance(value, list):
                if len(value) == 0:
                    yield pre+[key, '[]']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield pre+[key, '()']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            else:
                yield pre + [key, value]
    else:
        yield indict
def usefun(value):
    # print(dict_generator(data).next())
    for i in dict_generator(value):
        # print(i[-2])
        # print('.'.join(i[0:-1]), ':', i[-1])
        # if len(i) > 3:
        if i[0] == 'phases' and i[-2] ==  'measured_value' :
            print(i)
            # print(i[2] + '.' + i[-3]+ ':' +i[-1])
            # if i[-3] == 'sns_cal_version' and i[-2] == 'measured_value':
            #     print(i[-1])

if __name__ == "__main__":
    #去掉转码的符号
    filepath =  r'C:\Users\Administrator\Desktop\json_to_excel\1.json'
    filepath_str = str(filepath).encode('utf-8')
    fs = open(filepath_str, 'r')
    a = fs.read()
    data = json.loads(a)
    fs.close()
    usefun(data)
    # print(dict_generator(data).next())
    # for i in dict_generator(data):
    #     print(i)
    #     print('.'.join(i[0:-1]), ':', i[-1])