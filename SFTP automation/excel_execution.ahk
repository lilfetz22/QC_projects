; Activate a specific Excel window and sheet
;#IfWinActive, ahk_class Excel71WindowClass  ; Only run this script when an Excel window is active
;    WinGet, active_id, ID, A
;    WinGetTitle, active_title, A
;    WinGetClass, active_class, A
;    MsgBox, The active window's ID is "%active_id%". and the title is "%active_title%". and the class is "%active_class%"  

; Activate Excel window "Microsoft Excel - testing emails.xlsx" and go to Sheet3
^!b::
    ; Activate the specific Excel window
    ;WinActivate, testing emails - Excel
    ;WinWaitActive, testing emails - Excel
    WinGet, id, List,,, Program Manager
    Loop, %id%
    {
        this_id := id%A_Index%
        WinGetTitle, this_title, ahk_id %this_id%
        IfInString, this_title, Message
            {
                WinActivate, this_title
                MsgBox, %this_title%
                break
            }        
        else if (A_Index = %id%)
            {
                MsgBox, No window with "Message" in the title found.
                break
            }


        ;MsgBox, 4, , Visiting All Windows`n%A_Index% of %id%`nahk_id %this_id%`nahk_class %this_class%`n%this_title%`n`nContinue?
        ;IfMsgBox, NO, break
    }

    ;WinGet, active_id, ID, A
    ;WinGetTitle, active_title, A
    ;WinGetClass, active_class, A
    ;MsgBox, The active window's ID is "%active_id%". and the title is "%active_title%". and the class is "%active_class%" 

    ; if the active title contains "Message" then activate email draft window
    ;IfInString, active_title, Message
    ;{
    ;    WinActivate, active_title
    ;    Send, hello
    ;}
    ; Activate the specific sheet
    ;Send, ^q  ; 

return