# -*- coding: utf-8 -*-
#!/usr/bin/env python
import wx
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as pl
import datetime

def monthNum(month):
        if month == "Jan" :
            return 1
        elif month == "Feb" :
            return 2
        elif month == "Mar" :
            return 3
        elif month == "Apr" :
            return 4
        elif month == "May" :
            return 5
        elif month == "Jun" :
            return 6
        elif month == "Jul" :
            return 7
        elif month == "Aug" :
            return 8
        elif month == "Sep" :
            return 9
        elif month == "Oct" :
            return 10
        elif month == "Nov" :
            return 11
        elif month == "Dec" :
            return 12

def convertDate(dateTime):
        line = dateTime.split(' ')
        print(line)
        date = (str(line[3]) + "-" + str(monthNum(line[2])) + "-" + str(line[5]))
        return date

def readFile(filename):
        values = []
        dates = []
        openedFile = open(filename, "r")
        content = openedFile.readlines()
        openedFile.close()
        for line in content:
            line = line.strip()
            data = line.split("  ")
            values.append(int(data[0]))
            newDate = convertDate(data[1])
            dates.append(newDate)
        print(values)
        print(dates)

        if len(values) != 0 and len(dates) != 0 :
                drawChart(values, dates, filename)

def drawChart(values, dates, filename):
        fig = pl.figure(dpi=60,figsize=(18, 10))
        ax = fig.add_subplot(1,1,1)
        fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.2)
        ax.bar(range(len(dates)), values, facecolor='#777777', align='center', width=0.5, ecolor='black')
        pl.axis('tight')
        ax.set_xticks(range(len(dates)))
        pl.yticks(values)
        ax.set_xticklabels(dates, rotation = 90)
        pl.savefig(filename + ".png")
        pl.show()
        pl.close()

readFile("file.txt")