$Signature = @'
  [DllImport("user32.dll")]
  public static extern void mouse_event(long dwFlags, long dx, long dy, long cButtons, long dwExtraInfo);
'@
$MouseEvent = Add-Type -MemberDefinition $Signature -Name "Win32MouseEvent" -Namespace Win32Functions -PassThru
while ($true) {                             #
  Start-Sleep -s 30
  $MouseEvent::mouse_event(1, 0, 0, 0, 0)
}