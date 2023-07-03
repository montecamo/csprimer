section .text
global index
index:
	; rdi: matrix
	; esi: rows
	; edx: cols
	; ecx: rindex
	; r8d: cindex
  mov rax, rdx
  mul rcx
  add eax, r8d
  mov rax, [rdi+rax*4]
	ret
