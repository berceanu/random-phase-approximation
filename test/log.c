#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
  int logTimes = atoi(argv[1]);

  for (int i = 0; i < logTimes; i++)  {
    fprintf(stdout, "%s %d.\n", "Hello stdout", i);
  }

  return 0;
}
