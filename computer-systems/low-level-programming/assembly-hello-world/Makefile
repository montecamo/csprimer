compile:
	nasm -f macho64 program.asm 

link:
	ld -macosx_version_min 12.6.0 -L/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/lib -lSystem program.o

start: compile link
	./a.out

clean:
	rm program.o
	rm a.out
