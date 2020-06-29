import pdb

#Label class used to store contents of a label
class Label:
	def __init__(self,p_LabelName,p_LabelAddress):
		self.m_Name=p_LabelName
		self.m_Address=str(p_LabelAddress)

	def printLabel(self):
		print(str(self.m_Name)+"   "+str(self.m_Address))

LabelTable=[] #Label table stores all the declared Labels


#Variable class used to store parameters for variable
class Variable:
	def __init__(self,p_VariableName,p_Address,p_Value):
		self.m_VariableName=p_VariableName
		self.m_VarAddress=p_Address
		self.m_VarValue=str(p_Value)

	def printVariable(self):
		print(str(self.m_VariableName) +"  "+ str(self.m_VarAddress) +"  "+ str(self.m_VarValue))

VariableTable=[] #Variable table used to store all the variables that are declared

#Literal class used to store parameters for literals
class Literal:
	def __init__(self,name,address,value):
		self.m_LitName=name
		self.m_LitAddress=address
		self.m_LitValue=value

	def printLiteral(self):
		print(str(self.m_LitName)+"  "+str(self.m_LitAddress)+"  "+str(self.m_LitValue))

LiteralTable=[] #Literal table used to store all the declared literals

#OpCode class used to store used opcodes in the program
class OpCode:
	def __init__(self,p_OpCode,p_OpCodeName,p_Operand,p_Address,p_LineNum):
		self.m_OpCode=p_OpCode
		self.m_OpCodeName=p_OpCodeName
		self.m_Operand=p_Operand
		self.m_Address=p_Address
		self.m_LineNum=p_LineNum

OpCodeTable=[] #store all the opcode used in the program

def printOpCodeTable():
	for val in OpCodeTable:
		print(val.m_OpCode+"  "+val.m_OpCodeName+"  "+val.m_Operand+"  "+val.m_Address+"  "+val.m_LineNum)


#dictionary to store all the give opcodes Key: opCode name Value:OpCode
MOTTable={}
MOTTable["CLA"]="0000"
MOTTable["LAC"]="0001"
MOTTable["SAC"]="0010"
MOTTable["ADD"]="0011"
MOTTable["SUB"]="0100"
MOTTable["BRZ"]="0101"
MOTTable["BRN"]="0110"
MOTTable["BRP"]="0111"
MOTTable["INP"]="1000"
MOTTable["DSP"]="1001"
MOTTable["MUL"]="1010"
MOTTable["DIV"]="1011"
MOTTable["STP"]="1100"

LineNumber=0 #stores the line count for error reporting
LocationCounter=0
ErrorStack=[] #used to store all the errors and then report it in the end
LogStack=[] #Log all the activity and create a log report at the end of program
foundEnd=False #check if the end is received: yes->True no->False

#utility function to get address of Label/Variable/Literal
def getLabelAddress(tmpStr):
	for tmp in LabelTable:
		if(tmpStr == tmp.m_Name):
			return tmp.m_Address
	return -1

def getVariableAddress(tmpStr):
	for tmp in VariableTable:
		if(tmpStr == tmp.m_VariableName):
			return tmp.m_VarAddress
	return -1

def getLiteralAddress(tmpStr):
	for tmp in LiteralTable:
		if(tmpStr == tmp.m_LitName):
			return tmp.m_LitAddress
	return -1


#utility functions for external checking
def checkIsStart(tmpStr):
	if(tmpStr == "START"):
		return True
	return False

def checkIsOperandRequired(tmpStr):
	if(tmpStr == "CLA" or tmpStr == "STP"):
		return False
	return True

def checkBranchStatement(tmpStr):
	if(tmpStr[:-1] == "BR"):
		return True
	return False

def checkIsVariableDeclared(tmpStr):
	if(tmpStr == "DS"):
		return True
	return False

def getLiteralVal(tmpStr):
	if("=" not in tmpStr):
		ErrorStack.append("Invalid declaration of literal")
		return False
	else:
		return True,tmpStr.split("=")

