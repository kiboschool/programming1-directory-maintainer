# Use Case

As a tools SW engineer at a factory site, a reporting and data analysts team asked for your assistance to categorize the backlog of the system which looks a bit messy. Current situation is that all stakeholders send/insert files with different types into one main backlog for later usage! When the number of files started scaling up, file retrieval started to be challenging. Their current backlog has three types of files:

```
- CSV
- LOG
- TXT
```

# Requirements

You need to write a program that modifies the structure of the backlog pool into something more readable and unser friendly. Your program is expected to support the following items:
- File Categorisation: Within the main folder, create a new folder for each file extension type. Folder name is to be the `extension`. For example, a folder called CSV will have all csv files within.
- Log Window: Each time your program runs, it should make sure that the Log folder maintains a threshold window of files `window_threshold`. For example - if the threshold is 5, then the folder should have the `lastest` 5 logs only. others to be deleted.
- Large files: Within the txt folder, files with a size greater than a `size_threshold` should be maintaned into separate internal folder called `txt_large_files` -> threshold value is assumed to be in KB

 # User perspective

 A user would enter a big messy directory to your program and the program has to support all mentioned points. A user is expected to have the ability to modify threshold values from time to time to suite a specific use case.
 Your program should modify same directory input - so you may need to keep a backup copy while coding.

 # Output Snapshot
 
 If we have a directory that looks like the following:
 
 ```
 - Backlog
   - sheet_1.csv
   - sheet_2.csv
   - component_x.log
   - employees_i.txt
   - employees_ii.txt
   - component_y.log
   - component_z.log
 ```

After running your program - it should look like something like this:

 ```
 - Backlog
   - CSV
     - sheet_1.csv
     - sheet_2.csv
   - LOG
     - component_x.log
     - component_y.log
     - component_z.log
   - TXT
     - employees_i.txt
     - txt_large_files
       - employees_ii.txt
 ```

 ## Hints

 - Check the built-in function sorted in python and how to use it.