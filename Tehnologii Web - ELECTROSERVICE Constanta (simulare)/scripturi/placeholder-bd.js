var listaReviews = [];

function updateListaReviews(){//ne imaginam ca raspunsul vine de la un server
    listaReviews = [
        new Review(0, 0, "Ce este USB 3.2 gen 2×2?","Kingston a lansat recent unul dintre cele mai mici SSD-uri de pe piata, cu o capacitate de pana la 2 TB. Am vrut sa ne convingem si noi de performantele sale, asa ca producatorul. "),
        new Review(0, 1, "Upgrade pentru setup-ul de gaming cu ASUS ROG","A venit timpul pentru un setup de gaming next level? ASUS ROG are cateva propuneri pentru gamerii care isi doresc performanta, calitate si mai ales customizare la cel mai inalt nivel. "),
        new Review(0, 2, "CES 2022: Noutati de la AMD","Anuntand lansarea a peste 10 modele de procesoare, placi video pentru desktop si mobile, dar si tehnologii de top pentru gameri. In prim plan au fost bineinteles, "),
        new Review(0, 3, "Routere ASUS cu Wi-Fi 6"," Daca iti doresti sa gestionezi mai multe dispozitive conectate simultan la retea, sa beneficiezi de optimizari pentru jocurile online sau chiar abonamentul GeForce NOW si de ce nu, sa faci si streaming de filme la rezolutie cat mai mare pe TV-ul tau smart, iti recomandam sa citesti ghidul de mai jos."),
        new Review(0, 4, "Placa de baza", "Placa de bază este chiar cea mai importantă componentă a unui calculator, tocmai de aceea este foarte importantă cunoașterea ei. Pentru a înțelege cum funcționează, este important să cunoaștem componentele și funcționalitățile acestora. Având așa multe componente ar fi destul de greu să înțelegi în detaliu fiecare părticică a ei")
    ]
}

function obtinereVersiuneSite(){//ne imaginam ca raspunsul vine de la un server
    return "1.5 BETA";
}

function incarcare(){//raspunsul vine de la un server lorem ipsum
    if(listaReviews.length < 195){//dupa 195 request-uri api-ul nu va mai raspunde
        let animatieLoading = document.getElementsByClassName("imagine-loading")[0];
        if(animatieLoading != null){
            animatieLoading.setAttribute("id", "");
            animatie_on = true;
        }
        for(let i = 0; i < 5; i++){
            $.get("https://jsonplaceholder.typicode.com/comments/" + (listaReviews.length + i),function(data){
                listaReviews.push(new Review(parseInt(obtineCodImagineInaltime(listaReviews.length + 1)), obtineCodImagineLatime(listaReviews.length + 1), formatareTitlu(data), formatareDescriere(data)));
                randareReview(listaReviews.length - 1);
                updateLocalStorage(obtinereVersiuneSite());
                animatieLoading.setAttribute("id", "div-colapsat");
                animatie_on = false;
            });
        }
    }
}