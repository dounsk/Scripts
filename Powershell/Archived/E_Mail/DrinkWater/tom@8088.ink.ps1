﻿function Send-OutlookMail
{

param
  (
    # the email address to send to
    [Parameter(Mandatory=$true, Position=0, HelpMessage='The email address to send the mail to')]
    [String]
    $Recipient,

    # the subject line
    [Parameter(Mandatory=$true, HelpMessage='The subject line')]
    [String]
    $Subject,

    # the body text
    [Parameter(Mandatory=$true, HelpMessage='The body text')]
    [String]
    $body,

    # a valid file path to the attachment file (optional)
    [Parameter(Mandatory=$false)]
    [System.String]
    $FilePath = '',

    # mail importance (0=low, 1=normal, 2=high)
    [Parameter(Mandatory=$false)]
    [Int]
    [ValidateRange(0,2)]
    $Importance = 1,

    # when set, the mail is sent immediately. Else, the mail opens in a dialog
    [Switch]
    $SendImmediately
  )

  $o = New-Object -ComObject Outlook.Application
  $Mail = $o.CreateItem(0)
  $mail.importance = $Importance
  $Mail.To = $Recipient
  $Mail.Subject = $Subject
  $Mail.body = $body
  if ($FilePath -ne '')
  {
    try
    {
      $null = $Mail.Attachments.Add($FilePath)
    }
    catch
    {
      Write-Warning ("Unable to attach $FilePath to mail: " + $_.Exception.Message)
      return
    }
  }
  if ($SendImmediately -eq $false)
  {
    $Mail.Display()
  }
  else
  {
    $Mail.Send()
    Start-Sleep -Seconds 10
    $o.Quit()
    Start-Sleep -Seconds 1
    $null = [Runtime.Interopservices.Marshal]::ReleaseComObject($o)
  }
}

# --- Set The Mail Subject
$Subject = "$(Get-Date -Format 'dddd')提醒喝水小助手"
$Water = $(Get-Date -Format 'HH')-9

# --- Set The Mail Body
$body = "哟，Tom你好, 我是你的提醒喝水小助手，这是今天的第"+$Water +"轮，希望此刻看到消息的人可以和我一起来一杯水, 忙碌之余也要记得喝水呀。今日目标：250ml * 8杯，任务达成 （"+$Water+" / 8 ）。和我一起成为一天八杯水的人吧！ \^o^/"


# --- Send Email
Send-OutlookMail -Recipient tom@8088.ink -Subject $Subject -body $body -FilePath C:\Users\TOM\Documents\Mail\DrinkWater\Water.jpg  -SendImmediately #Send Now