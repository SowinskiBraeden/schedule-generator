#!/usr/bin/env python
import json

# Get students
try:
  with open("../output/students.json", 'r') as studentFile: students = json.load(studentFile)
except FileNotFoundError:
  with open("./output/students.json", 'r') as studentFile: students = json.load(studentFile)

flex = ("XAT--12A-S", "XAT--12B-S")

most_frequent = lambda l : max(set(l), key = l.count)

def getEstimatedGrade(pupil: dict) -> int:
  grades = [] # List of all possible grades
  for request in (r for r in pupil["requests"] if r not in flex):
    for extractedGrade in [int(s) for s in request["CrsNo"].split("-") if s.isdigit()]:
      grades.append(extractedGrade)

  return None if len(grades) == 0 else most_frequent(grades) # Final estimate of grade

if __name__ == '__main__':
  # Define students grade level
  for student in students:
    student["gradelevel"] = getEstimatedGrade(student)
  try:
    with open('../output/students.json', 'w') as studentFile:
      json.dump(students, studentFile, indent=2)
  except FileNotFoundError:
    with open('./output/students/json', 'w') as studnetFile:
      json.dump(students, studentFile, indent=2)
