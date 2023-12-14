import PySimpleGUI as sGui
import os
import sys
import shutil
import zipfile

def resource_path(pRelativePath):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, pRelativePath)

def deleteFolder(pPath):
    if os.path.exists(pPath):
        shutil.rmtree(pPath)
        print('Deleted ' + pPath)
    else:
        print('There is no ' + pPath)


def unzipOverwrite(pZip, pDestination):
    if os.path.isfile(pZip):
        if os.path.exists(pDestination):
            zipfile.ZipFile(pZip, 'r').extractall(pDestination)
            print('Finished installing/updating! :D\n')
        else:
            print('Directory does not exist: '+pDestination)
    else:
        print('File does not exist: '+pZip)


# ====PSG===============================================================================================================
sGui.theme('Reddit')

layout = [[sGui.Text('LethalCompany directory', size=(20, 1)), sGui.InputText(key='-gameDir-'), sGui.FolderBrowse()],
          [sGui.Text('Modpack (.zip)', size=(20, 1)), sGui.InputText(key='-modZip-'), sGui.FileBrowse(file_types=[('Modpack', '*.zip')])],
          [sGui.Checkbox('delete plugins', key='-delPlugins-'), sGui.Checkbox('delete configs', key='-delConfigs-')],
          [sGui.Button('Install / Update', key='-install-')],
          [sGui.Output(size=(75, 5))]]

window = sGui.Window('LethalModpackInstaller v1.0   (Smarall)', layout, icon=resource_path('lmi.ico'))

while True:
    event, values = window.read()
    if event == sGui.WIN_CLOSED:
        break
    if event == '-install-':
        if values['-delPlugins-']:
            deleteFolder(values['-gameDir-'] + '/BepInEx/plugins')
        if values['-delConfigs-']:
            deleteFolder(values['-gameDir-'] + '/BepInEx/config')
        unzipOverwrite(values['-modZip-'], values['-gameDir-'])

window.close()
