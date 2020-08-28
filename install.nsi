!include MUI2.nsh

Unicode True
Name "ecc"
OutFile "install-ecc.exe"
InstallDir "$PROGRAMFILES\ecc"
SetCompressor lzma
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!define MUI_ABORTWARNING


Section
  SetOutPath "$INSTDIR"
  File /r "dist\ecc_gui\*.*"
  
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
  CreateDirectory "$SMPROGRAMS\ecc"
  SetOutPath "$INSTDIR"
  CreateShortcut "$SMPROGRAMS\ecc\ecc.lnk" "$INSTDIR\ecc_gui.exe" ""
  
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ecc" "DisplayName" "ecc"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ecc" "UninstallString" '"$INSTDIR\uninstall.exe"'
SectionEnd


Section "Uninstall"
  RMDir /r "$INSTDIR"

  Delete "$SMPROGRAMS\ecc\ecc.lnk"
  RMDir /r "$SMPROGRAMS\ecc"

  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ecc"
SectionEnd
