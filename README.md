# Cloud Backup
## Backup your calendars and adressbook directly from the cloud! 


Thanks to [Tiktaktux-Wiki](https://www.tiktaktux.de/doku.php?id=linux:caldav_und_carddav_backup_erstellen) and [Henry Koch](https://www.henrykoch.de/de/python-loeschen-der-aeltesten-files-in-einem-verzeichnis-nur-die-neuesten-x-bleiben-zurueck) for important bases. ✨ 

Further a big thanks to [Cermit](https://twitter.com/Cermit3273?s=20&t=quwG6m5sDXRab5OmeCgPoQ) for the great help to make my first python project! 🎉 

---

_Please notice: This is my first python script. I have coded it attentive and I hope that everything works well without any guarantee of it._  
_Until now the script is tested with [Nextcloud](https://nextcloud.com/) under [Windows](https://www.microsoft.com/de-de/windows/) and some Linux distributions like [Kubuntu](https://kubuntu.org/) and [Raspberry Pi OS](https://www.raspberrypi.com/software/)._

---

### How to:

- Download and put the files from the repository in the same directory. 📁

- Run "cloud-backup-settings.py" to make the settings. 🖊

- Backup your calendars, adressbook and local cloud data by starting the script "cloud-backup.py". 💾

- Finished! 🎉 

___Note: You can use the script manually or control it with a cronjob!___ 
  
---  

### Roadmap:

- Making executable package files for linux and windows
- Possibility to make backups from different clouds
- Implement official feature to make backups from local sources

---

### Changelog:

v.1.0
- Stable release  

v.1.0.1
- Prevent overwriting todays backup
- Codecleaning

v.1.1
- Autoremove older subdirectories by setting the number individually

v.1.2
- Store data directory from by having installed the client
- Tool for making all the settings
- Code cleaning

---

<img src="https://cdn.pixabay.com/photo/2019/06/14/09/25/cloud-4273197_960_720.png" width="40%">

picture: [pixabay](https://pixabay.com/de/vectors/wolke-m%c3%a4nner-himmel-menschen-4273197/)
