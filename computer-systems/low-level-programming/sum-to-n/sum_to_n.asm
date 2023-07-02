section .text
global sum_to_n

sum_to_n:
  xor eax, eax
  jmp sum

sum:
  add eax, edi
  sub edi, 1
  cmp edi, 0
  jg sum 
	ret
