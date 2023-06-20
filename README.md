
# Minecraft Server Mod Updater

This is a small command line utility that can check the Minecraft mods folder for any updates and download new jar files. I run a small Minecraft server and the most tedious maintence task is keeping the mods up to date. This tool is designed to help with that. Currently the tool only supports Modrinth. 


## Usage

```sh
usage: updater.py [-h] -f F -v V -l L [-y]

Minecraft Server Mod Updater

optional arguments:
  -h, --help         show this help message and exit
  -f F, --folder F   The directory of the mods folder.
  -v V, --version V  The version of Minecraft to update mods to
  -l L, --loader L   The mod loader you are using (Fabric, Forge, etc...)
  -y                 Automatically accept update
```


## Disclaimer

This is a very small project that was made by one person in a few hours. It has not been rigerourly testes and you should use at your own risk. I take no responsibility for the effects of running this program. If you have any feedback or find any bugs please let me know.

