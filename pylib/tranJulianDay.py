print("引入tranJulianDay包")
import math
import osLib
# JD是JulianDay的缩写
#儒略历是一种历法，太阳历，四年一闰，每一天用日期格式表示
#格里历是一种历法，太阳历，四年一闰，但逢世纪年还要看能否被400整除，400年97闰
#1582年10.04后一天改为10.15
#儒略日是数字格式，以儒略历公元前4713年1月1日12:00为起点，过一天+1，时分秒用小数表示
# 儒略历日期转儒略日
def JulianCalendarDate2JD(year,month,day):
    a=math.floor((14-month)/12)
    y=year+4800-a
    m=month+12*a-3
    JD=day+math.floor((153*m+2)/5)+365*y+math.floor(y/4)-32083
    return JD

def GregorianCalendarDate2JD(year,month,day):
    a=math.floor((14-month)/12)
    y=year+4800-a
    m=month+12*a-3
    JD=day+math.floor((153*m+2)/5)+365*y+math.floor(y/4)-math.floor(y/100)+math.floor(y/400)-32045
    return JD

#一直使用儒略历，儒略日转儒略历日期
def JD2JulianCalendar(JD):
    print('儒略历')
    #32083=32142-59,相当于把1、2月提到了前一年，这一年从3月开始
    y0=math.floor((JD+32083)/365.25)
    y=y0-4800
    days=JD+32083-math.floor(y0*365.25)
    m=math.floor((days-0.6)/30.6)+3
    if days==0:
        d=29
    else:
        d=days-round((m-3)*30.6)

    if m>12:
        m=m-12
        y=y+1

    JulianCalendar=str(y)+"/"+str(m)+"/"+str(d)
    print(JulianCalendar)
    return [y,m,d]

# 一直使用格里历
def JD2GregorianCalendar(JD):
    print('格里历')

    JD0=JD+32045
    #y0=math.floor((JD0)/365.25)
    A=math.floor(JD0/36524.25)
    B=math.floor(JD0/36524.25/4)
    y0=math.floor((JD0+A-B)/365.25)
    y=y0-4800
    days=JD+32045-math.floor(y0*365.25)+A-B
    m=math.floor((days-0.6)/30.6)+3
    if days==0:
        d=29
    else:
        d=days-round((m-3)*30.6)

    if m>12:
        m=m-12
        y=y+1

    GregorianCalendar=str(y)+"/"+str(m)+"/"+str(d)
    print(GregorianCalendar)
    return [y,m,d]

# 通行历法，1582年10.04前为儒略历，次日改为格里历1582年10.15
def JD2Calendar(JD):
    if JD<2299161:
        return JD2JulianCalendar(JD)
    else:
        return JD2GregorianCalendar(JD)

def Calendar2JD(year,month,day):
    if (year<1582) or (year==1582 and month<10) or (year==1582 and month==10 and day<15):
        JD=JulianCalendarDate2JD(year,month,day)
    else:
        JD=GregorianCalendarDate2JD(year,month,day)
    return JD

def isRunNian(y):
    if y>1582:
        if y%4==0:
            if y%100==0:
                if y%400==0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    else:
        if y%4==0:
            return True
        else:
            return False
def JD2Period(date1,date2):
    #date1=JD2Calendar(JD1)
    #date2=JD2Calendar(JD2)
    y1=date1[0];m1=date1[1];d1=date1[2]
    y2=date2[0];m2=date2[1];d2=date2[2]
    JD=1414247
    startJD=0
    endJD=1414247
    for y in range(y1,y2+1):
        yearstartJD=endJD+1
        for m in range(1,13):
            if m in [1,3,5,7,8,10,12]:
                JD=JD+1
                startJD=JD
                if y==1582 and m==10:
                    JD=JD+20
                else:
                    JD=JD+30
                endJD=JD
            if m in [4,6,9,11]:
                JD=JD+1
                startJD=JD
                JD=JD+29
                endJD=JD
            if m==2:
                JD=JD+1
                startJD=JD
                if isRunNian(y):
                    JD=JD+28
                else:
                    JD=JD+27
                endJD=JD
            print(y,m,startJD,endJD)
            out=[str(y)+'年'+str(m)+'月',startJD,endJD]

            osLib.write2csv('D:\\CalendarDate\\MonthJDRange.csv',out)
        out=[str(y)+'年',yearstartJD,endJD]

        osLib.write2csv('D:\\CalendarDate\\YearJDRange.csv',out)
    # if y2-y1==0:
    #     for month in range(m1,m2+1):
    #         print(y1,month)
    # if y2-y1==1:
    #     for month in range(m1,13):
    #         print(y1,month)
    #     for month in range(1,m2+1):
    #         print(y2,month)
    # if y2-y1>=2:
    #     for month in range(m1,13):
    #         print(y1,month)
    #     for month in range(1,m2+1):
    #         print(y2,month)
    #     for y in range(y1+1,y2):
    #         for month in range(1,13):
    #             print(y,month)
    return []

if __name__ == '__main__':
    JD2Period([-840,1,1],[2100,1,1])
    #print(Calendar2JD(1582,10,4))
    #print(Calendar2JD(1582,10,6))
    print(Calendar2JD(-840,1,31))#1414248
    JD2Calendar(2488404)