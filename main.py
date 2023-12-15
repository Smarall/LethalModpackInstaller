import PySimpleGUI as sGui
import os
import sys
import shutil
import zipfile
from configparser import ConfigParser
import numpy as np
from datetime import datetime


config = ConfigParser()


def resource_path(pRelativePath):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, pRelativePath)


def timestampPrint(pContent):
    print(str(datetime.now().strftime('%H:%M:%S'))+': '+pContent)


def deleteFolder(pPath):
    if os.path.exists(pPath):
        shutil.rmtree(pPath)
        timestampPrint('Deleted ' + pPath)
    else:
        timestampPrint('There is no ' + pPath)


def unzipOverwrite(pZip, pDestination):
    if os.path.isfile(pZip):
        if os.path.exists(pDestination):
            zipfile.ZipFile(pZip, 'r').extractall(pDestination)
            updateConfig('paths', 'installation', values['-gameDir-'])
            updateConfig('paths', 'previousModpack', values['-modZip-'])
            timestampPrint('==>Finished installing/updating! :D')
        else:
            timestampPrint('Directory does not exist: '+pDestination)
    else:
        timestampPrint('File does not exist: '+pZip)


def updateConfig(pCategory, pKey, pContent):
    config.read('config.ini')
    config.set(pCategory, pKey, pContent)

    with open('config.ini', 'w') as conf:
        config.write(conf)


def readConfig(pCategory, pKey):
    config.read('config.ini')
    return config.get(pCategory, pKey)


def searchFiles(pDirectory, pExtension):
    foundFiles = []
    for file in os.listdir(pDirectory):
        if file.endswith(pExtension):
            foundFiles.append(file)
    return foundFiles


def modlist2Table(pSource, pTable):
    tmp = searchFiles(pSource + '/BepInEx/plugins/', '.dll')
    pModlist = (np.array(tmp).reshape(len(tmp), -1).tolist())
    window[pTable].update(values=pModlist)


# ====PSG===============================================================================================================
sGui.theme('Reddit')

layout = [[sGui.Text('LethalCompany directory', size=(20, 1)),
           sGui.InputText(default_text=readConfig('paths', 'installation'), key='-gameDir-'),
           sGui.FolderBrowse()],


          [sGui.Text('Modpack (.zip)', size=(20, 1)),
           sGui.InputText(default_text=readConfig('paths', 'previousModpack'), key='-modZip-'),
           sGui.FileBrowse(file_types=[('Modpack', '*.zip')])],

          [sGui.Checkbox('delete plugins', key='-delPlugins-'),
           sGui.Checkbox('delete configs', key='-delConfigs-')],

          [sGui.Button('Install / Update', key='-install-')],

          [sGui.Output(size=(75, 10))]]

modlistLayout = [[sGui.Button('Refresh Modlist', expand_x=True, key='-reloadModlist-')],

                 [sGui.Table(headings=['Installed Mods'], values=[], hide_vertical_scroll=True, size=(0, 15), justification='left', key='-availableMods-'),
                  sGui.Table(headings=['Selected Mods'], values=[], hide_vertical_scroll=True, size=(0, 15), justification='left', key='-selectedMods-')]]

window = sGui.Window('LethalModpackInstaller v1.1   (Smarall)',
                     [[sGui.Column(layout), sGui.VerticalSeparator(), sGui.Column(modlistLayout)]],
                     icon=resource_path('lmi.ico'))


while True:
    event, values = window.read()

    if event == sGui.WIN_CLOSED:
        break

    if event == '-reloadModlist-':
        modlist2Table(values['-gameDir-'], '-availableMods-')
        zipfile.ZipFile(values['-modZip-'], 'r').extractall(values['-modZip-'].removesuffix('.zip'))
        modlist2Table(values['-modZip-'].removesuffix('.zip'), '-selectedMods-')
        shutil.rmtree(values['-modZip-'].removesuffix('.zip'))

    if event == '-install-':
        if values['-delPlugins-']:
            deleteFolder(values['-gameDir-'] + '/BepInEx/plugins')
        if values['-delConfigs-']:
            deleteFolder(values['-gameDir-'] + '/BepInEx/config')
        unzipOverwrite(values['-modZip-'], values['-gameDir-'])


window.close()
