document.getElementById("adresa").value = window.sessionStorage.getItem("adresaRetinuta");

if(window.sessionStorage.getItem("mesajTrimis") != null){
    window.sessionStorage.removeItem("mesajTrimis");
    let divSucces = document.getElementById("mesaj-trimis");
    divSucces.innerHTML="<p style=\"color:green;font-size:20px;\">Mesaj trimis cu succes!</p>";
}
function abonare(){
    window.sessionStorage["adresaRetinuta"]=document.getElementById("adresa").value;
    if(document.getElementById("adresa").value != null){
        window.sessionStorage["mesajTrimis"]=true;
    }
}