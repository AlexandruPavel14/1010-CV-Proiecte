Clear-Host
$locatie="C:\WINDOWS\System32\config\systemprofile\Desktop\TestProiect" #calea folderului din care sunt preluat fisierele
$items=Get-ChildItem -Path $locatie #reprezita un vector cu fisierele din variabila $locatie
$numarul=0 #reprezinta variabila contor
$datazi=(Get-Date).Date
$dataafisare=Get-Date -Format "MM/dd/yyy" #reprezinta formatul in care se va afisa data 
#se parcurg elemetele din vector, respectiv pentru fiecare fisiere
foreach($item in $items){ 
    $dataModif=$item.LastWriteTime.Date


    if($dataModif -eq $datazi)
    {$numarul++} #se incrementeaza variabila numarul daca data ultimei modificari este cea curenta
}
if ($numarul -ne 0){
    "Astazi $dataafisare s-au modificat $numarul fisier(e) in $locatie" #se afiseaza acest mesaj daca variabila numarul nu este egala cu 0
} else {
    "Astazi $dataafisare nu s-a modificat niciun fisier in $locatie" #se afiseaza acest mesaj daca variabila numarul este egala cu 0
}    
