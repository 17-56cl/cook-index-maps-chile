
# -*- coding: UTF-8 -*-
import xlrd
import folium
import pandas
import json
import os
import io
from bs4 import BeautifulSoup
import re


def main(mouseover):

	# Nombre para guardar el nuevo mapa creado
	nombreMapa = "../../maps/Cook_Index.html"

	#Usamos pandas para leer el Excel y guardar la info en un DataFrame
	datosComunas = pandas.ExcelFile("../../data/plantilla_static_maps1756.xlsx", encoding="utf-8")
	datosCook = datosComunas.parse("plantilla_static_maps1756", parse_cols = 'J:K')

	# Imprimir lo importado del excel para ver que todo esté bien
	def print_full(x):
		pandas.set_option('display.max_rows', len(x))
		print(x)
		pandas.reset_option('display.max_rows')

	print_full(datosCook)

	# Creamos una instancia de Folium y le damos toda la info
	map_osm = folium.Map(location=[-33.47, -70.91],zoom_start=7)

	map_osm.choropleth(geo_path="../../geojson/[Agregado cook] Comunas Chile Final.json", data=datosCook,
				 columns=['COD_COMUNA','Cook'],
				 key_on='properties.COD_COMUNA',
				 fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2,
				 legend_name='Cook Partisan Voting Index')

	# Guardamos el mapa en un archivo html
	map_osm.save(nombreMapa)

	if mouseover:
		agregarMouseover(nombreMapa)


def agregarDatosAGeoJsonComunas(nombreGeojson, dfDatos, nombreDatos = "Cook" ):
	dfDatos = dfDatos.set_index("COD_COMUNA")
	print dfDatos

	with open(nombreGeojson) as json_file:
		json_decoded = json.load(json_file)

	for val in json_decoded['features']:
		cod_comuna =  val['properties']['COD_COMUNA']

		if cod_comuna != 0:
			val['properties'][nombreDatos] = str(dfDatos.loc[cod_comuna][nombreDatos])

	with open("[Agregado "+nombreDatos+"] "+nombreGeojson, 'w') as f:
			json.dump(json_decoded, f)

# Este método agrega mouseover al mapa creado por folium. Lo hace
# en base en las instrucciones de esta página: http://leafletjs.com/examples/choropleth/
# dede que dice "Adding Interaction" y sin incluir "Custom Legend Control"
# (la leyenda la crea folium por defecto)
# Resumen: Folium transforma código Python a LeafletJS. Como no ha implementado interactividad
# lo agregamos a mano
def agregarMouseover(rutaHtml):
	
    print("Agregando Mouseover...")
    with open(rutaHtml) as inf:
		txt = inf.read()

	# Tenemos que encontrar el nombre que le da folium al mapa (de la forma 'map_38e2871dd8654d49ba30ce8a329d9d1e')
    map_id = re.search(r'\bmap_\w+', txt)
    map_id = map_id.group(0)

    print("Nombre mapa: "+map_id)

    textToReplace = """FeatureCollection"}"""
    newText = """FeatureCollection"}, {
    onEachFeature: onEachFeature}"""

    if textToReplace in txt:
        print("1.- Encontrado Feature Collection!")
        txt = txt.replace(textToReplace,newText)
    else:
        print("ERROR con Feature Collection!")

    textToReplace = """.text('');"""

    newText = """
				    function highlightFeature(e) {
				    var layer = e.target;

				    layer.setStyle({
				        weight: 5,
				        color: '#666',
				        dashArray: '',
				        fillOpacity: 1
				    });

				    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
				        layer.bringToFront();
				    }

				    info.update(layer.feature.properties);

				}

				function resetHighlight(e) {
				    var layer = e.target;

				    layer.setStyle({
				        weight: 1,
				        color: '#666',
				        dashArray: '',
				        fillOpacity: 0.7,
				        opacity: 1
				    });
				    info.update();
				}

				function zoomToFeature(e) {
				    map.fitBounds(e.target.getBounds());
				}

				function onEachFeature(feature, layer) {
				    layer.on({
				        mouseover: highlightFeature,
				        mouseout: resetHighlight,
				        click: zoomToFeature
				    });
				}


				var info = L.control();

				info.onAdd = function (map) {
				    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
				    this.update();
				    return this._div;
				};


				// method that we will use to update the control based on feature properties passed
				info.update = function (props) {
				    this._div.innerHTML = '<h4>Cook Index:</h4>' +  (props ?
				        '<b>' + props.NOM_COM + '</b><br />' + props.Cook        : 'Pasa el mouse por las comunas');
				};

				info.addTo("""+map_id+""");
				</script></html>
				"""

    if textToReplace in txt:
        print("2.- Encontrado"+textToReplace)
        txt = txt.replace(textToReplace,newText)
    else:
        print("ERROR encontrando"+textToReplace)

    soup = BeautifulSoup(txt, "lxml")

	# Replace FeatureCollection"} with FeatureCollection"}, {
    # onEachFeature: onEachFeature
    # }

    cssMouseover = """
	<style>
	.info {
	    padding: 6px 8px;
	    font: 14px/16px Arial, Helvetica, sans-serif;
	    background: white;
	    background: rgba(255,255,255,0.8);
	    box-shadow: 0 0 15px rgba(0,0,0,0.2);
	    border-radius: 5px;
	}
	.info h4 {
	    margin: 0 0 5px;
	    color: #777;
	}

	.legend {
	    line-height: 18px;
	    color: #555;
	}
	.legend i {
	    width: 18px;
	    height: 18px;
	    float: left;
	    margin-right: 8px;
	    opacity: 0.7;
	}
	</style>
	"""

    soup.head.append(BeautifulSoup(cssMouseover, 'html.parser'))

    with open(rutaHtml, "w") as outf:
    	outf.write(str(soup))