#function to generate 8 bit address for an instruction
def generateAddress():
	tmpAddress=str(bin(LocationCounter)[2:])
	tmpLen=len(tmpAddress)
	finalAddress=('0'*(8-tmpLen))+tmpAddress
	return finalAddress

#utility functions to check if there is duplicacy and for error checking during forward referencing
def checkVariableRepeate(tmpStr):
	for var in VariableTable:
		if(var.m_VariableName == tmpStr) :
			return True
	return False

def checkLabelRepeate(tmpStr):
	for lbl in LabelTable:
		if(lbl.m_Name == tmpStr):
			return True
	return False

def checkLiteralRepeate(tmpStr):
	for lit in LiteralTable:
		if(lit.m_LitName == tmpStr):
			return True
	return False



#functions for label Table
def printLabelTable():
	for tmp in LabelTable:
		tmp.printLabel()


def checkLabel(tmpStr):
	global LocationCounter,foundEnd	
	if(tmpStr[-1] == ":"):
		tmpStr = tmpStr[:-1]
		if(foundEnd == True):
			ErrorStack.append("The Label is found after the end. Line-> "+str(LineNumber))
			return False
		if(checkLabelRepeate(tmpStr) == True):
			#print("inside if of Label")
			ErrorStack.append("Same Label Declaration Found. Line-> "+str(LineNumber)+" of the Label "+tmpStr)
			LocationCounter=LocationCounter-12
			return False
		elif(tmpStr in MOTTable.keys()):
			ErrorStack.append("Label of Same name as opcode. Line-> "+str(LineNumber)+" of the Label "+tmpStr)
			LocationCounter=LocationCounter-12
			return False
		elif(checkVariableRepeate(tmpStr) == True):
			ErrorStack.append("Label name same as variable name. Line-> "+str(LineNumber))
			LocationCounter=LocationCounter-12
			return False
		elif(checkLiteralRepeate(tmpStr) == True):
			ErrorStack.append("Label name same as Literal name. Line-> "+str(LineNumber))
			LocationCounter=LocationCounter-12
			return False
		else:
			LabelTable.append(Label(tmpStr,generateAddress()))
			return True



#function for variable table
def printVariableTable():
	for var in VariableTable:
		var.printVariable()

def setVariableTable(tmpStr,tmpVal,tmpAddress):
	if(checkVariableRepeate(tmpStr) == True):
		ErrorStack.append("Multiple Declaration Error: variable "+str(tmpStr)+" is declared again. Line-> "+str(LineNumber))
		return False
	elif(tmpStr in MOTTable.keys()):
		ErrorStack.append("Variable name same as opCode name. Line-> "+str(LineNumber))
		return False
	elif(checkLabelRepeate(tmpStr)==True):
		ErrorStack.append("Variable name same as label name. Line-> "+str(LineNumber))
		return False
	elif(checkLiteralRepeate(tmpStr) == True):
		ErrorStack.append("Variable name same as literal name. Line-> "+str(LineNumber))
		return False
	else:
		VariableTable.append(Variable(tmpStr,tmpAddress,tmpVal))
		return True


#function for literal table
def printLiteralTable():
	for lit in LiteralTable:
		lit.printLiteral()

def setLiteralTable(tmpStr,tmpAddress,tmpVal):
	if(checkLiteralRepeate(tmpStr) == True):
		ErrorStack.append("Multiple Declartation Error: literal "+str(tmpStr)+" is declared again. Line-> "+str(LineNumber))
		return False
	elif(tmpStr in MOTTable.keys()):
		ErrorStack.append("Literal name same as opCode name.Line-> "+str(LineNumber))
		return False
	elif(checkVariableRepeate(tmpStr) == True):
		ErrorStack.append("Literal name same as variable name. Line-> "+str(LineNumber))
		return False
	elif(checkLabelRepeate(tmpStr) == True):
		ErrorStack.append("Literal name same as Label name. Line-> "+str(LineNumber))
		return False
	else:
		LiteralTable.append(Literal(tmpStr,tmpAddress,tmpVal))
		return True


