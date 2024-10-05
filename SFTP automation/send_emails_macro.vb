Sub SendEmails()
    Dim OutApp As Object
    Dim OutMail As Object
    Dim OutMail2 As Object
    Dim cell As Range
    Dim emailBody As String
    Dim emailSubject As String
    Dim emailBody2 As String
    Dim emailSubject2 As String
    Dim startRow As Long
    Dim endRow As Long
    
    ' Create an instance of Outlook
    Set OutApp = CreateObject("Outlook.Application")
    
    ' Find the first cell that doesn't have a 1 in Column J
    startRow = 2
    While Range("J" & startRow).Value = 1
        startRow = startRow + 1
    Wend

    ' Set the end row to the 4th cell after the first empty cell
    endRow = startRow + 10

    ' Loop through the email addresses in the Excel file
    For Each cell In Range("C" & startRow & ":C" & endRow)
        If cell.Value <> "" Then
            ' Create a new email message
            Set OutMail = OutApp.CreateItem(0)

            ' Set the email properties
            OutMail.To = cell.Value ' Email address
            emailSubject = Range("H" & cell.Row).Value ' Subject is in cell B2
            emailBody = Range("F" & cell.Row).Value ' Body is in cell C2
            OutMail.Subject = emailSubject
            OutMail.body = emailBody
            
            ' Display the email
            OutMail.Display

            ' Clean up
            Set OutMail = Nothing
            
            ' Create the next email message
            Set OutMail2 = OutApp.CreateItem(0)

            ' Set the email properties
            OutMail2.To = cell.Value ' Email address
            emailSubject2 = Range("I" & cell.Row).Value
            emailBody2 = Range("G" & cell.Row).Value
            OutMail2.Subject = emailSubject2
            OutMail2.body = emailBody2

            ' display the email
            OutMail2.Display

            ' Clean up
            Set OutMail2 = Nothing
            Range("J" & cell.Row).Value = 1
        End If
    Next cell

    ' Clean up
    Set OutApp = Nothing
End Sub
