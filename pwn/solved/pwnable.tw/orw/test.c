#include <stdio.h>
/* #include <string.h> */
/* #include <unistd.h> */
#include <fcntl.h>

int main(){
  int fd = 0;
  char buf[20];

  fd = open("/home/yyy/flag", O_RDONLY);
  read(fd, &buf, 10);
  write(1, &buf, 10);

  close(fd);

  return 0;
}
