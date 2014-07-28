#!/usr/bin/env python

import csv
fp = open('test.csv', 'w')
a = csv.writer(fp, delimiter=',')
data = [['Me', 'You'],['293', '219'],['54', '13']]
a.writerows(data)
fp.close()
