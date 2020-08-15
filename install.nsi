Unicode True
Name "ecc"
OutFile "install-ecc.exe"
InstallDir "$PROGRAMFILES\ecc"
SetCompressor lzma
Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

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
