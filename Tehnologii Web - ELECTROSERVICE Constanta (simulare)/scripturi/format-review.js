const sursa = document.getElementById("sursa");
continutSursa = sursa.innerHTML;
sursa.innerHTML = "";
const tinta = document.getElementById("tinta");

listaReviews = JSON.parse(window.localStorage.getItem("reviews"));
var versiuneSite = obtinereVersiuneSite();
if(listaReviews == null || window.localStorage.getItem("versiune") != versiuneSite){
    //alert("citirea s-a efectuat din server")
    updateListaReviews();
    updateLocalStorage(versiuneSite);
}
//else alert("citirea s-a efectuat din localstorage")

function updateLocalStorage(versiuneSite){
    window.localStorage["reviews"]=JSON.stringify(listaReviews);
    window.localStorage["versiune"]=versiuneSite;
}

function randareReview(i){
    for(; i < listaReviews.length; i++){
        tinta.innerHTML = tinta.innerHTML + continutSursa;
        elemente = document.getElementsByClassName("container-review");
        if(i%2)
            elemente[i].setAttribute("class", "fundal-gray-800 container-review");
        else elemente[i].setAttribute("class", "fundal-gray-700 container-review");
    
        elemente = document.getElementsByClassName("titlu");
        elemente[i].innerText = listaReviews[i].titlu;
        elemente = document.getElementsByClassName("descriere");
        elemente[i].innerText = listaReviews[i].descriere;
    
        elemente = document.getElementById("pozitie_neasignata");
        elemente.removeAttribute("id");
        elemente.setAttribute("class", "imagine pozitie-"+listaReviews[i].imagine_w+"w-"+listaReviews[i].imagine_h+"h");
    }
}

randareReview(0);