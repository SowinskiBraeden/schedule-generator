#!/usr/bin/env python
import json

# Get students
try:
  with open("../output/students.json") as studentFile: students = json.load(studentFile)
except FileNotFoundError:
  with open("./output/students.json") as studentFile: students = json.load(studentFile)

flex = ("XAT--12A-S", "XAT--12B-S")

most_frequent = lambda l : max(set(l), key = l.count)

def getEstimatedGrade(pupil: dict) -> int:
  grades = [] # List of all possible grades
  for request in pupil["requests"]:
    if request["CrsNo"] in flex: continue
    for extractedGrade in [int(s) for s in request["CrsNo"].split("-") if s.isdigit()]:
      grades.append(extractedGrade)

  return None if len(grades) == 0 else most_frequent(grades) # Final estimate of grade

if __name__ == '__main__':
  # Define students grade level
  for student in students:
    student["gradelevel"] = getEstimatedGrade(student)
