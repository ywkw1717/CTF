#include <stdio.h>
int main(){
  int key = 0xdeadbeef;
  char buf[1024];

  printf("key addres = %x\n", &key);
  fflush(stdout);

  fgets(buf, sizeof(buf), stdin);
  printf(buf); // FSB

  fflush(stdout);

  if(key == 0x12345678) {
    printf("Hacked");
    fflush(stdout);
  }
  return 0;
}
