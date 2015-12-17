# FudanPTAutoDownloader
A script for auto download torrents of [PT@Platform](http://pt.vm.fudan.edu.cn/)
##Usage
* Modify your `ptusername` and `ptuserinfo` in script `transmission.py`
  * The `ptuserinfo` can be calculated by `sha1(username + password)`
  * If your username has any Chinese character, please refer to PT's javascript.
* Modify `save_path` to a folder used to save torrent file.
* Modify `token_path` to a blank file to save your cookie.
* Modify info in `transmissionrpc` and make sure the IP is authorised.
* Use `crontab` to run script `transmission.py` automatically.
* Also, the script `downloader.py` can be used to download the N smallest torrents.

##About
* If you use this script and want to send some `ptp` to me, you can send them to user `ihciah`.
