[Setup]
AppName=Region Census
AppVersion=0.8.1

DefaultDirName={commonpf32}\Region Census
DefaultGroupName=Region Census

OutputBaseFilename=RegionCensusSetup
Compression=lzma
SolidCompression=yes

DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no

WizardStyle=classic
WizardImageFile=wizard.bmp
WizardSmallImageFile=wizard_small.bmp


[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\Region Census"; Filename: "{app}\RegionCensus.exe"
Name: "{commondesktop}\Region Census"; Filename: "{app}\RegionCensus.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; Flags: unchecked

[Run]
Filename: "{app}\RegionCensus.exe"; Description: "Launch Region Census"; Flags: nowait postinstall skipifsilent
