/* mdMonitor.c
 * This c daemon is to monitor when minecraftPi is on, ensuring the
 * modLoader python script is running when 
 *
 */

#include <stdio.h>
#include <string.h>//memset
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <syslog.h>


static void daemonize(){
  pid_t pid;

  /* Fork off the parent process */
  pid = fork();

  /* An error occurred */
  if (pid < 0)
    exit(EXIT_FAILURE);

  /* Success: Let the parent terminate */
  if (pid > 0)
    exit(EXIT_SUCCESS);

  /* On success: The child process becomes session leader */
  if (setsid() < 0)
    exit(EXIT_FAILURE);

  /* Fork off for the second time*/
  pid = fork();

  /* An error occurred */
  if (pid < 0)
    exit(EXIT_FAILURE);

  /* Success: Let the parent terminate */
  if (pid > 0)
    exit(EXIT_SUCCESS);

  /* Set new file permissions */
  umask(0);

  /* Change the working directory to the root directory */
  /* or another appropriated directory */
  chdir("/");

  /* Close all open file descriptors */
  int x;
  for (x = sysconf(_SC_OPEN_MAX); x>0; x--)
  {
    close (x);
  }

}

int main(){
  FILE * fp;
  FILE * fpMC;
  char buffer[BUFSIZ];
    daemonize();

  while(1){
    //daemon code here
    fp = popen("ps -elaf | grep 'minecraftModChooser.py' | grep -v grep", "r");//mod chooser running
    fpMC = popen("ps -elaf | grep minecraft-pi | grep -v bin | grep -v grep", "r");//minecraft running

    //begin check for minecraft pi running
    fgets(buffer, sizeof(buffer) - 1, fpMC);//buffer has minecraft process
    if(strcmp(buffer, "")){ //if minecraft-pi is running
      //clear buffer
      memset((void *)buffer, '\0', sizeof(buffer));

      //begin check for mod chooser running
      fgets(buffer, sizeof(buffer) - 1,fp);//buffer has modchooser process
      if(!strcmp(buffer, "")){ //if modChooser not running
        system("python /home/pi/minecraftModChooser/minecraftModChooser.py &");
      }
      //clear buffer
      memset((void *)buffer, '\0', sizeof(buffer));
    }
    else{
      //clear buffer
      memset((void *)buffer, '\0', sizeof(buffer));
      fgets(buffer, sizeof(buffer) - 1,fp);//buffer has modchooser process
      if(strcmp(buffer, "")){ //if modChooser is running and mi-pi not running
        //kill modchooser
        system("killall python");

      }
      //clear buffer
      memset((void *)buffer, '\0', sizeof(buffer));

    }
    sleep(2);

  }
  return EXIT_SUCCESS;
}
