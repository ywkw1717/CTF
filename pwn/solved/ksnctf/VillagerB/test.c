#include <stdio.h>
#include <fcntl.h>

int main(){
  int fd;
  char buff[10];
  int rc;

  fd = open("hoge.txt", O_RDONLY);

  if (fd == -1)
  {
    printf("ファイルオープンエラー\n");
    return;
  }
  rc = read(fd, buff, 100);
  if (rc == -1)
  {
    printf("ファイル読み込みエラー\n");
  }
  else
  {
    buff[rc] = '\0';
    printf("read:%d - %s\n", rc, buff);
  }
  close(fd);
  return 0;
}
