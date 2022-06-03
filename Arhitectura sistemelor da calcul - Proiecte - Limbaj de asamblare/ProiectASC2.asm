m1	db	     'Introduceti parola:$'
m2	db 13,10 'Parola incorecta.$'
m3  db 13,10 'Parola corecta.$'
m4  db		 'Alexandru'
.code
	mov ax,@data
	mov ds,ax

	mov bx,offset m4
	mov cx,6

;	afisare mesaj m1
	mov ah, 9h
	mov dx, offset m1
	int 21h
;	citeste un caracter in al fara intoarcere

again:
	mov ah,08
	int 21h

	cmp al,[bx]
	jne eroare
	inc bx
	loop again

	mov dx,offset m3
	mov ah,09
	int 21h
	jmp sfarsit

eroare:
	mov dx,offset m2
	mov ah,09h
	int 21h

sfarsit:
	mov ah, 4ch
	int 21h
end