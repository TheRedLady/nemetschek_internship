1. Create a shell script that will tell you all the files that are currently
opened on the machine and it will give the output in the following format:
  command0 || file0
  command0 || file1
  command0 || file2
  command1 || file0

Hint: read about the /proc filesystem

2. Write a bash script which will rotate logs. The idea is simple, in one
directory you have a few logs - access.log, error.log and system.log, you need
to create a script that on each of its runs will rename each of the logs to
LOG.1 and then gzip the file(LOG is the name of the log that is beeing renamed).
If there is already LOG.1.gz then the file should be renamed to LOG.2.gz and so
on. You need to keep max of 12 copies of the logs.

3. Write a bash script that will output only the unique numbers in a file that
is with the following format:
  word | number
Be aware that the numbers in the file may or may not be ordered.

Ex.:

hello | 1
world | 2
hello | 4
hi | 1
buy | 3

output:

1
2
4
3

4. Write a bash script which will parse a text file with the following format:
64.31.49.26|2013-07-24-06:51:01|Blocked by pesho
108.171.243.146|2013-07-24-08:17:01|Blocked by niki
183.13.241.95|2013-07-24-11:51:00|Blocked by mm
183.240.177.169|2013-07-24-11:51:01|Blocked by joro
112.111.172.106|2013-07-24-13:00:00|Blocked by toni
220.113.166.194|2013-07-24-13:00:01|Blocked by pesho
82.59.74.82|2013-07-24-13:51:00|Blocked by pesho
103.6.237.126|2013-07-24-16:51:00|Blocked by misho
111.250.97.231|2013-07-24-18:34:00|Blocked by lubo
209.208.27.41|2013-07-24-18:34:00|Blocked by vlado
201.184.44.184|2013-07-24-18:51:01|Blocked by joro
79.19.133.36|2013-07-24-20:00:00|Blocked by toni

The script has to output only the lines that have dates older then 14 days.
Sort the output by date. 

5. Configure your command prompt in such a way, that you will always see the
current temperature.  You can use curl, sed, jq and the services
http://openweathermap.org/api and http://whatismycountry.com/.

6. Create a bash template engine script.

The script accepts:
    - bash scripts (one or more) with variable definitions (-v)
    - optionally template file (-t); if not given, read from stdin
    - optionnaly extra vars string (-e) in the format (var=val var=val ...);
      extra vars override variables from the file provided
    - optionally output file name (-o); if not given write to stdout

Ex:

$ ./render.sh -t somefile.tmpl -v vars.sh -o output

somefile.tmpl:
Hello <name>!

vars.sh:
name='world'

output:
Hello world!

---

### Useful resources:

http://www.tldp.org/
http://stedolan.github.io/jq/manual/
http://httpkit.com/resources/HTTP-from-the-Command-Line/
https://en.wikipedia.org/wiki/List_of_Unix_commands
http://www.grymoire.com/Unix/Sed.html
