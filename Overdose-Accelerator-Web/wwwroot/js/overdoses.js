// Setting up the map
let map = L.map('map').setView([47.35, -121.9], 10);

let attr_osm = 'Map data &copy; <a href="http://openstreetmap.org/">OpenStreetMap</a> contributors';
let attr_mapbox = 'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>'
let attr_overpass = 'POI via <a href="http://www.overpass-api.de/">Overpass API</a>';

const mapbox = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    maxZoom: 30,
    attribution: [attr_osm, attr_mapbox, attr_overpass].join(', '),
    id: 'mapbox/light-v9',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1Ijoibmlja2F0c3B1ciIsImEiOiJjbDNtNDdlZ3cwMHppM2ptZnVqbTNocTN3In0._Avg2W_oO-_NALJriDR7qA'
}).addTo(map);

// Buildings setup
// Layer Groups for each amenity type we want to show
const schools = L.layerGroup();
const clinics = L.layerGroup();
const hospitals = L.layerGroup();
const socialFacilities = L.layerGroup();
const fireStations = L.layerGroup();
const police = L.layerGroup();
const libraries = L.layerGroup();

// Overpass API
let overpassQuery = '(area["name"="King County"][admin_level=6]["wikipedia"="en:King County, Washington"];)->.searchArea; nwr["amenity"~"(school|clinic|hospital|social_facility|fire_station|police|library)"](area.searchArea); out geom;'

const opl = new L.OverPassLayer({
    'minZoom': 9,
    'query': overpassQuery,
    'minZoomIndicatorEnabled': true,
    'minZoomIndicatorOptions': {
        position: 'topright',
        minZoomMessageNoLayer: 'No layer assigned',
        minZoomMessage: 'Current zoom level: CURRENTZOOM - Building data at level: MINZOOMLEVEL'
    },
    'cacheEnabled': true,
    'beforeRequest': function () { console.log('Requested data with query: ' + overpassQuery); },
    'beforeRequest': function () { map.spin(true); },
    'onError': function (xhr) { console.log(xhr); map.spin(false); },
    'onTimeout': function (xhr) { console.log(xhr); map.spin(false); },
    'onSuccess': function (data) {

        for (var i = 0; i < data.elements.length; i++) {
            var e = data.elements[i];

            var pos;

            if (e.type === "node") {
                pos = new L.LatLng(e.lat, e.lon);
            } else {
                pos = new L.LatLng((e.bounds.minlat + e.bounds.maxlat) / 2, (e.bounds.minlon + e.bounds.maxlon) / 2);
            }

            var popupContent = "";
            popupContent = popupContent + "<dt>@id</dt><dd>" + e.type + "/" + e.id + "</dd>";
            var keys = Object.keys(e.tags);
            keys.forEach(function (key) {
                popupContent = popupContent + "<dt>" + key + "</dt><dd>" + e.tags[key] + "</dd>";
            });
            popupContent = popupContent + "</dl>"

            var amenityName = e.tags["amenity"];

            switch (amenityName) {
                case "school":
                case "prep_school":
                    L.circle(pos, 75, {
                        color: '#66cdaa',
                        fillColor: '#66cdaa',
                        fillOpacity: 0.5
                    }).bindPopup(popupContent).addTo(schools);
                    break;
                case "clinic":
                    L.circle(pos, 75, {
                        color: '#ff0000',
                        fillColor: '#ff0000',
                        fillOpacity: 0.5
                    }).bindPopup(popupContent).addTo(clinics);;
                    break;
                case "hospital":
                    L.circle(pos, 75, {
                        color: '#ffd700',
                        fillColor: '#ffd700',
                        fillOpacity: 0.5
                    }).bindPopup(popupContent).addTo(hospitals);;
                    break;
                case "social_facility":
                    L.circle(pos, 75, {
                        color: '#c71585',
                        fillColor: '#c71585',
                        fillOpacity: 0.5
                    }).bindPopup(popupContent).addTo(socialFacilities);;
                    break;
                case "fire_station":
                    L.circle(pos, 75, {
                        color: '#00ff00',
                        fillColor: '#00ff00',
                        fillOpacity: 0.5
                    }).bindPopup(popupContent).addTo(fireStations);
                    break;
                case "police":
                    L.circle(pos, 75, {
                        color: '#0000ff',
                        fillColor: '#0000ff',
                        fillOpacity: 0.5
                    }).bindPopup(popupContent).addTo(police);
                    break;
                case "library":
                    L.circle(pos, 75, {
                        color: '#1e90ff',
                        fillColor: '#1e90ff',
                        fillOpacity: 0.5
                    }).bindPopup(popupContent).addTo(libraries);
                    break;
                default:
                //console.log('Amenity of name ' + amenityName + ' is not configured to be added to the map.' )

                map.spin(false);
            }
        }

        // Add building layers to map
        schools.addTo(map);
        clinics.addTo(map);
        hospitals.addTo(map);
        socialFacilities.addTo(map);
        fireStations.addTo(map);
        police.addTo(map);
        libraries.addTo(map);
    },
});

// Triggers the request for OSM building data via Overpass API
opl.addTo(map);

// Adding Some Color
function getColor(d) {
    return d > 250 ? '#65001e' :
        d > 125 ? '#772245' :
            d > 50 ? '#843a60' :
                d > 25 ? '#8b476e' :
                    d > 15 ? '#985e88' :
                        d > 5 ? '#a677a5' :
                            d > 1 ? '#b999cc' :
                                '#c8b4eb';
}

function style(feature) {

    var overdosesAsInt = parseInt(feature.properties.overdoses, 10);
    if (isNaN(overdosesAsInt)) overdosesAsInt = 0;

    return {
        fillColor: getColor(overdosesAsInt),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

// global zipCodeData
L.geoJson(zipCodeData).addTo(map);

// Adding Interaction
var geojson;

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        // We don't want the layer on top of the markers
        //layer.bringToFront();
    }

    info.update(layer.feature.properties);
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
    console.log('Current zoom: ' + map.getZoom())
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);

    info.update();
}

// add the listeners on our zip code layers
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

geojson = L.geoJson(zipCodeData, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);

// Custom Info Control
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>King County Overdoses</h4>' + (props ?
        '<b>' + props.ZIPCODE + '</b><br />' + props.overdoses + ' overdoses'
        : 'Hover over a zip code');
};

info.addTo(map);

// Custom Legend Control
var legend = L.control({ position: 'bottomright' });

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 1, 5, 15, 25, 50, 125, 250],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);

// Add buildings and layer control to the map
var overlayMaps = {
    "Schools <div class='filterColor' id='schools'></div>": schools,
    "Clinics <div class='filterColor' id='clinics'></div>": clinics,
    "Hospitals <div class='filterColor' id='hospitals'></div>": hospitals,
    "Social Facilities <div class='filterColor' id='socialFacilities'></div>": socialFacilities,
    "Fire Stations <div class='filterColor' id='fireStations'></div>": fireStations,
    "Police Stations <div class='filterColor' id='policeStations'></div>": police,
    "Libraries <div class='filterColor' id='libraries'></div>": libraries
}

var controlLayer = L.control.layers(null, overlayMaps, { collapsed: false });

// Tries to fix a bug where the layer control displays multple times on the map
if (map.hasLayer(controlLayer)) {
    console.log('Control layer has already been added to the map');
} else {
    console.log('Adding buildings control layer to the map')
    controlLayer.addTo(map);
}