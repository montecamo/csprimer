section .text
global sum_to_n

sum_to_n:
  mov eax, edi
  inc eax
  mul edi
  mov ecx, 2
  div ecx
  ret
