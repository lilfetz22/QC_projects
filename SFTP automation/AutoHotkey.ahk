^j::
; #IfWinActive, ahk_class Excel71WindowClass
; #IfWinActive, ahk_class Outlook

WinActivate, contacts_w_sftp_info_no_macro_2024_07_11 - Excel
Send, ^q

^!p::Pause

^!j::

WinGet, id, List,,, Program Manager
Loop, %id%
{
    this_id := id%A_Index%
    WinGetTitle, this_title, ahk_id %this_id%

    ; if the active title contains "Message" then activate email draft window
    IfInString, this_title, Message
    {
        WinActivate, this_title
        ;WinWaitActive, this_title
        ;WinMaximize, this_title

        ; encrypt the email message
        Send, !ppm{Enter}
        Sleep, 1000

        ;change the from email address
        ControlGetPos, X, Y, Width, Height, Button2, ahk_id %this_id%
        MouseClick, left, X, Y
        Send, {Down}{Enter}       
        Sleep, 1000

        ; send the email 
        Send, ^{Enter}
        Sleep, 1000
    }
}


return