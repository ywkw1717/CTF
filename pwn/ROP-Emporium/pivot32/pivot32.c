#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void pwnme(char *str){
  char buf[28];
  memset(buf, 0, 32);

  puts("Call ret2win() from libpivot.so");
  printf("The Old Gods kindly bestow upon you a place to pivot: %p\n", str);

  puts("Send your second chain now and it will land there");
  printf("> ");

  fgets(str, 256, stdin);
  puts("Now kindly send your stack smash");
  printf("> ");

  fgets(buf, 58, stdin);
}

int main(){
  char *hoge;
  char *str;

  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);

  puts("pivot by ROP Emporium");
  puts("32bits\n");

  str = (char *)malloc(0x1000000);
  hoge = str;
  pwnme(hoge);

  hoge = NULL;
  free(str);

  puts("\nExiting");

  return 0;
}