#function to check opCode table for errors
def checkTables():
	foundVariable=False
	foundLiteral=False

	for row in OpCodeTable:
		tmpOpCode=row
		tmpName=tmpOpCode.m_Operand
		tmpOperation=row.m_OpCodeName

		if(tmpOperation == "CLA"):
			continue

		if(checkBranchStatement(tmpOperation) == True):
			if(checkLabelRepeate(tmpName) == False):
				ErrorStack.append("Label "+tmpName +" not declared but used")
			else:
				continue
		else:

			if(checkVariableRepeate(tmpName) == True):
				foundVariable = True
			elif(checkLiteralRepeate(tmpName) == True):
				foundLiteral=True

			if(foundVariable == False and foundLiteral == False):
				ErrorStack.append("Variable "+tmpName+" used but not declared")
				continue
			else:
				continue


#function to check comments
def checkComment(String):
	if(String[0] == "/" and String[1]=='/'):
		return True
	return False

#function to read file and convert into list
def readFile(fileString):
	with open(fileString) as fileObj:
		data=fileObj.read()
		fileInput=data.split("\n")

	return fileInput


#function to check errors: calls checkTable() method
def checkErrors():
	global foundEnd
	if(foundEnd == False):
		ErrorStack.append("STP not found in the program")
	checkTables()


#Pass 1 of the 2 pass assembler
#create Variable,Literal,OpCode,Label Table
#checks errors
def Pass1(fileString):
	
	global LineNumber,LocationCounter,foundEnd
	Input=readFile(fileString)

	for line in Input:
		wordArr=line.split(" ")
		i=0

		if(wordArr[0] == "START"):
			LocationCounter=0;
			foundEnd=False
			LineNumber+=1
			continue

		if(wordArr [0] == "STP"):
			foundEnd=True
			LineNumber+=1
			continue

		if(wordArr[0] == "CLA"):
			OpCodeTable.append(OpCode("0000","CLA","",generateAddress(),str(LineNumber)))
			LocationCounter+=12
			LineNumber+=1
			continue

		while(i<len(wordArr)):
			if(checkComment(wordArr[i]) == True):
				LogStack.append("Found a comment in line: "+str(LineNumber))
				LocationCounter=LocationCounter-12
				LineNumber=LineNumber-1
				break


			#checking for a label
			if(checkLabel(wordArr[i]) == True):
				LogStack.append("Added a label to Label Table")

			#checking for an opCode and Variable or a literal corrosponding to it
			elif(wordArr[i] in MOTTable):
				
				if(foundEnd == False):
					bool=False
					bool=checkIsOperandRequired(wordArr[i])
					chkBranch=checkBranchStatement(wordArr[i])
					i+=1
					if(i < len(wordArr)):
						if((checkComment(wordArr[i]) == True) and bool == True and chkBranch == False):
							ErrorStack.append("no Operand found. Line-> "+str(LineNumber))
							LocationCounter=LocationCounter-12
							break

						elif(wordArr[i] in MOTTable.keys() and bool == True and chkBranch == False):
							ErrorStack.append("Invalid Operand name. Line-> "+str(LineNumber))
							LocationCounter=LocationCounter-12
							break

						elif(checkLabelRepeate(wordArr[i]) == True and bool == True and chkBranch == False):
							ErrorStack.append("Invalid Operand name; already declared as a label. Line-> "+str(LineNumber))
							LocationCounter=LocationCounter-12
							break

						elif(checkVariableRepeate(wordArr[i]) == True and bool == True and chkBranch == False):
							ErrorStack.append("Invalid Operand name;already declared as a variable. Line-> "+str(LineNumber))
							LocationCounter=LocationCounter-12
							break

						elif(checkLiteralRepeate(wordArr[i]) == True and bool == True and chkBranch == False):
							ErrorStack.append("Invalid Operand name; already declared as a Literal. Line-> "+str(LineNumber))
							LocationCounter=LocationCounter-12
							break

						else:
							OpCodeTable.append(OpCode(MOTTable[wordArr[i-1]],wordArr[i-1],wordArr[i],generateAddress(),str(LineNumber)))

					else:
						ErrorStack.append("Operand not found. Line-> "+ str(LineNumber))
						LocationCounter=LocationCounter-12
						break
				else:
					ErrorStack.append("Operation found after STP. Line-> "+str(LineNumber))
					LocationCounter=LocationCounter-12
					break


			elif(checkIsVariableDeclared(wordArr[i]) == True):

				if(i+1<len(wordArr)):
					i+=1
					tmpVar=wordArr[i]
					if(i+1<len(wordArr)):
						i+=1
						tmpVal=wordArr[i]
					else:
						tmpVal=str(0)

					if(LocationCounter!=0):
						LocationCounter=LocationCounter-12
					LocationCounter+=4
					if(setVariableTable(tmpVar,tmpVal,generateAddress()) == True):
						LogStack.append("setting variable in variable table")
						break
					else:
						LogStack.append("error setting variable table")
						LocationCounter=LocationCounter-4
						break

					
				else:
					ErrorStack.append("invalid declaration of variable. Line-> "+str(LineNumber))
					LogStack.append("error adding variable to Variable Table")
					LocationCounter=LocationCounter-12
					break

			elif(wordArr[i] == "DC"):
				i+=1
				if(LocationCounter!=0):
					LocationCounter=LocationCounter-12
				LocationCounter+=4
				bool,LitList=getLiteralVal(wordArr[i])
				if(bool == True):
					if(setLiteralTable(LitList[0],generateAddress(),LitList[1]) == True):
						LogStack.append("adding literal to literal table")
					else:
						LogStack.append("error adding literal to literal table")
						LocationCounter=LocationCounter-4
						break

			i+=1

		LocationCounter+=12
		LineNumber+=1

	checkErrors()


