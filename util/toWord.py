#!/usr/bin/env python3.11

from docx.shared import Inches
import docx
import json

flex = ("XAT--12A-S", "XAT--12B-S")

def putScheduleToWord(student):
	# create an instance of a word doc.
	doc = docx.Document()

	doc.add_heading(f'Schedule for Student {student["Pupil #"]}')

	# Create a table object
	table = doc.add_table(rows=1, cols=4)
	table.autofit = True
	table.style = 'Colorful List'

	# course name + (code) | block | semester | room
	row = table.rows[0].cells
	row[0].text = 'Course'
	row[1].text = 'Block'
	row[2].text = 'Sem.'
	row[3].text = 'Room #'
 
	table.columns[0].width = Inches(3.5)
	table.columns[1].width = Inches(0.75)
	table.columns[2].width = Inches(0.75)

	for block in student['schedule']:
		courseCode = student["schedule"][block][0]
		if courseCode in flex: courseName = 'Study'
		else: courseName = courses[courseCode[:-2]]["Description"]
		blockNum = int(block.split('block')[1])
		semester = 2 if blockNum > 5 else 1
		if blockNum > 5: blockNum -= 5
		row = table.add_row().cells
		row[0].text = f'{courseName}\n({courseCode})'
		row[1].text = str(blockNum)
		row[2].text = str(semester)
		row[3].text = 'B101'

	for row in table.rows:
		row.height = Inches(0.75)

	doc.save(f'../output/student_schedules/{student["Pupil #"]}_schedule.docx')

def main():
	global courses

	# Get students
	try:
		with open("../output/students.json", 'r') as studentFile: students = json.load(studentFile)
	except FileNotFoundError:
		with open("./output/students.json", 'r') as studentFile: students = json.load(studentFile)

  # get course information
	try:
		with open("../output/courses.json", 'r') as courseFile: courses = json.load(courseFile)
	except FileNotFoundError:
		with open("./output/courses.json", 'r') as courseFile: courses = json.load(courseFile)

  # Define students grade level
	for student in students:
		putScheduleToWord(student)

if __name__ == '__main__':
	main()