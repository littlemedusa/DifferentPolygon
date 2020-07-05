import numpy as np
import matplotlib.pyplot as plt
import copy
import os

def setting():
    #多边形的边数为n
    n = 6
    #随机生成点的次数为iteration
    iteration = 1000
    return n, iteration

#(x3,y3)点到过(x1,y1)和(x2,y2)的直线的距离，区分正负
def f(x1,y1,x2,y2,x3,y3):
    distance = (y1-y2)*x3-(x1-x2)*y3+x1*y2-x2*y1
    return round(distance,6)

def polygon(n):
    #坐标list
    x = [0]*n
    y = [0]*n
    for i in range(n):
        x[i] = round(np.random.rand(),3)
        y[i] = round(np.random.rand(),3)
    condition = True
    for i in range(n-2):
        for j in range(i+1,n-1):
            for k in range(j+1,n):
                result = f(x[i],y[i],x[j],y[j],x[k],y[k])
                if(result == 0):
                    condition = False

    # print(x)
    # print(y)
    if(condition):
        count = newdot(x=x,y=y,side=[0],count=0)
        all_side = []
        result = count//2
        return result,x,y
    else:
        return 0,x,y

#从0开始,side为边的list，count为可行方案的计数(2倍)
def newdot(x,y,side=[0],count=0):
    for i in range(n):
        if(i not in side):
            # print(side)
            # print(i)
            new_dot = True
            previous_dot = side[-1]
            current_dot = i
            test = [0]*len(side)
            for j in range(len(side)):
                test_dot = side[j]
                test[j] = f(x[previous_dot],y[previous_dot],x[current_dot],y[current_dot],x[test_dot],y[test_dot])
            for j in range(len(side)-1):
                if(test[j]*test[j+1]<0):
                    dis_1 = f(x[side[j]],y[side[j]],x[side[j+1]],y[side[j+1]],x[previous_dot],y[previous_dot])
                    dis_2 = f(x[side[j]],y[side[j]],x[side[j+1]],y[side[j+1]],x[current_dot],y[current_dot])
                    if(dis_1*dis_2<0):
                        # print(previous_dot,current_dot,";",side[j],side[j+1],"cross")
                        # print(test[j],test[j+1],dis_1,dis_2)
                        new_dot = False
            if(new_dot):
                # print("succeed")
                side.append(i)
                if(set(all_dot) == set(side)):
                    new_line = True
                    previous_dot = side[-1]
                    current_dot = 0
                    test = [0]*len(side)
                    for j in range(len(side)):
                        test_dot = side[j]
                        test[j] = f(x[previous_dot],y[previous_dot],x[current_dot],y[current_dot],x[test_dot],y[test_dot])
                    for j in range(len(side)-1):
                        if(test[j]*test[j+1]<0):
                            dis_1 = f(x[side[j]],y[side[j]],x[side[j+1]],y[side[j+1]],x[previous_dot],y[previous_dot])
                            dis_2 = f(x[side[j]],y[side[j]],x[side[j+1]],y[side[j+1]],x[current_dot],y[current_dot])
                            if(dis_1*dis_2<0):
                                new_line = False
                    if(new_line):
                        all_side.append(copy.deepcopy(side))
                        # print(side)
                        count += 1                
                count = newdot(x,y,side,count)
        if(i == n-1):
            del side[-1]
                    
    return count

def RemoveSamePic(all_side):
    for i in range(len(all_side)):
        if(i<len(all_side)):
            side = copy.deepcopy(all_side[i])
            side.remove(0)
            side.reverse()
            side.insert(0,0)
            if(side in all_side):
                all_side.remove(side)
    return all_side  

def draw():
    b = os.getcwd()
    os.mkdir(b+'/polygon_%s'%(n))
    plt.scatter(max_x, max_y, s=20, c="r", marker='o')
    plt.savefig(b+'/polygon_%s/scatter.png'%(n))
    # plt.show()
    plt.close('all')
    for i in range(len(all_side)):
        plt.scatter(max_x, max_y, s=20, c="r", marker='o')
        side = all_side[i]
        for j in range(len(side)):
            if(j == len(side)-1):
                j_next = 0;
            else:
                j_next = j + 1
            x_line = [max_x[side[j]],max_x[side[j_next]]]
            y_line = [max_y[side[j]],max_y[side[j_next]]]
            plt.plot(x_line, y_line, color='b')
        plt.savefig(b+'/polygon_%s/pic_%s.png'%(n,i+1))
        # plt.show()
        plt.close('all')

if __name__ == '__main__':
    n, iteration = setting()
    all_side = []
    all_dot = np.arange(n)
    max_result, max_x, max_y = 0, 0, 0
    for i in range(iteration):
        if(i%(iteration//100)==0):
            print(i/(iteration//100),"%")
        result,x,y = polygon(n)
        if(result>max_result):
            max_result = result
            max_x = x
            max_y = y
    print("Max value of different polygons in %s points: "%(n), max_result)
    print("X_coordinate: ", max_x)
    print("Y_coordinate: ", max_y)

    #具体例子、路线、散点图
    all_side = []
    count = newdot(x=max_x,y=max_y,side=[0],count=0)
    #去掉重复图形
    all_side = RemoveSamePic(all_side) 
    #检验绘图的数量有没有问题       
    print("Picture in polygon_%s: "%(n), len(all_side)==max_result)
    draw()
    

    







