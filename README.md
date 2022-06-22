# Schedule Generator

Hello there! This is the standalone repository for the schedule generator from my [school-management-api](https://github.com/SowinskiBraeden/school-management-api) project.

The algorithm reads student requests and generates a timetable for all requested classes and fills them with students, giving the students their own schedules.

The algorithm has been moved out of `tinker.py` into its own python script. Version 1 and 2 are removed and the script can be found in the `/scheduleGenerator` folder. The algorithm has come a long way; using real 2018 course selection data from my school, enabling me to better test the script. V3 has a entirely different approach from V1 and V2, that you can read about at the top of the function in [`generator.py`](/scheduleGenerator/generator.py). The function is broken up into 6 steps, each step is labeled within the function with a comment, giving a brief explination of what that step contributes to the algorithm.

This is the output after running it with the following command
```
  $ ./tinker.py
```

![preview](/preview/generator-preview.png)


A more in depth error log can be read with the additional argument
```
  $ ./tinker.py errors
```

![preview](/preview/error-preview.png)
