

let h2 = document.querySelector('h2')
var map, marker, circle;
let paradas = document.querySelector('#paradas')
let pessoas = document.querySelector('#pessoas')
var markers = L.layerGroup();
import municipios from './PE_Municipios_2022.js';
import bairros from './Bairros_RMR_Sirgas2000.js';

fetch('http://127.0.0.1:8000/bairros')
    .then(response => response.json())
    .then(data => {
        const select = document.getElementById('n_bairro_a');
        data.bairros.forEach(bairro => {
            console.log(bairro[0].trim());
            const bairroName = bairro[0].trim();  // Access the string inside the array and trim it
            const option = document.createElement('option');
            option.value = bairroName;
            option.text = bairroName;
            select.appendChild(option);
        });
    })
    .catch(error => console.error('Error:', error));

document.getElementById('pessoas').addEventListener('click', function () {
    var idade_min = document.getElementById('idade_min').value;
    var idade_max = document.getElementById('idade_max').value;
    var sexo = document.querySelector('input[name="sexo"]:checked').value;
    var deficiencia = document.querySelector('select[name="deficiencia"]').value;
    var n_bairro_a = document.getElementById('n_bairro_a').value;


    var url = new URL('http://localhost:8000/dados');
    var params = { sexo: sexo, tipo_defic: deficiencia, idade_min: idade_min, idade_max: idade_max, n_bairro_a: n_bairro_a };
    url.search = new URLSearchParams(params).toString();


    fetch(url)
        .then(response => response.json())
        .then(data => {

            markers.clearLayers();


            data.data.forEach(item => {
                var marker = L.marker([item[3], item[4]]);
                markers.addLayer(marker);
            });


            markers.addTo(map);
        })
        .catch(error => console.error('Error:', error));
});

function sucess(pos) {
    console.log(pos.coords.latitude, pos.coords.longitude)
    h2.textContent = `Latitude: ${pos.coords.latitude} Longitude: ${pos.coords.longitude}`

    if (map === undefined) {
        initializeMap(pos.coords.latitude, pos.coords.longitude);
    } else {
        map.remove()
        initializeMap(pos.coords.latitude, pos.coords.longitude);
    }
    L.marker([pos.coords.latitude, pos.coords.longitude], {icon: L.divIcon({className: 'css-icon', html: '<div class="gps_ring"></div>'})}).addTo(map);
    var circle = L.circle([pos.coords.latitude, pos.coords.longitude], {
        color: 'red',      // Define a cor da borda do círculo
        fillColor: '#f03', // Define a cor de preenchimento do círculo
        fillOpacity: 0.1,  // Define a opacidade do preenchimento do círculo
        radius: 450        // Define o raio do círculo em metros
    }).addTo(map);
    fetch('http://localhost:8000/ponibus')
    .then(response => response.json())
    .then(data => {
        data.data.forEach(item => {
            // Extrai as coordenadas do ponto
            var pointCoords = item[0].replace("POINT (", "").replace(")", "").split(" ").map(Number).reverse();

            // Cria um objeto LatLng para o ponto
            var point = L.latLng(pointCoords);

            // Calcula a distância entre o ponto e o centro do círculo
            var distance = circle.getLatLng().distanceTo(point);

            // Verifica se o ponto está dentro do círculo
            if (distance <= circle.getRadius()) {
                var marker = L.marker(pointCoords);
                markers.addLayer(marker);
            }
        });

        markers.addTo(map);
    })
    .catch(error => console.error('Error:', error));
}




var municipiosLayer = L.geoJson(municipios);
var bairrosLayer = L.geoJson(bairros);

function initializeMap(latitude, longitude) {
    map = L.map('map').setView([latitude, longitude], 16);
    markers.clearLayers();


    var baseLayers = {
        "OpenStreetMap": L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }),

    };


    var overlayLayers = {
        "Municipios": municipiosLayer,
        "Bairros": bairrosLayer,
        // Adicione aqui outras camadas de sobreposição se necessário
    };

    // Adiciona as camadas de base e de sobreposição ao mapa
    L.control.layers(baseLayers, overlayLayers).addTo(map);

    // Adiciona a camada de base padrão ao mapa
    baseLayers["OpenStreetMap"].addTo(map);

    // ... código restante ...
}

// ... código restante ...

function error(erro) {
    console.log(erro)
}


//var PE_Municipios_2022 = L.geoJson(PE_Municipios_2022).addTo(map);

var watchID = navigator.geolocation.watchPosition(sucess, error, {
    enableHighAccuracy: true,
    timeout: 5000,
})





