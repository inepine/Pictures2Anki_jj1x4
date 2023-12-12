data2Anki := "C:\Users\vboxuser\Documents\Pictures2Anki_jj1x4\data2Anki.txt"
;如果data不存在，结束程序
if(not FileExist(data2Anki)) 
{
	Exit
}

SetTitleMatchMode 3 

user1 := "user1 - Anki"
WinActivate %user1%
Send y
sleep 100

anki_sync := "正在同步..."


WinWait ,%anki_sync%  ,,2
WinActivate %anki_sync%
i = 0 ;一个i延时250ms。用于判断导入文件结束。
while (i<8)
{
	if(WinExist(anki_sync))
	{
		i = 0
    WinActivate %anki_sync%
		Sleep 10
}else{
	Sleep 250
	i++
}
}

WinActivate .*-\sAnki$
Send ^+i


WinWait , 导入
WinActivate 导入
Sleep 1000
Send {Blind}{Text} %data2Anki%
sleep 500
Send {Enter}
Send {Enter}

WinWait , 导入文件
WinActivate 导入文件


i = 0 ;一个i延时250ms。用于判断导入文件结束。
while (i<4)
{
	if(WinExist(导入文件))
	{
		i = 0
		Send ^{Enter}
		Sleep 10
}else{
	Sleep 250
	i++
}
}
Sleep 250
Send y

FileDelete %data2Anki%