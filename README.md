## About

This is Light weight mail notifier written in PyQt5. It checks your mailbox periodically and notify you if you have new mail.

## Screenshots
![MailboxEmpty](https://raw.github.com/rinaldus/mail-notify/master/screenshots/screen1.jpg)
![MailboxFull](https://raw.github.com/rinaldus/mail-notify/master/screenshots/screen2.jpg)
![Settings](https://raw.github.com/rinaldus/mail-notify/master/screenshots/screen3.jpg)

## Install

You need to install PyQt5 as dependency. Then just clone this git repository or download release and copy all files where you want to store this program. No additional installation is required.  
*In version 0.10 you also need to edit mail-notifier.py and fill your mailbox credentials in 70-72 rows*

## Launch

Give execute permission to mail-notifier.py
```sh
$ chmod +x mail-notifier.py
```

## Changelog
### Version 1.0 (release date: 01.11.15)
* Settings window
* All parameters are stored in configuration file *(~/.config/mail-notifier/settings.conf)*
* Many improvements

### Version 0.10 (pre release date: 28.10.15)
* Initial version
* All parameters are stored right in script

## Todo
* "About program" window
