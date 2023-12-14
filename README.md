# How to use it?
![image](https://github.com/Smarall/LethalModpackInstaller/assets/41205154/9ee0ed3b-b0c9-486f-b8fa-590c6c4ab9a8)
**- LethalCompany directory:** Please select the installation directory of your game. It should look somewhat like this: `DriveLetter:\Steam\steamapps\common\Lethal Company`
**- Modpack (.zip):** For this, please select your modpack zip archive. You'll find more information about compatibility below.

## Advanced
**- delete plugins:** When switching between modpacks and for clean updates, I recommend to check this box - it'll get rid of all currently installed plugins before installing the new ones.
**- delete configs:** As long as you didn't change anything in your config files by hand, I always recommend turning this on. As you might get rid off some mods, those would otherwise remain.

### Modpack compatibility:
Compatible modpacks should use the BepInEx folder structure:
`\BepInEx\plugins` <-- *.dll and similar
`\BepInEx\configs` <-- *.cfg
In the best case, you include the newest supported version of BepInEx in your modpack.
