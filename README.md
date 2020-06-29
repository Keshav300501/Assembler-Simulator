# Assembler-Simulator
Assembler simulator made in python


Input
*****
Input the path and name of the text file containg the assembly code and the name and path of output file
where the machine code will be stored.

Output
******
Text file containg the machine code for the input assembly code.

Pass 1
******
In pass 1 the following functions are being performed

	1. Reading the text file containg the assembly language code
	2. Creating Literal Table, Variable Table, Label Table and OpCode Table
	3. Error checking in syntax and declaration of variables literals and Labels
	4. Creation of an error stack in order of errors that are appearing
	5. Checking for comments and omitting it in the machine language code

Methodology:
	
	1. The text file is read line by line
	2. Each line is initally checked for comments
	3. Then each line is documented in Instruction Table with appropriate errors in error stack
	4. Variables are appended in variable table and literals are appended in literal tables
	5. The code includes forward referencing of variables and literals


Pass 2
******
In pass 2 the following functions are being performed

	1. If there are errors, then those are reported on console and printed in output file
	2. If there are no errors then the assembly code in the input file is convented into machine code in the output file

Methodology:

	1. Error Stack is checked for errors
	2. Then input file is read again in accordance with instruction table and converted into machine code


Errors Reported:
****************
The following errors is reported in the program

	1. If the Label is found after the end statement
	2. Multiple declaration of label
	3. Label name same as opcode name/variable name/literal name
	4. Multiple declaration of variable
	5. Varaible name same as opcode/literal/label
	6. Multiple declaration of literal
	7. Literal name same as opcode name/variable name/label name
	8. If variable/literal/label is used but not declared
	9. If there is syntactical error in declartion of label/variable/literal
	10. If the operand name is invalid
	11. If the operand required is missing
	12. If the STP statement is missing


Assumption: 
			1. All operands are declared at the end of instructions, sequentially and in order of their appearance in the code.
			2. Addressing starts from 00000000
			3. Variables are declared using DS
			4. Literals are declared using DC
			5. Every variable and literal occupies 4 bits

***************************************************************************************************************************************************************