#function to print tables after pass 1
def printTables():

	print()
	print()

	print("LABEL TABLE")
	print()
	for line in LabelTable:
		print(str(line.m_Address)+"       "+str(line.m_Name))


	print()
	print()
	print()

	print("LITERAL TABLE")
	print()
	for line in LiteralTable:
		print(str(line.m_LitAddress)+"       "+str(line.m_LitName)+"        "+str(line.m_LitValue))

	print()
	print()
	print()

	print("SYMBOL TABLE")
	print()
	for line in LabelTable:
		print(str(line.m_Address)+"       "+str(line.m_Name)+"        "+str("Label")+"           "+str("-"))
	for line in VariableTable:
		print(str(line.m_VarAddress)+"        "+str(line.m_VariableName)+"        "+str("Variable")+"        "+str(line.m_VarValue))

	print()
	print()
	print()

	print("INSTRUCTION TABLE")
	print()
	for line in OpCodeTable:
		print(str(line.m_Address)+"        "+str(line.m_OpCode)+"        "+str(line.m_OpCodeName) +"        "+str(line.m_Operand))


#Pass 2 of 2 pass assembler
#If no error is found convert the program to machine code
#If errors are found report errors in a txt File
def Pass2(outputFile):
	if(len(ErrorStack) != 0):
		print("There are errors in the code.")
		print(len(ErrorStack))

		for line in ErrorStack:
			print(line)

		with open(outputFile,'w') as file:
			for line in ErrorStack:
				file.write(line)
				file.write('\n')

		return False
	file=open(outputFile,'w')

	for cmd in OpCodeTable:
		tmpOpCode=cmd
		file.write(tmpOpCode.m_Address+"    "+tmpOpCode.m_OpCode+"    ")
		if(tmpOpCode.m_OpCodeName == "CLA"):
			file.write('\n')
			continue

		if(checkBranchStatement(tmpOpCode.m_OpCodeName) == True):
			file.write(getLabelAddress(tmpOpCode.m_Operand))
			file.write('\n')

		else:
			tmp=getVariableAddress(tmpOpCode.m_Operand)
			if(tmp == -1):
				file.write(str(getLiteralAddress(tmpOpCode.m_Operand)))
				file.write('\n')
			else:
				file.write(tmp)
				file.write('\n')
		continue


print("enter the path and the file for input")
inputFile=input()
Pass1(str(inputFile))
printTables()
Pass2("Output.txt")