# Este método toma un Geojson recien convertido de los Shapefiles bajados de la libreria del congreso y lo arregla
# Con false no crea un nuevo archivo. Solo imprime a consola para debuggear.
# Ejemplo: actualizarCodigosJson("geojson/[Sin arreglar] Comunas Chile - Geojson.json", False)
# rutaGeoJson: Es el archivo convertido de los Shapefiles de la libreria del congreso: http://www.bcn.cl/siit/mapas_vectoriales/index_html
# Son específicamente los a nivel comunal: http://www.bcn.cl/obtienearchivo?id=repositorio/10221/10396/1/division_comunal.zip
def actualizarCodigosJson(rutaGeoJson,cambiarDatos = False):
	with open(rutaGeoJson) as json_file:
		json_decoded = json.load(json_file)

	i=0
	codigos = []
	indexZona = -1

	for val in json_decoded['features']:
		comuna = val['properties']['NOM_COM'].encode('utf-8')
		cod_comuna =  val['properties']['COD_COMUNA']

		nuevo_cod = 0
		if comuna == "Puerto Montt":
			nuevo_cod = 10101
		if comuna == "Calbuco":
			nuevo_cod =	10102
		if comuna == "Cochamó":
			nuevo_cod =	10103
		if comuna == "Fresia":
			nuevo_cod =	10104
		if comuna == "Frutillar":
			nuevo_cod =	10105
		if comuna == "Los Muermos":
			nuevo_cod =	10106
		if comuna == "Llanquihue":
			nuevo_cod =	10107
		if comuna == "Maullín":
			nuevo_cod =	10108
		if comuna == "Puerto Varas":
			nuevo_cod =	10109
		if comuna == "Castro":
			nuevo_cod =	10201
		if comuna == "Ancud":
			nuevo_cod =	10202
		if comuna == "Chonchi":
			nuevo_cod =	10203
		if comuna == "Curaco de Vélez":
			nuevo_cod =	10204
		if comuna == "Dalcahue":
			nuevo_cod =	10205
		if comuna == "Puqueldón":
			nuevo_cod =	10206
		if comuna == "Queilén":
			nuevo_cod =	10207
		if comuna == "Quellón":
			nuevo_cod =	10208
		if comuna == "Quemchi":
			nuevo_cod =	10209
		if comuna == "Quinchao":
			nuevo_cod =	10210
		if comuna == "Osorno":
			nuevo_cod =	10301
		if comuna == "Puerto Octay":
			nuevo_cod =	10302
		if comuna == "Purranque":
			nuevo_cod =	10303
		if comuna == "Puyehue":
			nuevo_cod =	10304
		if comuna == "Río Negro":
			nuevo_cod =	10305
		if comuna == "San Juan de la Costa":
			nuevo_cod =	10306
		if comuna == "San Pablo":
			nuevo_cod =	10307
		if comuna == "Chaitén":
			nuevo_cod =	10401
		if comuna == "Futaleufú":
			nuevo_cod =	10402
		if comuna == "Hualaihué":
			nuevo_cod =	10403
		if comuna == "Palena":
			nuevo_cod =	10404
		if comuna == "Coyhaique":
			nuevo_cod =	11101
		if comuna == "Lago Verde":
			nuevo_cod =	11102
		if comuna == "Aysén":
			nuevo_cod =	11201
		if comuna == "Cisnes":
			nuevo_cod =	11202
		if comuna == "Guaitecas":
			nuevo_cod =	11203
		if comuna == "Cochrane":
			nuevo_cod =	11301
		if comuna == "O'Higgins":
			nuevo_cod =	11302
		if comuna == "Tortel":
			nuevo_cod =	11303
		if comuna == "Chile Chico":
			nuevo_cod =	11401
		if comuna == "Río Ibáñez":
			nuevo_cod =	11402
		if comuna == "Punta Arenas":
			nuevo_cod =	12101
		if comuna == "Laguna Blanca":
			nuevo_cod =	12102
		if comuna == "Río Verde":
			nuevo_cod =	12103
		if comuna == "San Gregorio":
			nuevo_cod =	12104
		if comuna == "Cabo de Hornos":
			nuevo_cod =	12201
		if comuna == "Porvenir":
			nuevo_cod =	12301
		if comuna == "Primavera":
			nuevo_cod =	12302
		if comuna == "Timaukel":
			nuevo_cod =	12303
		if comuna == "Natales":
			nuevo_cod =	12401
		if comuna == "Torres del Paine":
			nuevo_cod =	12402
		if comuna == "Santiago":
			nuevo_cod =	13101
		if comuna == "Cerrillos":
			nuevo_cod =	13102
		if comuna == "Cerro Navia":
			nuevo_cod =	13103
		if comuna == "Conchalí":
			nuevo_cod =	13104
		if comuna == "El Bosque":
			nuevo_cod =	13105
		if comuna == "Estación Central":
			nuevo_cod =	13106
		if comuna == "Huechuraba":
			nuevo_cod =	13107
		if comuna == "Independencia":
			nuevo_cod =	13108
		if comuna == "La Cisterna":
			nuevo_cod =	13109
		if comuna == "La Florida":
			nuevo_cod =	13110
		if comuna == "La Granja":
			nuevo_cod =	13111
		if comuna == "La Pintana":
			nuevo_cod =	13112
		if comuna == "La Reina":
			nuevo_cod =	13113
		if comuna == "Las Condes":
			nuevo_cod =	13114
		if comuna == "Lo Barnechea":
			nuevo_cod =	13115
		if comuna == "Lo Espejo":
			nuevo_cod =	13116
		if comuna == "Lo Prado":
			nuevo_cod =	13117
		if comuna == "Macul":
			nuevo_cod =	13118
		if comuna == "Maipú":
			nuevo_cod =	13119
		if comuna == "Ñuñoa":
			nuevo_cod =	13120
		if comuna == "Pedro Aguirre Cerda":
			nuevo_cod =	13121
		if comuna == "Peñalolén":
			nuevo_cod =	13122
		if comuna == "Providencia":
			nuevo_cod =	13123
		if comuna == "Pudahuel":
			nuevo_cod =	13124
		if comuna == "Quilicura":
			nuevo_cod =	13125
		if comuna == "Quinta Normal":
			nuevo_cod =	13126
		if comuna == "Recoleta":
			nuevo_cod =	13127
		if comuna == "Renca":
			nuevo_cod =	13128
		if comuna == "San Joaquín":
			nuevo_cod =	13129
		if comuna == "San Miguel":
			nuevo_cod =	13130
		if comuna == "San Ramón":
			nuevo_cod =	13131
		if comuna == "Vitacura":
			nuevo_cod =	13132
		if comuna == "Puente Alto":
			nuevo_cod =	13201
		if comuna == "Pirque":
			nuevo_cod =	13202
		if comuna == "San José de Maipo":
			nuevo_cod =	13203
		if comuna == "Colina":
			nuevo_cod =	13301
		if comuna == "Lampa":
			nuevo_cod =	13302
		if comuna == "Tiltil":
			nuevo_cod =	13303
		if comuna == "San Bernardo":
			nuevo_cod =	13401
		if comuna == "Buin":
			nuevo_cod =	13402
		if comuna == "Calera de Tango":
			nuevo_cod =	13403
		if comuna == "Paine":
			nuevo_cod =	13404
		if comuna == "Melipilla":
			nuevo_cod =	13501
		if comuna == "Alhué":
			nuevo_cod =	13502
		if comuna == "Curacaví":
			nuevo_cod =	13503
		if comuna == "María Pinto":
			nuevo_cod =	13504
		if comuna == "San Pedro":
			nuevo_cod =	13505
		if comuna == "Talagante":
			nuevo_cod =	13601
		if comuna == "El Monte":
			nuevo_cod =	13602
		if comuna == "Isla de Maipo":
			nuevo_cod =	13603
		if comuna == "Padre Hurtado":
			nuevo_cod =	13604
		if comuna == "Peñaflor":
			nuevo_cod =	13605
		if comuna == "Valdivia":
			nuevo_cod =	14101
		if comuna == "Corral":
			nuevo_cod =	14102
		if comuna == "Lanco":
			nuevo_cod =	14103
		if comuna == "Los Lagos":
			nuevo_cod =	14104
		if comuna == "Máfil":
			nuevo_cod =	14105
		if comuna == "Mariquina":
			nuevo_cod =	14106
		if comuna == "Paillaco":
			nuevo_cod =	14107
		if comuna == "Panguipulli":
			nuevo_cod =	14108
		if comuna == "La Unión":
			nuevo_cod =	14201
		if comuna == "Futrono":
			nuevo_cod =	14202
		if comuna == "Lago Ranco":
			nuevo_cod =	14203
		if comuna == "Río Bueno":
			nuevo_cod =	14204
		if comuna == "Arica":
			nuevo_cod =	15101
		if comuna == "Camarones":
			nuevo_cod =	15102
		if comuna == "Putre":
			nuevo_cod =	15201
		if comuna == "General Lagos":
			nuevo_cod =	15202

		if nuevo_cod != 0:
			val['properties']['COD_COMUNA'] = nuevo_cod
			codigos.append(nuevo_cod)

		if nuevo_cod == 0:
			codigos.append(cod_comuna)

		# Eliminar la Zona Sin Demarcar
		if cod_comuna == 0:
			indexZona = i

		i = i + 1

	if indexZona >= 0:
		del json_decoded['features'][indexZona]
	
	if cambiarDatos:
		with open("../../geojson/NuevosCodigos2.json", 'w') as f:
			json.dump(json_decoded, f)


	codigos.sort()
	print codigos
	print "Numero de comunas geojson: "+str(i)

if __name__ == '__main__':
	#datosComunas = pandas.ExcelFile("plantilla_static_maps1756.xlsx", encoding="utf-8")
	#datosCook = datosComunas.parse("plantilla_static_maps1756", parse_cols = 'J:K')
	#agregarDatosAGeoJsonComunas("geojson/NuevosCodigos2.json",datosCook)
	main(False)


