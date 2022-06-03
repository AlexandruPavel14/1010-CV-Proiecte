.model small
.stack 100
.data
m1 db 'Introduceti numarul: $'
m2 db 'Cifrele numarului sunt egale.$'
m3 db 'Cifrele numarului nu sunt egala.$'
.code
	mov ax, @data
	mov ds, ax

	mov ah, 9h
	mov dx, offset m1
	int 21h

	mov ah, 01h
	int 21h

	mov dl, al
	int 21h

	cmop al, dl
	jne negatie

	mov dl, 0dh
	mov dl, 0ah
	int 21h

	mov ah, 09h
	lea dx, m2
	int 21h
	jmp sfarsit
neegale:
	mov dl, 0dh
	mov dl, 0ah
	int 21h

	mov ah, 09h
	lea dx, m3
	int 21h

sfarsit:
	mov ah, 4ch
	int 21h
end