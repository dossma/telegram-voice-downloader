# telegram-voice-downloader
Download all voice messages from a Telegram channel.

## Motivation 
If you like a channel where the owner shares valuable voice messages, but have not always the time to listen to them, you can hereby download and archive them on your computer. Archiving can also be important in case the app or the channel shuts down.

## Procedure
To use this program, it is beforehand required to have an API ID and an API hash which you can get from https://core.telegram.org/api/obtaining_api_id#obtaining-api-id. Read, understand and comply to the terms of Telegram's API service.

1. Set the folder where you want the files to be downloaded.
2. Paste your API ID and API hash in the designated fields.
3. Type in the channel name under the variable `channel`. The channel name is the one after t.me/ of the link https://t.me/channelname.
4. Set the value for `limit` which indicates how many files you want to download. It downloads in order from the most recent one. Set `None` if you want to get all.

On the first run, a file called `id_list.txt` will be created inside the same folder of where the files are to be downloaded.
For each voice message downloaded, the program stores its unique ID into that file.
So when you run the program another time, the program reads which IDs are already present in this file and skips downloading them.
This prevents downloading duplicates and you can run the program any time knowing that only files will be downloaded which you yet not have.
So it is very important to keep this file. When you set a different folder at some point, make sure you move this file to the new folder.

The file name pattern has been set to `<creation date> <title> <views>views`,
so i.e. `2022-12-16 Why we do what we do 800views.oga`

In case a title of the voice message is not present, the pattern is `<creation date> <unknown> <trailing number> <views>views`,
so i.e. `2022-12-16 unknown1 800views.oga`

Note that view count is rounded to hundred.

## Development setup

Required external libraries are
- Telethon: https://github.com/LonamiWebs/Telethon

```sh
pip install telethon
```

## Meta

Author: Jonas Dossmann

Distributed under the GPL-3.0 license.

[https://github.com/dossma/](https://github.com/dossma/)

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dossma/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dossma/node-datadog-metrics
[wiki]: https://github.com/dossma/ebook-file-renaming/wiki
