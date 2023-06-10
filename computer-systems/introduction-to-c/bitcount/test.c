#include <assert.h>
#include <stdint.h>
#include <stdio.h>

int bitcount(uint32_t num) {
  int count = 0;

  for (int i = 0; i < 32; i++) {
    count += (num >> i) & 1;
  }

  return count;
}

int main() {
  assert(bitcount(0) == 0);
  assert(bitcount(1) == 1);
  assert(bitcount(3) == 2);
  assert(bitcount(8) == 1);
  assert(bitcount(0xffffffff) == 32);

  printf("OK\n");
}
