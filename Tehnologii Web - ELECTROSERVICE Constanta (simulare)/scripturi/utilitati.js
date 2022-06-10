function obtineCodImagineLatime(a){
  if(typeof(a)!="number")
      return;
  return a%5;
}
function obtineCodImagineInaltime(a){
  if(typeof(a)!="number")
      return;
  return (a/5)%4;
}

function formatareTitlu(raspunsJSON){
  let numeScurtat = raspunsJSON.name.length > 20 ? raspunsJSON.name.substring(0,20)+"..." : raspunsJSON.name;
  return numeScurtat.charAt(0).toUpperCase() + numeScurtat.slice(1);
}

function formatareDescriere(raspunsJSON){
  let descScurtat = raspunsJSON.name.body > 270 ? raspunsJSON.name.substring(0,270)+"..." : raspunsJSON.body;
  let linii  = descScurtat.split(/\r\n|\r|\n/);
  if(linii.length > 4){
    descScurtat = "";
    let nrMaxLinii = 4;
    for(let i = 0; i < nrMaxLinii; i++)
      if(linii[i].length > 65){//approx 270 impartit la 4
        nrMaxLinii -= (linii[i].length / 65) + 1;
        if(i == nrMaxLinii - 1)
          linii[i] = linii[i].substring(65) + "...";
      }
      descScurtat += linii[i] + '\n';
  }
  return descScurtat.charAt(0).toUpperCase() + descScurtat.slice(1);
}