#Use Cases

##Use Case: 1 Single Node Cracking

###CHARACTERISTIC INFORMATION

**Goal in Context:** The user will run the program on a single computer.

**Scope:** End User/Program

**Level:** Primary Function

**Preconditions:** The program is running on a single computer, the user has a hash in one of the supported formats ready to be cracked. The user has files for specific methods of cracking (a dictionary file and/or rainbow table)

**Success End Condition:** The hash will have been found and the user will have the original text used to create it.

**Failed End Condition:** The hash will not have been found.

**Primary Actor:** User, the person operating the software.

**Trigger:** The program is started and single computer mode is selected.

###MAIN SUCCESS SCENARIO

*put here the steps of the scenario from trigger to goal delivery, and any cleanup after*

1. User starts the program.

2. User inputs hash and selects cracking method.

3. User tells program to start cracking.

4. Program requests location of support files as needed.

5. Program finds the text which generated the user's hash.

###EXTENSIONS

*put here there extensions, one at a time, each refering to the step of the main scenario*

* *step altered number* *condition*:

  + *subset number* *action or sub.use case*
  
* 1a. User has selected Server mode
  + 1a1. Program displays its IP address and waits for nodes to connect.
* 1b. User has selected Node mode
  + 1b1. Program requests server IP address. 
  + 1b2. Program connects to server.
* 1c. User has selected Single Computer mode
  + 1c1. Program moves directly to input and mode selection screen.

* 4a. User has selected Brute Force cracking
  + 4a1. No further action is required.
* 4b. User has selected dictionary cracking
  + 4b1. Program requests dictionary file.
  + 4b2. If no file is available, program cannot continue.
* 4c. User has selected Rainbow Table cracking
  + 4c1. Program requests rainbow table file.
  + 4c2. If no file is available, user may generate a rainbow table.
* 5a. Program does not find the original text.
  + 5a1. The wrong hash function may have been selected.
  + 5a2. The dictionary file may not have contained the original text.
  + 5a3. The rainbow table may not have been complete.
  + 5a4. The key length may have been too long.
  
###SUB-VARIATIONS

*put here the sub-variations that will cause eventual bifurcation in the scenario*

* *step or variation number* *list of sub-variations*

* 1a. User may select program mode
Single Computer,
Node,
Server


* 2a. User may choose cracking method
brute force,
dictionary,
rainbow table

 


###RELATED INFORMATION (optional)

**Priority:** *how critical to your system / organization*

**Performance Target:** *the amount of time this use case should take*

**Frequency:** *how often it is expected to happen*

**Superordinate Use Case:** *optional, name of use case that includes this one*

**Subordinate Use Cases:** *optional, depending on tools, links to sub.use cases*

**Channel to primary actor:** *e.g. interactive, static files, database*

**Secondary Actors:** *list of other systems needed to accomplish use case*

**Channel to Secondary Actors:** *e.g. interactive, static, file, database, timeout*

###OPEN ISSUES (optional)

*list of issues about this use cases awaiting decisions*

###SCHEDULE

**Due Date:** *date or release of deployment*

...any other schedule / staffing information you need…
