#!/usr/bin/env python3.11

# Define global debug function
debug = lambda data : print(f'>> Debug: {data}') if type(data) == str else print('>> Debug: ', data)