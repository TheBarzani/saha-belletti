OPENQASM 3;
include "stdgates.inc";
bit[3] _creg;
qubit[6] q57;
h q57[0];
h q57[1];
h q57[2];
x q57[5];
h q57[5];
x q57[3];
x q57[4];
cx q57[0], q57[1];
x q57[1];
cx q57[1], q57[3];
x q57[1];
cx q57[0], q57[1];
cx q57[1], q57[2];
x q57[2];
cx q57[2], q57[4];
x q57[2];
cx q57[1], q57[2];
ccx q57[3], q57[4], q57[5];
cx q57[1], q57[2];
x q57[2];
cx q57[2], q57[4];
x q57[2];
cx q57[1], q57[2];
cx q57[0], q57[1];
x q57[1];
cx q57[1], q57[3];
x q57[1];
cx q57[0], q57[1];
h q57[0];
x q57[0];
h q57[1];
x q57[1];
z q57[2];
ccx q57[0], q57[1], q57[2];
z q57[2];
x q57[0];
h q57[0];
x q57[1];
h q57[1];
_creg[0] = measure q57[0];
_creg[1] = measure q57[1];
_creg[2] = measure q57[2];
