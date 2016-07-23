# subdomainator

Stay on top of new subdomains! Bug bounty hunters can use this tool to receive Pushbullet notifications each time there is a new target subdomain.

## Installation

```
git clone https://github.com/skorov/subdomainator.git
cd subdomainator
pip install -r requirements.txt
python subdomainator_cli.py
```

**Sign up with Pushbullet and get your API key.**
![pushbullet](http://i.imgur.com/hRi6KM0.png)

**Add the Pushbullet key in subdomainator.**
[![add key](https://asciinema.org/a/7y595ruxx2rsgyvtcoalfgrhz.png)](https://asciinema.org/a/7y595ruxx2rsgyvtcoalfgrhz)

**Edit config.py file.**  
![config](http://i.imgur.com/doOjbYK.png)

That's the bare minimum! You're ready to add domains.

## Usage

**Enable some modules to search for subdomains for us.**
[![enable mod](https://asciinema.org/a/e9uuvc7a6rgm6exjjno9yjl0p.png)](https://asciinema.org/a/e9uuvc7a6rgm6exjjno9yjl0p)

**Add a domain to monitor.**
[![add domain](https://asciinema.org/a/cws3ea4ch9r9lyl4pgqfog2yu.png)](https://asciinema.org/a/cws3ea4ch9r9lyl4pgqfog2yu)

Note: You won't get notification the first run.

That's it! Sit back and wait for the subdomains to roll in to your browser, phone or wherever you have Pushbullet.

## Modules
The following modules currently come with subdomainator. I plan to add more later. :-)

### sublist3r
Such an awesome tool, that I just had to hook into it. This modules runs the non-bruteforce parts of the tool.
You will need to get sublist3r working yourself before you can use this module.

### Virus Total
Contains decent subdomain data.

## History

**23/07/2016:**
 * Release

## Credits

* Credit for inspiration goes to Shubs (@infosec_au) and his tool, [Assetnote](https://github.com/infosec-au/assetnote)
* Thanks to aboul3la for making [sublist3r](https://github.com/aboul3la/Sublist3r) for which subdomainator has a module. This made my life much easier!

## Get in touch

Does my tool suck? Let me know what you think!
Twitter: [@skorov8](https://twitter.com/skorov8)
