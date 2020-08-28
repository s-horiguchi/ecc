!include MUI2.nsh

Unicode True
Name "ecc"
OutFile "install-ecc.exe"
InstallDir "$LOCALAPPDATA\ecc"
InstallDirRegKey HKCU "Software\ecc" ""
RequestExecutionLevel user
SetCompressor lzma

;------- Variables -------

Var StartMenuFolder


;------- Interface Settings -------
!define MUI_WELCOMEPAGE_TITLE "ecc installer"
!define MUI_WELCOMEPAGE_TEXT "Click next to run the ecc installation"
!define MUI_FINISHPAGE_RUN "$INSTDIR\ecc_gui.exe"

!define MUI_FINISHPAGE_SHOWREADME
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Create Desktop Shortcut"
!define MUI_FINISHPAGE_SHOWREADME_FUNCTION CreateDesktopShortCut
!define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED

;------- Functions -------

Function CreateDesktopShortCut
 
  CreateShortCut "$DESKTOP\ecc.lnk" "$INSTDIR\Advanced.exe" "" 
 
FunctionEnd


;------- Pages -------
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY

;Start Menu Folder Page Configuration
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\ecc"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES


!insertmacro MUI_LANGUAGE "English"
!define MUI_ABORTWARNING


Section
  SetOutPath "$INSTDIR"
  File /r "dist\ecc_gui\*.*"
  WriteRegStr HKCU "Software\ecc" "" $INSTDIR
  
  WriteUninstaller "$INSTDIR\uninstall.exe"

  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
  CreateShortCut "$SMPROGRAMS\$StartMenuFolder\ecc.lnk" "$INSTDIR\ecc_gui.exe" "" 
  CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\uninstall.exe"

  !insertmacro MUI_STARTMENU_WRITE_END

 

SectionEnd


Section "Uninstall"
  RMDir /r "$INSTDIR"
 
  ;Get Start Menu Folder
  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
 
  ;Delete shortcuts
  Delete "$SMPROGRAMS\$StartMenuFolder\ecc.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk"
  RMDir "$SMPROGRAMS\$StartMenuFolder"
 
  Delete "$DESKTOP\$(^Name).lnk"

  DeleteRegKey /ifempty HKCU "Software\ecc"
SectionEnd
