#!/usr/bin/env python

# Define global debug function
debug = lambda data : print(f'>> Debug: {data}') if type(data) == str else print('>> Debug: ', data)