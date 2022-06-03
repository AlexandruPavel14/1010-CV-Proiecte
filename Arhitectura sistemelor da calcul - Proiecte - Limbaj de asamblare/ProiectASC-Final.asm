;	verificarea paritatii unui sir de numere

.model small
.stack 100vh
.data
;	cele 6 mesaje pe care le cuprinde programul in intregime
	msg1 db 0ah, 0dh, "|| Proiect - Arhitectura sistemelor de calcul ||$"
	msg db 0ah, 0dh, "| Introduceti lungimea sirului de numere: $"
	array db 0ah, 0dh, "| Introduceti elementele acestuia:$"
	pare db 0ah, 0dh, "| Numerele pare introduse sunt: $"
	continuare db 0ah, 0dh, "Doriti sa continuati? Da(d) / Nu(n)",0ah, 0dh, '$'
	impar db 0ah, 0dh, "| Nu se regasesc numere pare in datele introduse!",0ah,0dh, '$'
.code
main:
;	initializare segment de date
	mov ax, @data
	mov ds, ax

;	afisare mesaj msg1 - titlu
	lea dx, msg1
	mov ah, 09h
	int 21h

cont:
;	afisare mesaj msg - datele cerute de la tastatura pentru lungimea sirului introdus
	lea dx, msg
	mov ah, 09h
	int 21h

	mov ah, 01h
	int 21h

	sub al, 30h
	mov cl, al
;	afisare mesaj array - datele cerute de la tastatura pentru elementele sirului introdus
	lea dx, array
	mov ah, 09h
	int 21h

	mov ch, 00h

again:
	mov dl, ' '
	mov ah, 02h
	int 21h

	mov ah, 01h
	int 21h

	sub al, 30h
	mov ah, 00h
	mob bl, 02h
	aad
	div bll
	cmp ah, 00h
	je increase

return:
	dec cl
	cmp cl, 00h
	jg again

	cmp ch, 00h
	je numere_impare
;	afisare mesaj numere par - acestea se regasesc in datele de intrare
	lea dx, pare
	mov ah, 09h
	int 21h

	jmp num

numere_impare
;	afisare mesaj numere impare - acestea nu se regasesc in datele de intrare
	lea dx, impar
	mov ah, 09h
	int 21h
	jmp algere

num:
;	afisare numere introduse de utilizator
	mov dl, ' '
	mov ah, 02h
	int 21h

	pop ax
	mov dl, ax
	add dl, 30h
	mov ah, 02h
	int 21h
	dec ch
	cmp ch, 00h
	jmp num

alegere:
;	afisare mesaj continuare - daca dorim sa reluam procesul
	lea dx, continuare
	mov ah, 09h
	int 21h

	mov ah, 01h
	int 21h
	or al, 20h
	cmp al, 'd'
	je cont

	jmp exit

increase:
	mov ah, al
	add ah, al
	push ax
	inc ch
	jmp return

;	apel functie de terminare normala a programului
exit:
	mov ah, 4ch
	int 21h
