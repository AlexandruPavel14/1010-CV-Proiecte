let animatie_on = false;

let poz_w = 0;
let poz_h = 0;

window.setInterval(function(){
    if(animatie_on){
        console.log(poz_w+","+poz_h);

        poz_w += 1;
        if(poz_w > 3){
            poz_w = 0;
            poz_h++;
        }
        if(poz_h > 3){
            poz_w = 0;
            poz_h = 0;
        }
        let animatieLoading = document.getElementsByClassName("imagine-loading")[0];
        if(animatieLoading != null){
            animatieLoading.setAttribute("class", `imagine-loading pozitie-loading-${poz_w}w-${poz_h}h`)
        }
    }
}, 33.3333);//30 fps