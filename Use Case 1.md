#Use Cases

##Use Case: 1 Hash Cracking

###CHARACTERISTIC INFORMATION

**Goal in Context:** The user will run the program.

**Scope:** Computer Security Specialists / Password Auditing (Recovery) Specialists / System Administrators

**Level:** Primary Function

**Preconditions:** The program is running on at least one computer, the user has a hash in one of the supported formats ready to be cracked. The user has files for specific methods of cracking (a dictionary file and/or rainbow table).

**Success End Condition:** The hash will have been found and the user will have the original text used to create it.

**Failed End Condition:** The hash will not have been found.

**Primary Actor:** User, the person operating the software.

**Trigger:** The program is started.

###MAIN SUCCESS SCENARIO

*put here the steps of the scenario from trigger to goal delivery, and any cleanup after*

1. User starts the program.

2. User inputs hash and selects cracking method.

3. User tells program to start cracking.

4. Program requests location of support files as needed.

5. Program finds the text which generated the user's hash.

###EXTENSIONS

*put here there extensions, one at a time, each referring to the step of the main scenario*

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
  + 4a1. Program requests hash type.
* 4b. User has selected dictionary cracking
  + 4b1. Program requests dictionary file.
  + 4b2. program request hash type.
  + 4b3. If no file is available, program cannot continue.
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


* 1a. User may select program mode
Single Computer, 
Node, 
Server


* 2a. User may choose cracking method
brute force, 
dictionary, 
rainbow table

 


###RELATED INFORMATION (optional)

**Priority:** Necessary for hash cracking.

**Performance Target:** Time scales range from miliseconds to years, depending on available computing power.

**Frequency:** Each time the user has a hash they wish to crack.

**Channel to primary actor:** Interactive GUI or CLI.

**Secondary Actors:** A system in server mode requires one or more computers in Node mode. Computers in Node mode require a computer in Server mode.

###OPEN ISSUES (optional)
* Rainbow table generator may run independently.
* Additional modes may be implemented including running multiple modes simultaneously on separate clients.
* 
###SCHEDULE

**Due Date:** March 2015