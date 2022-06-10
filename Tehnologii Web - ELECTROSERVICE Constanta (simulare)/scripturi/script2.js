/*
Începem codul nostru cu o solicitare ajax pentru a prelua datele
din fișierul json.
*/
// Mai întâi creez un nou obiect xmlhttp-request
let http = new XMLHttpRequest();
// variabila http deține acum toate metodele și proprietățile obiectului.

//  apoi pregătesc cererea cu metoda open().
http.open('get', 'products.json', true);
// primul argument stabilește metoda http.
// în al doilea argument trecem fișierul în care se află datele noastre.
// iar ultimul cuvânt cheie true, setează cererea să fie asincronă.

// in continuare voi trimite cererea.
http.send();

// Acum trebuie identificat răspunsul.
// voi verifica onload eventlistener.
http.onload = function(){
	// În interiorul funcției, trebuie să verific proprietățile readystate și stare.
	if(this.readyState == 4 && this.status == 200){
		// dacă avem un răspuns de succes, trebuie să analizez datele json
		// și convertiți-le într-o matrice javascript.
		let products = JSON.parse(this.responseText);

		// Apoi avem nevoie de o variabilă fara valoare pentru a adăuga datele primite.
		let output = "";

		// acum trebuie să parcurg produsele și în fiecare iterație
		// adaug un șablon html la variabila de ieșire.
		for(let item of products){
			output += `
				<div class="product">
					<img src="${item.image}" alt="${item.description}">
					<p class="title">${item.title}</p>
					<p class="description">${item.description}</p>
					<p class="price">
						<span>De la ${item.price} RON</span>
					</p>
					<p class="cart"><Add to cart <i class="bx bx-cart-alt"></i></p>
				</div>
			`;
		}
		/* și la sfârșit țintesc containerul de produse și adaug datele pe care
		variabila de ieșire se menține. */
		document.querySelector(".products").innerHTML = output;
		
	}
} 