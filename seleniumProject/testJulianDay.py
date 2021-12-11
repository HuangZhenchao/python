import tranJulianDay

jd=tranJulianDay.JulianCalendarDate2JD(-56,10,5)
jd2=tranJulianDay.GregorianCalendarDate2JD(2000,2,30)
print('儒略历转儒略日',str(jd))
print('格里历转儒略日',str(jd2))
print('儒略日转儒略历日期',tranJulianDay.JD2Calendar(jd))#1867216