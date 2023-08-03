; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!


#define MyAppName "AYON"
#define SourceDir GetEnv("BUILD_SRC_DIR")
#define OutputDir GetEnv("BUILD_DST_DIR")
#define OutputFilename GetEnv("BUILD_DST_FILENAME")
#define AppVer GetEnv("BUILD_VERSION")


[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={#MyAppName}{#AppVer}
AppName={#MyAppName}
AppVersion={#AppVer}
; 'AppVerName' What is shown in app remove section of Control Panel
AppVerName={#MyAppName} {#AppVer}
AppPublisher=Ynput s.r.o
AppPublisherURL=https://ynput.io
AppSupportURL=https://ynput.io
AppUpdatesURL=https://ynput.io
; 'DefaultDirName' We don't use this value!!! Go to 'InitializeWizard'
DefaultDirName={autopf64}\Ynput\AYON\app\{#MyAppName} {#AppVer}
UsePreviousAppDir=no
DisableProgramGroupPage=yes
OutputBaseFilename={#OutputFilename}
AllowCancelDuringInstall=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
SetupIconFile=common\ayon_common\resources\AYON.ico
OutputDir={#OutputDir}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\ayon.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[InstallDelete]
; clean everything in previous installation folder
Type: filesandordirs; Name: "{app}"

[UninstallDelete]
; clean everything in installation folder - it is not recommended by inno setup documentation but we need to do it
;  because there may be files that were not available in install files (like .pyc files)
Type: filesandordirs; Name: "{app}"

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; AfterInstall: AfterInstallProc(); Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\ayon.exe"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\ayon.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\ayon.exe"; Description: "{cm:LaunchProgram,AYON}"; Flags: nowait postinstall skipifsilent

[Code]
procedure AfterInstallProc();
var
  OutputFilepath: String;
  InstallDir: String;
begin
  OutputFilepath := GetEnv('AYON_INSTALL_EXE_OUTPUT');
  InstallDir := ExpandConstant('{app}');
  if Length(OutputFilepath) > 0 then
  begin
    if FileExists(OutputFilepath) then
    begin
      SaveStringToFile(OutputFilepath, InstallDir+'\ayon.exe', False)
    end;
  end;
end;

function CompareParameter(param, expected: String): Boolean;
begin
  Result := False;
  if Length(param) >= Length(expected) then
  begin
    if CompareText(Copy(param, 1, Length(expected)), expected) = 0 then
    begin
      Result := True;
    end;
  end;
end;

function GetParameter(expectedParam: String): String;
var
  i : LongInt;
begin
  Result := '';
  for i := 0 to ParamCount() do
  begin
    if CompareParameter(ParamStr(i), '/' + expectedParam + '=') then
    begin
      Result := Copy(ParamStr(i), Length(expectedParam) + 3, Length(ParamStr(i)));
      break;
    end;
  end;
end;

procedure InitializeWizard();
var
  NewInstallFolder: String;
  NewInstallRoot: String;
  CurrentDefaultDir: String;
  ProgramFilesDir: String;
begin
  NewInstallFolder := GetParameter('DIR');
  if Length(NewInstallFolder) = 0 then
  begin
    NewInstallRoot := GetParameter('INSTALLROOT');
    if Length(NewInstallRoot) > 0 then
    begin
      NewInstallFolder := NewInstallRoot + '\{#MyAppName} {#AppVer}'
    end
    else
    begin
      CurrentDefaultDir := ExpandConstant('{autopf64}');
      ProgramFilesDir := ExpandConstant('{commonpf64}');
      if CompareStr(CurrentDefaultDir, ProgramFilesDir) = 0 then
        NewInstallFolder := ExpandConstant('{commonpf64}') + '\Ynput\{#MyAppName} {#AppVer}'
      else
        NewInstallFolder := ExpandConstant('{localappdata}') + '\Ynput\AYON\app\{#MyAppName} {#AppVer}';
    end;
  end;
  WizardForm.DirEdit.Text := NewInstallFolder;
end;
