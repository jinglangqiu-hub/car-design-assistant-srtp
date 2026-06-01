#define MyAppName "Car Design Assistant"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Chongqing University SRTP Project"
#define MyAppExeName "CarDesignAssistant.exe"

[Setup]
AppId={{7B0BD756-0F71-4F04-BED9-CF92D14D0B0A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\CarDesignAssistant
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=..\installer
OutputBaseFilename=CarDesignAssistant_Setup_v{#MyAppVersion}
Compression=lzma2
SolidCompression=yes
DiskSpanning=yes
DiskSliceSize=1500000000
WizardStyle=modern
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional tasks:"; Flags: unchecked

[Files]
Source: "..\dist\CarDesignAssistant\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\app\README.md"; DestDir: "{app}\app"; Flags: ignoreversion

[Dirs]
Name: "{app}\outputs"
Name: "{app}\outputs\app_generated"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
