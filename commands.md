### DJANGO AXES

```sh
python manage.py axes_reset
``` 
will reset all lockouts and access records.

```sh
python manage.py axes_reset_ip [ip ...] 
``` 
will clear lockouts and records for the given IP addresses.

```sh
python manage.py axes_reset_username [username ...]
```
will clear lockouts and records for the given usernames.

```sh
python manage.py axes_reset_ip_username [ip] [username] 
```
will clear lockouts and records for the given IP address and username.

```sh
python manage.py axes_reset_logs 
```
(age) will reset (i.e. delete) AccessLog records that are older than the given age where the default is 30 days.


### AUDIT HISTORY
```sh
python manage.py populate_history --auto
```
generate an initial change for preexisting model instances