document.getElementById("telefon").value = window.sessionStorage.getItem("telefonRetinut");
document.getElementById("email").value = window.sessionStorage.getItem("emailRetinut");
document.getElementById("prenume").value = window.sessionStorage.getItem("prenumeRetinut");
document.getElementById("nume").value = window.sessionStorage.getItem("numeRetinut");
document.getElementById("adresa").value = window.sessionStorage.getItem("adresaRetinuta");

if(window.sessionStorage.getItem("mesajTrimis") != null){
    window.sessionStorage.removeItem("mesajTrimis");
    let divSucces = document.getElementById("mesaj-trimis");
    divSucces.innerHTML="<p style=\"color:green;font-size:20px;\">Mesaj trimis cu succes!</p>";
}

function contact(){
    window.sessionStorage["telefonRetinut"]=document.getElementById("telefon").value;
    window.sessionStorage["emailRetinut"]=document.getElementById("email").value;
    window.sessionStorage["prenumeRetinut"]=document.getElementById("prenume").value;
    window.sessionStorage["numeRetinut"]=document.getElementById("nume").value;
    window.sessionStorage["adresaRetinuta"]=document.getElementById("adresa").value;

    if(document.getElementById("prenume").value != null && document.getElementById("nume").value != null && document.getElementById("email").value != null && document.getElementById("mesaj").value != null){
        window.sessionStorage["mesajTrimis"]=true;
    }
}