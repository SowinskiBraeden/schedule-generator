#!/usr/bin/env python3.113.11
from os.path import exists as file_exists
from prettytable import PrettyTable
from typing import Tuple
from time import time, sleep
import itertools
import threading
import json
import sys

# Import required utilities
from util.mockStudents import getSampleStudents
from util.generateCourses import getSampleCourses

# Import other utilities
from util.debug import debug

# Import Algorithm
from scheduleGenerator.generator import generateScheduleV3

done = False

# consts
blockClassLimit = 40

# print()
# debug(f'Current blockClassLimit = {blockClassLimit}')
  
def processing(msg: str):
  for c in itertools.cycle(['|', '/', '-', '\\']):
    if done: break
    sys.stdout.write(f'\r{msg} {c}')
    sys.stdout.flush()
    sleep(0.1)

def errorOutput(students) -> Tuple[PrettyTable, dict, dict]:
  # Error Table calulation / output  
  f = open('./output/conflicts.json')
  conflicts = json.load(f)
  f.close()
  totalCritical = conflicts["Critical"]["Students"]
  totalAcceptable = conflicts["Acceptable"]["Students"]

  t = PrettyTable(['Type', 'Error %', 'Success %', 'Student Error Ratio'])
  
  errorsC = round(totalCritical / len(students) * 100, 2)
  successC = round(100 - errorsC, 2)
  errorsA = round(totalAcceptable / len(students) * 100, 2)
  successA = round(100 - errorsA, 2)
  
  t.add_row(['Critical', f"{errorsC} %", f"{successC} %", f"{totalCritical}/{len(students)} Students"])
  t.add_row(['Acceptable', f"{errorsA} %", f"{successA} %", f"{totalAcceptable}/{len(students)} Students"])
  
  return t, conflicts["Critical"], conflicts["Acceptable"]

def main():  
  showError = False
  noAnim = False
  for e in sys.argv:
    if e.lower().replace('_', '') == 'showerror': showError = True
    if e.lower().replace('_', '') == 'noanim': noAnim = True

  if (len(sys.argv) > 1 and sys.argv[1] not in ('no_refresh', 'errors')) or len(sys.argv) == 1:
    print()

    st = time() # Start time
    
    if noAnim:
      sampleStudents = getSampleStudents("./sample_data/course_selection_data.csv", True)
      sampleCourses = getSampleCourses("./sample_data/course_selection_data.csv", True)
      timetable = {}
      timetable["Version"] = 3
      timetable["timetable"] = generateScheduleV3(sampleStudents, sampleCourses, blockClassLimit, "./output/students.json", "./output/conflicts.json")
    else:
      t = threading.Thread(target=processing, args=('Collection student requests',))
      t.start() # Start animation
      sampleStudents = getSampleStudents("./sample_data/course_selection_data.csv", True)
      done = True # End Animation
      print('\nStudent list generated.\n')


      t = threading.Thread(target=processing, args=('Collection Course Information',))
      done = False # reset animation
      t.start() # Start animation
      sampleCourses = getSampleCourses("./sample_data/course_selection_data.csv", True)
      done = True # End Animation
      print('\nCourse Information Collected.\n')
      
      sleep(0.1)
      t = threading.Thread(target=processing, args=('Processing',))
      done = False # reset animation
      t.start() # Start animation
      timetable = {}
      timetable["Version"] = 3
      timetable["timetable"] = generateScheduleV3(sampleStudents, sampleCourses, blockClassLimit, "./output/students.json", "./output/conflicts.json")

      done = True # End Animation
    
    et = time() # End time
    elapsed_time = round((et - st), 3) # Execution time
    print(f'\n\nDone - Finished in {elapsed_time} seconds\n')

    if showError:
      errors, _, _ = errorOutput(sampleStudents)
      print(errors)

    with open("./output/timetable.json", "w") as outfile:
      json.dump(timetable, outfile, indent=2)

  elif sys.argv[1].lower() == "no_refresh":
    print()

    st = time() # Start time

    if not file_exists('./output/students.json') or not file_exists('./output/courses.json'):
      print('\n No previous data exists, please use the following command\n./tinker.py generate_data')
      exit()

    with open('./output/students.json') as f: sampleStudents = json.load(f)
    with open('./output/courses.json') as f: sampleCourses = json.load(f)

    for student in sampleStudents:
      student["remainingAlts"] = []
      for i in range(1, 11): student["schedule"][f"block{i}"] = []
      student["classes"] = 0
    
    if noAnim:
      timetable = {}
      timetable["Version"] = 3
      timetable["timetable"] = generateScheduleV3(sampleStudents, sampleCourses, blockClassLimit, "./output/students.json", "./output/conflicts.json")
    else :
      t = threading.Thread(target=processing, args=('Processing',))
      t.start() # Start animation
      timetable = {}
      timetable["Version"] = 3
      timetable["timetable"] = generateScheduleV3(sampleStudents, sampleCourses, blockClassLimit, "./output/students.json", "./output/conflicts.json")
      done = True # End Animation
    
    et = time() # End time
    elapsed_time = round((et - st), 3) # Execution time
    print(f'\n\nDone - Finished in {elapsed_time} seconds\n')

    if showError:
      errors, _, _ = errorOutput(sampleStudents)
      print(errors)

    with open("./output/timetable.json", "w") as outfile:
      json.dump(timetable, outfile, indent=2)

  elif sys.argv[1].lower() == "generate_data":
    t = threading.Thread(target=processing, args=('Collection student requests',))
    t.start() # Start animation
    _ = getSampleStudents("./sample_data/course_selection_data.csv", True)
    done = True # End Animation
    print('\nStudent list generated.\n')

    t = threading.Thread(target=processing, args=('Collection Course Information',))
    done = False # reset animation
    t.start() # Start animation
    _ = getSampleCourses("./sample_data/course_selection_data.csv", True)
    done = True # End Animation
    print('\nCourse Information Collected.\n')
    print('You can now use the following command\n./tinker.py no_refresh')

  elif sys.argv[1].upper() == "ERRORS":
    f = open('./output/students.json')
    studentData = json.load(f)
    f.close()
    errors, critical, acceptable = errorOutput(studentData)
    print()
    print(errors)

    print(f"\n{critical['Total']} critical errors")
    for i in range(len(critical["Errors"])):
      print(f"x{critical['Errors'][i]['Total']} {critical['Errors'][i]['Code']} Errors: Critical - {critical['Errors'][i]['Description']}")

    print(f"\n{acceptable['Total']} acceptable errors")
    for i in range(len(acceptable["Errors"])):
      print(f"x{acceptable['Errors'][i]['Total']} {acceptable['Errors'][i]['Code']} Errors: Critical - {acceptable['Errors'][i]['Description']}")

    exit()

  else:
    print("Invalid argument")
    exit()

if __name__ == '__main__':
  main()
