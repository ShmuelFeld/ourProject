#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow as tf

def ourfilter(input_files):
    for input_file in input_files:
        splitToLines = []
        reWriten = []
        fi = open(input_file, 'r+')
        lines = fi.readlines()
        for sentence in lines:
            if ". " in sentence:
            #means we want to create two sentences from this one
                splitToLines.append(sentence.replace(". ", '\n'))
            else:
                splitToLines.append(sentence)
        for sentence in splitToLines:
            if "צד א" in sentence:
                reWriten.append(sentence.split("צד א: ")[1])
            elif "צד ב" in sentence:
                reWriten.append(sentence.split("צד ב: ")[1])
            else:
                reWriten.append(sentence)
        fi.seek(0,0)
        fi.truncate()
        fi.writelines(reWriten)
        fi.close()




    return
input_files = []
match = tf.gfile.Glob("../inputFiles_Heb/*.txt")
input_files.extend(match)
ourfilter(input_files)