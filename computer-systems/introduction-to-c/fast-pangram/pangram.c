#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

bool ispangram(char *s) {
  int32_t alphabet = 0;
  char letter = '\0';

  while ((letter = tolower(*s++)) != '\0') {
    if (97 <= letter && letter <= 122) {
      alphabet |= 1 << (letter - 97);
    }
  }

  return alphabet == 0x3ffffff;
}

int main() {
  size_t len;
  ssize_t read;
  char *line = NULL;
  while ((read = getline(&line, &len, stdin)) != -1) {
    if (ispangram(line))
      printf("%s", line);
  }

  if (ferror(stdin))
    fprintf(stderr, "Error reading from stdin");

  free(line);
  fprintf(stderr, "ok\n");
}
