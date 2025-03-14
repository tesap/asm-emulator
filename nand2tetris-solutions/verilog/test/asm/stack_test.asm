// push constant 17
@17
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 17
@17
D=A
@SP
AM=M+1
A=A-1
M=D

// eq
@SP
AM=M-1
D=M
@R13
M=D
@SP
AM=M-1
D=M
@R13
D=D-M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@THEN0
D;JEQ
D=0
@ENDIF0
0;JMP
(THEN0)
D=-1
(ENDIF0)
@SP
AM=M+1
A=A-1
M=D

// push constant 892
@892
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 891
@891
D=A
@SP
AM=M+1
A=A-1
M=D

// lt
@SP
AM=M-1
D=M
@R13
M=D
@SP
AM=M-1
D=M
@R13
D=D-M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@THEN1
D;JLT
D=0
@ENDIF1
0;JMP
(THEN1)
D=-1
(ENDIF1)
@SP
AM=M+1
A=A-1
M=D

// push constant 32767
@32767
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 32766
@32766
D=A
@SP
AM=M+1
A=A-1
M=D

// gt
@SP
AM=M-1
D=M
@R13
M=D
@SP
AM=M-1
D=M
@R13
D=D-M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@THEN2
D;JGT
D=0
@ENDIF2
0;JMP
(THEN2)
D=-1
(ENDIF2)
@SP
AM=M+1
A=A-1
M=D

// push constant 56
@56
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 31
@31
D=A
@SP
AM=M+1
A=A-1
M=D

// push constant 53
@53
D=A
@SP
AM=M+1
A=A-1
M=D

// add
@SP
AM=M-1
D=M
@R13
M=D
@SP
AM=M-1
D=M
@R13
D=D+M
@SP
AM=M+1
A=A-1
M=D

// push constant 112
@112
D=A
@SP
AM=M+1
A=A-1
M=D

// sub
@SP
AM=M-1
D=M
@R13
M=D
@SP
AM=M-1
D=M
@R13
D=D-M
@SP
AM=M+1
A=A-1
M=D

// neg
@SP
AM=M-1
D=M
D=-D
@SP
AM=M+1
A=A-1
M=D

// and
@SP
AM=M-1
D=M
@R13
M=D
@SP
AM=M-1
D=M
@R13
D=D&M
@SP
AM=M+1
A=A-1
M=D

// push constant 82
@82
D=A
@SP
AM=M+1
A=A-1
M=D

// or
@SP
AM=M-1
D=M
@R13
M=D
@SP
AM=M-1
D=M
@R13
D=D|M
@SP
AM=M+1
A=A-1
M=D

