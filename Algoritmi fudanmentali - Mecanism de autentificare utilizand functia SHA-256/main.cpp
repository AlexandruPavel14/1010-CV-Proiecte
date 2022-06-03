/*
 Student: Pavel Alexandru Daniel
 Data: 17.05.2021
 Descriere: Crearea unui mecanism de autentificare utilizatori,
            cont si parola, utilizand functii hash, MD5, SHA, la alegere.
 Algoritmi:
   1. Functia folosită pentru a schimba culoarea textului din consola
   2. Functia care primeste o variabila de tip string si o returneaza pe acesta sub forma de cod SHA256

*/

#include<iostream>   //  Pentru a citi sau scrie în fluxurile standard de intrare / ieșire.
#include"criptare.h" //  Apelare fisier algoritm SHA256.
#include<stdio.h>    //  Pentru a include funcțiile legate de intrare / ieșire în programul nostru.
#include<conio.h>    //  Ține ecranul până când se recepționează tastatura.
#include<stdlib.h>   //  pentru acceptarea și afișarea intrărilor și ieșirilor.
#include<windows.h>  //  Fișier antet specific Windows pentru limbajele de programare C și C ++ care conține declarații pentru toate funcțiile din API-ul Windows.
#include<dos.h>      //  Această bibliotecă are funcții care sunt utilizate pentru gestionarea întreruperilor, producerea funcțiilor de sunet, dată și oră.
#include<fstream>    //  Biblioteca oferă funcții pentru fișiere. Pentru a deschide un fișier, mai întâi trebuie creat un obiect filestream.
#include<string>     //  Conține definiții macro, constante și declarații de funcții și tipuri utilizate nu numai pentru gestionarea șirurilor, ci și diverse funcții de gestionare a memoriei.
using namespace std; //  Toate elementele bibliotecii standard C++ sunt declarate într-un spaţiu de nume (namspece), şi anume in namespace-ul cu titlul std.


// 1. Functia folosită pentru a schimba culoarea textului din consola
void SetColor(int ForgC)
{
    WORD wColor; // Este necesar pentru a obține atributul curent de fundal
    HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_SCREEN_BUFFER_INFO csbi; // csbi este folosit pentru cuvântul wAttributes

    // Pentru a masca toate, cu excepția atributului de fundal, și pentru a adăuga culoarea
    if (GetConsoleScreenBufferInfo(hStdOut, &csbi))
    {
        wColor = (csbi.wAttributes & 0xF0) + (ForgC & 0x0F);
        SetConsoleTextAttribute(hStdOut, wColor);
    }
    return;
}

// 2. Functia care primeste o variabila de tip string si o returneaza pe acesta sub forma de cod SHA256
string stringToSha(string password){ // password reprezinta parametrul formal
    string hash; 
    int len=password.length();
    char cahrtot[len+1];
    strcpy(cahrtot,password.c_str());
    hash=SHA256(cahrtot);

    return hash;
}


// funcţia principala care alcătuieşte programul 
int main (){
	// declarare variabilie de tip caracter
	string account_name, account_name_login, password, password_login, username, hash, account_password;

    // declarare variabilie pentru numar incercari autentifacre utilizator și citire optiune
	bool login_successful = false;
    long long option, remain = 5;
    SetColor(14);

    // Afisare pe ecranul utilizatorului titlul proiectului
    cout << "--------------------------------------------------------\n";
    cout << "  Mecanism de autentificare utilizand functia SHA-256\n";
    cout << "--------------------------------------------------------\n" << endl;

    // Afisare pe ecranul utilizatorului optiunile pe care acesta le poate folosi
    cout << "[Optiunea 1] Inregistrare" << endl << "[Optiunea 2] Autentificare"  << endl;
    cout << "Optiunea aleasa de dumneavoastra: ";

    // Citire optiune aleasa de utilizator
    cin >> option;

    // [Optiunea 1] Inregistrare utilizatorului
    if (option == 1)
    {
    	// afisarea textului care urmeaza se prezinta a fi de culoarea ____
    	SetColor(11);

    	// Informare utilizator în cazul în care se afla
    	cout << "--------------------------\n";
        cout << "      Inregistrare\n";
        cout << "--------------------------\n" << endl;

    	// Creare utlizator
        cout << "Creati un nume de utilizator: ";
        cin >> account_name;
        cout << endl;

        // Creare parola
        cout << "Creati o parola: ";
        cin >> password;

        // variablia password_login este convertita in parola securizat SHA256
        account_password=stringToSha(password);

        // crearea fisier txt
        ofstream user_info;

        // numele fisierului 
        user_info.open("user_" + account_name + ".txt");

        // datele pe care fisierul sa le contina
        user_info << account_name << endl << account_password;

        // finalizare fisier txt
        user_info.close();

        // afisarea textului care urmeaza se prezinta a fi de culoarea ____
        SetColor(2);

        // afisarea textului care urmeaza se prezinta a fi de culoarea verde. 
        cout << "\n-> Inregistrare efectuata cu succes!" << endl << endl;

        // finalizare set de instructiuni pentru [Optiunea 1]
        main();

    }

    // [Optiunea 2] Autentificare utilizatorului
    else if (option == 2)
    {
        do
        {

    	// afisarea textului care urmeaza se prezinta a fi de culoarea ____
        SetColor(9);

    	// Informare utilizator în cazul în care se afla
    	cout << "--------------------------\n";
        cout << "      Autentificare\n";
        cout << "--------------------------" << endl;

        // Autentificare utlizator - introducere nume
        cout << endl << "Introduceti numele de utilizator: ";
        cin >> account_name_login;

        // Autentificare utlizator - introducere parola
        cout << endl << "Introduceti parola: ";
        cin >> password_login;

        ifstream find_account("user_" + account_name_login + ".txt");

        // getline este utilizată pentru a citi datele din fisierul txt creat la inregistrarea utilizatorului
        getline(find_account, account_name);
        getline(find_account, password);

        // utilizatorul introduce parola de la tastatura, aceasta urmand a trece prin procesul de SHA256 si dupa comparata cu parola hash
        // Conditia in care datele introduse se asociaza cu cele din fiserul txt
        if(account_name==account_name_login && password==stringToSha(password_login)){
            
            // afisarea textului care urmeaza se prezinta a fi de culoarea ____
            SetColor(2);
                cout << endl << "-> Autentificare efectuata cu succes!" << endl << endl;
                login_successful = true;
                main();
        }

        // Conditia in care datele introduse nu se asociaza cu cele din fiserul txt
        else{
            // afisarea textului care urmeaza se prezinta a fi de culoarea ____
            SetColor(4);

                // daca datele introduse nu sunt corecte se repeta procesul de inca 5 ori
                cout << endl << "Numele de utilizator sau parola sunt introduse incorect." << endl << "Mai aveti " << remain << " incercari de efectuat!" << endl << "" << endl;
                remain--;
                login_successful = false;
            }
        }

        while (!login_successful && remain != -1);

        if (remain == -1){
            // afisarea textului care urmeaza se prezinta a fi de culoarea ____
            SetColor(12);

            // limita atinsa de incercari pentru conectare 
            cout << "Ati atins limita de incercari efectuate!" << endl << "Programul se va inchide!";
            Sleep(1);
            return 0;
        }
    }

    return 0;
}


