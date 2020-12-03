'''
simpleset.py
'''
from functools import *

def intersect(*ar):
    ''' 교집합 '''
    return reduce(__intersectSC, ar)

def __intersectSC(listX, listY):
    setList = []
    for x in listX:
        if x in listY:
            setList.append(x)
    return setList

def difference(*ar):
    ''' 차집합 '''
    setList = []
    intersectSet = intersect(*ar)
    unionSet = union(*ar)
    for x in unionSet:
        if not x in intersectSet:
            setList.append(x)
    return setList

def union(*ar):
    ''' 합집합 '''
    setList = []
    for item in ar:
        for x in item:
            if not x in setList:
                setList.append(x)
    return setList

if __name__ == '__main__':
    print("모듈을 직접 실행했다.")
else:
    print("모듈을 임포트했다.")