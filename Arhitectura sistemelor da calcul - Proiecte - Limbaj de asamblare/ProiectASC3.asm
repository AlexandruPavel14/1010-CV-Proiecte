.model small
.stack 100h
.data

mesaj db 13,10,'Introduceti numarul:(<=9)$'
mesg_par db 13,10,'Numarul introdus este par!$'
mesg_impar db 13,10,'Numarul introdus este impar!$'

.code

mov ax, @data
mov ds, ax

mov ah, 09
mov dx, offset mesaj
int 21h

mov ah, 01h
int 21h
mov bx,2
div bx
cmp dx,0
jnz impar
mov ah,09
mov dx, offset mesg_par
int 21h
jmp sfarsit

impart:
mov ah,09
mov dx,offset mesg_impar
int 21h

sfarsit:
mov ah,4ch
int 21h
end