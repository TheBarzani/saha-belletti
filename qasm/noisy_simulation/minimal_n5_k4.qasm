OPENQASM 2.0;
include "qelib1.inc";
gate mcx q0,q1,q2,q3 { h q3; p(pi/8) q0; p(pi/8) q1; p(pi/8) q2; p(pi/8) q3; cx q0,q1; p(-pi/8) q1; cx q0,q1; cx q1,q2; p(-pi/8) q2; cx q0,q2; p(pi/8) q2; cx q1,q2; p(-pi/8) q2; cx q0,q2; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q1,q3; p(pi/8) q3; cx q2,q3; p(-pi/8) q3; cx q0,q3; h q3; }
gate mcu1(param0) q0,q1,q2,q3,q4,q5,q6,q7,q8,q9 { cu1(pi/256) q8,q9; cx q8,q7; cu1(-pi/256) q7,q9; cx q8,q7; cu1(pi/256) q7,q9; cx q7,q6; cu1(-pi/256) q6,q9; cx q8,q6; cu1(pi/256) q6,q9; cx q7,q6; cu1(-pi/256) q6,q9; cx q8,q6; cu1(pi/256) q6,q9; cx q6,q5; cu1(-pi/256) q5,q9; cx q8,q5; cu1(pi/256) q5,q9; cx q7,q5; cu1(-pi/256) q5,q9; cx q8,q5; cu1(pi/256) q5,q9; cx q6,q5; cu1(-pi/256) q5,q9; cx q8,q5; cu1(pi/256) q5,q9; cx q7,q5; cu1(-pi/256) q5,q9; cx q8,q5; cu1(pi/256) q5,q9; cx q5,q4; cu1(-pi/256) q4,q9; cx q8,q4; cu1(pi/256) q4,q9; cx q7,q4; cu1(-pi/256) q4,q9; cx q8,q4; cu1(pi/256) q4,q9; cx q6,q4; cu1(-pi/256) q4,q9; cx q8,q4; cu1(pi/256) q4,q9; cx q7,q4; cu1(-pi/256) q4,q9; cx q8,q4; cu1(pi/256) q4,q9; cx q5,q4; cu1(-pi/256) q4,q9; cx q8,q4; cu1(pi/256) q4,q9; cx q7,q4; cu1(-pi/256) q4,q9; cx q8,q4; cu1(pi/256) q4,q9; cx q6,q4; cu1(-pi/256) q4,q9; cx q8,q4; cu1(pi/256) q4,q9; cx q7,q4; cu1(-pi/256) q4,q9; cx q8,q4; cu1(pi/256) q4,q9; cx q4,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q7,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q6,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q7,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q5,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q7,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q6,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q7,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q4,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q7,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q6,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q7,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q5,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q7,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q6,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q7,q3; cu1(-pi/256) q3,q9; cx q8,q3; cu1(pi/256) q3,q9; cx q3,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q6,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q5,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q6,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q4,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q6,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q5,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q6,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q3,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q6,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q5,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q6,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q4,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q6,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q5,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q6,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q7,q2; cu1(-pi/256) q2,q9; cx q8,q2; cu1(pi/256) q2,q9; cx q2,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q5,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q4,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q5,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q3,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q5,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q4,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q5,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q2,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q5,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q4,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q5,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q3,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q5,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q4,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q5,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q6,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q7,q1; cu1(-pi/256) q1,q9; cx q8,q1; cu1(pi/256) q1,q9; cx q1,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q4,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q3,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q4,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q2,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q4,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q3,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q4,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q1,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q4,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q3,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q4,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q2,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q4,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q3,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q4,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q5,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q6,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; cx q7,q0; cu1(-pi/256) q0,q9; cx q8,q0; cu1(pi/256) q0,q9; }
gate mcx_gray q0,q1,q2,q3,q4,q5,q6,q7,q8,q9 { h q9; mcu1(pi) q0,q1,q2,q3,q4,q5,q6,q7,q8,q9; h q9; }
qreg q13[15];
creg reg_creg[10];
h q13[0];
h q13[1];
h q13[2];
h q13[3];
h q13[4];
h q13[5];
h q13[6];
h q13[7];
h q13[8];
h q13[9];
x q13[14];
h q13[14];
x q13[10];
x q13[11];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[6],q13[8];
x q13[8];
cx q13[7],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[7],q13[9];
x q13[8];
cx q13[6],q13[8];
cx q13[2],q13[8];
x q13[8];
cx q13[3],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[10];
x q13[9];
cx q13[3],q13[9];
x q13[8];
cx q13[2],q13[8];
mcx q13[10],q13[11],q13[12],q13[13];
cx q13[2],q13[8];
x q13[8];
cx q13[3],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[10];
x q13[9];
cx q13[3],q13[9];
x q13[8];
cx q13[2],q13[8];
cx q13[6],q13[8];
x q13[8];
cx q13[7],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[7],q13[9];
x q13[8];
cx q13[6],q13[8];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[4],q13[6];
x q13[6];
cx q13[5],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[11];
x q13[7];
cx q13[5],q13[7];
x q13[6];
cx q13[4],q13[6];
cx q13[2],q13[6];
x q13[6];
cx q13[3],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[10];
x q13[7];
cx q13[3],q13[7];
x q13[6];
cx q13[2],q13[6];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[6];
x q13[6];
cx q13[3],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[10];
x q13[7];
cx q13[3],q13[7];
x q13[6];
cx q13[2],q13[6];
cx q13[4],q13[6];
x q13[6];
cx q13[5],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[11];
x q13[7];
cx q13[5],q13[7];
x q13[6];
cx q13[4],q13[6];
cx q13[4],q13[8];
x q13[8];
cx q13[5],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[5],q13[9];
x q13[8];
cx q13[4],q13[8];
mcx q13[13],q13[12],q13[11],q13[14];
cx q13[4],q13[8];
x q13[8];
cx q13[5],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[5],q13[9];
x q13[8];
cx q13[4],q13[8];
cx q13[4],q13[6];
x q13[6];
cx q13[5],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[11];
x q13[7];
cx q13[5],q13[7];
x q13[6];
cx q13[4],q13[6];
cx q13[2],q13[6];
x q13[6];
cx q13[3],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[10];
x q13[7];
cx q13[3],q13[7];
x q13[6];
cx q13[2],q13[6];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[6];
x q13[6];
cx q13[3],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[10];
x q13[7];
cx q13[3],q13[7];
x q13[6];
cx q13[2],q13[6];
cx q13[4],q13[6];
x q13[6];
cx q13[5],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[11];
x q13[7];
cx q13[5],q13[7];
x q13[6];
cx q13[4],q13[6];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[6],q13[8];
x q13[8];
cx q13[7],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[7],q13[9];
x q13[8];
cx q13[6],q13[8];
cx q13[2],q13[8];
x q13[8];
cx q13[3],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[10];
x q13[9];
cx q13[3],q13[9];
x q13[8];
cx q13[2],q13[8];
mcx q13[10],q13[11],q13[12],q13[13];
cx q13[2],q13[8];
x q13[8];
cx q13[3],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[10];
x q13[9];
cx q13[3],q13[9];
x q13[8];
cx q13[2],q13[8];
cx q13[6],q13[8];
x q13[8];
cx q13[7],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[7],q13[9];
x q13[8];
cx q13[6],q13[8];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
h q13[0];
x q13[0];
h q13[1];
x q13[1];
h q13[2];
x q13[2];
h q13[3];
x q13[3];
h q13[4];
x q13[4];
h q13[5];
x q13[5];
h q13[6];
x q13[6];
h q13[7];
x q13[7];
h q13[8];
x q13[8];
z q13[9];
mcx_gray q13[0],q13[1],q13[2],q13[3],q13[4],q13[5],q13[6],q13[7],q13[8],q13[9];
z q13[9];
x q13[0];
h q13[0];
x q13[1];
h q13[1];
x q13[2];
h q13[2];
x q13[3];
h q13[3];
x q13[4];
h q13[4];
x q13[5];
h q13[5];
x q13[6];
h q13[6];
x q13[7];
h q13[7];
x q13[8];
h q13[8];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[6],q13[8];
x q13[8];
cx q13[7],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[7],q13[9];
x q13[8];
cx q13[6],q13[8];
cx q13[2],q13[8];
x q13[8];
cx q13[3],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[10];
x q13[9];
cx q13[3],q13[9];
x q13[8];
cx q13[2],q13[8];
mcx q13[10],q13[11],q13[12],q13[13];
cx q13[2],q13[8];
x q13[8];
cx q13[3],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[10];
x q13[9];
cx q13[3],q13[9];
x q13[8];
cx q13[2],q13[8];
cx q13[6],q13[8];
x q13[8];
cx q13[7],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[7],q13[9];
x q13[8];
cx q13[6],q13[8];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[4],q13[6];
x q13[6];
cx q13[5],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[11];
x q13[7];
cx q13[5],q13[7];
x q13[6];
cx q13[4],q13[6];
cx q13[2],q13[6];
x q13[6];
cx q13[3],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[10];
x q13[7];
cx q13[3],q13[7];
x q13[6];
cx q13[2],q13[6];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[6];
x q13[6];
cx q13[3],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[10];
x q13[7];
cx q13[3],q13[7];
x q13[6];
cx q13[2],q13[6];
cx q13[4],q13[6];
x q13[6];
cx q13[5],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[11];
x q13[7];
cx q13[5],q13[7];
x q13[6];
cx q13[4],q13[6];
cx q13[4],q13[8];
x q13[8];
cx q13[5],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[5],q13[9];
x q13[8];
cx q13[4],q13[8];
mcx q13[13],q13[12],q13[11],q13[14];
cx q13[4],q13[8];
x q13[8];
cx q13[5],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[5],q13[9];
x q13[8];
cx q13[4],q13[8];
cx q13[4],q13[6];
x q13[6];
cx q13[5],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[11];
x q13[7];
cx q13[5],q13[7];
x q13[6];
cx q13[4],q13[6];
cx q13[2],q13[6];
x q13[6];
cx q13[3],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[10];
x q13[7];
cx q13[3],q13[7];
x q13[6];
cx q13[2],q13[6];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[6];
x q13[6];
cx q13[3],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[10];
x q13[7];
cx q13[3],q13[7];
x q13[6];
cx q13[2],q13[6];
cx q13[4],q13[6];
x q13[6];
cx q13[5],q13[7];
x q13[7];
ccx q13[6],q13[7],q13[11];
x q13[7];
cx q13[5],q13[7];
x q13[6];
cx q13[4],q13[6];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[6],q13[8];
x q13[8];
cx q13[7],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[7],q13[9];
x q13[8];
cx q13[6],q13[8];
cx q13[2],q13[8];
x q13[8];
cx q13[3],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[10];
x q13[9];
cx q13[3],q13[9];
x q13[8];
cx q13[2],q13[8];
mcx q13[10],q13[11],q13[12],q13[13];
cx q13[2],q13[8];
x q13[8];
cx q13[3],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[10];
x q13[9];
cx q13[3],q13[9];
x q13[8];
cx q13[2],q13[8];
cx q13[6],q13[8];
x q13[8];
cx q13[7],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[7],q13[9];
x q13[8];
cx q13[6],q13[8];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
ccx q13[10],q13[11],q13[12];
cx q13[2],q13[4];
x q13[4];
cx q13[3],q13[5];
x q13[5];
ccx q13[4],q13[5],q13[10];
x q13[5];
cx q13[3],q13[5];
x q13[4];
cx q13[2],q13[4];
cx q13[0],q13[8];
x q13[8];
cx q13[1],q13[9];
x q13[9];
ccx q13[8],q13[9],q13[11];
x q13[9];
cx q13[1],q13[9];
x q13[8];
cx q13[0],q13[8];
h q13[0];
x q13[0];
h q13[1];
x q13[1];
h q13[2];
x q13[2];
h q13[3];
x q13[3];
h q13[4];
x q13[4];
h q13[5];
x q13[5];
h q13[6];
x q13[6];
h q13[7];
x q13[7];
h q13[8];
x q13[8];
z q13[9];
mcx_gray q13[0],q13[1],q13[2],q13[3],q13[4],q13[5],q13[6],q13[7],q13[8],q13[9];
z q13[9];
x q13[0];
h q13[0];
x q13[1];
h q13[1];
x q13[2];
h q13[2];
x q13[3];
h q13[3];
x q13[4];
h q13[4];
x q13[5];
h q13[5];
x q13[6];
h q13[6];
x q13[7];
h q13[7];
x q13[8];
h q13[8];
measure q13[0] -> reg_creg[0];
measure q13[1] -> reg_creg[1];
measure q13[2] -> reg_creg[2];
measure q13[3] -> reg_creg[3];
measure q13[4] -> reg_creg[4];
measure q13[5] -> reg_creg[5];
measure q13[6] -> reg_creg[6];
measure q13[7] -> reg_creg[7];
measure q13[8] -> reg_creg[8];
measure q13[9] -> reg_creg[9];

