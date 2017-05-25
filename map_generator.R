#Shapefiles..
library(ggplot2)
library(plotly)

filename="1756Shp/division_comunal_1756-2.shp"
geodata=readShapeSpatial(filename)
datos=read.csv("plantilla_static_maps1756.csv")
datos$Cook[datos$Cook>12]=12 #Limitar Cook Index a máximo 12
geodata@data=data.frame(geodata@data,datos[match(geodata@data[,"COD_COM2"],datos[,"COD_COMUNA"]),])
geodata@data$ï..comunas=NULL


######Common GGPPLOT Format
opt1=scale_fill_gradient2(low = "red3",high = "blue3",limits=c(-12,12),midpoint=0,
		labels=c("Nueva Mayoría","Distrito balanceado","Chile Vamos"),breaks=c(-10,0,10))
opt2=theme(axis.line=element_blank(),axis.text.x=element_blank(),
        	axis.text.y=element_blank(),
        	axis.title.x=element_blank(),
        	axis.title.y=element_blank())
opt3=labs(fill = "Predominancia")
opt4=geom_path(color = "black",size=0.1)
#########################################################################
#########################################################################


####Todo Chile excepto IdP, JF y Antártica
geodata@data$id <- rownames(geodata@data)
shapefile_df <- fortify(geodata,region="id")
shapefile_df2 <- merge(shapefile_df, geodata@data, by = "id")
shapefile_df3=shapefile_df2[-which(shapefile_df2$NOM_COM=="Isla de Pascua"),] ###Eliminar Isla de Pascua
shapefile_df4=shapefile_df3[-which(shapefile_df3$NOM_COM=="Juan Fernández"),] 
mapChile<- ggplot(data = shapefile_df4, aes(x = long, y = lat, group = group, fill=Cook))+geom_polygon()+ 
		ggtitle("Índice de Cook de predominancia política \nChile Continental - Distritos Electorales")+
		opt1+opt2+opt3+opt4

#################################
#####Regiones 15 y 1:
subgeodata_15y1=geodata[which(geodata$NOM_REG == "Región de Arica y Parinacota" |geodata$NOM_REG == "Región de Tarapacá" ),]
subgeodata_15y1@data$id <- rownames(subgeodata_15y1@data)
shapefile_df_15y1 <- fortify(subgeodata_15y1,region="id")
shapefile_df_15y1id <- merge(shapefile_df_15y1, subgeodata_15y1@data, by = "id")
map15y1 <- ggplot(data = shapefile_df_15y1id, aes(x = long, y = lat, group = group, fill=Cook))+geom_polygon()+
		ggtitle("Índice de Cook de predominancia política \nRegiones XV y I- Distritos Electorales")+
		opt1+opt2+opt3+opt4

#####Regiones 2 y 3:
subgeodata_2y3=geodata[which(geodata$NOM_REG == "Región de Atacama" | geodata$NOM_REG == "Región de Antofagasta"),]
subgeodata_2y3@data$id <- rownames(subgeodata_2y3@data)
shapefile_df_2y3 <- fortify(subgeodata_2y3,region="id")
shapefile_df_2y3id <- merge(shapefile_df_2y3, subgeodata_2y3@data, by = "id")
map2y3=ggplot(data = shapefile_df_2y3id, aes(x = long, y = lat, group = group, fill=Cook))+geom_polygon()+
		ggtitle("Índice de Cook de predominancia política \nRegiones II y III - Distritos Electorales")+
		opt1+opt2+opt3+opt4

#####Regiones 4 y 5
subgeodata_4y5=geodata[which(geodata$NOM_REG == "Región de Coquimbo"|	geodata$NOM_REG == "Región de Valparaíso"),]

subgeodata_4y5@data$id <- rownames(subgeodata_4y5@data)
shapefile_df_4y5 <- fortify(subgeodata_4y5,region="id")
shapefile_df_4y5id <- merge(shapefile_df_4y5, subgeodata_4y5@data, by = "id")
shapefile_df_4y5id=shapefile_df_4y5id[-which(shapefile_df_4y5id$NOM_COM=="Isla de Pascua"),]# 
shapefile_df_4y5id=shapefile_df_4y5id[-which(shapefile_df_4y5id$NOM_COM=="Juan Fernández"),] #esto hace fallar código
map4y5 <- ggplot(data = shapefile_df_4y5id, aes(x = long, y = lat, group = group, fill=Cook))+geom_polygon()+
		ggtitle("Índice de Cook de predominancia política \nRegiones IV y V - Distritos Electorales")+
		opt1+opt2+opt3+opt4

#####Regiones 6 y 7:
subgeodata_6y7=geodata[which(geodata$NOM_REG == "Región del Libertador Bernardo O'Higgins"|	geodata$NOM_REG == "Región del Maule"),]
subgeodata_6y7@data$id <- rownames(subgeodata_6y7@data)
shapefile_df_6y7 <- fortify(subgeodata_6y7,region="id")
shapefile_df_6y7id <- merge(shapefile_df_6y7, subgeodata_6y7@data, by = "id")
map6y7 <- ggplot(data = shapefile_df_6y7id, aes(x = long, y = lat, group = group, fill=Cook))+geom_polygon()+
		ggtitle("Índice de Cook de predominancia política \nRegiones VI y VII - Distritos Electorales")+
		opt1+opt2+opt3+opt4

#####Regiones 8 y 9:
subgeodata_8y9=geodata[which(geodata$NOM_REG == "Región del Bío-Bío"|geodata$NOM_REG == "Región de La Araucanía"),]
subgeodata_8y9@data$id <- rownames(subgeodata_8y9@data)
shapefile_df_8y9 <- fortify(subgeodata_8y9,region="id")
shapefile_df_8y9id <- merge(shapefile_df_8y9, subgeodata_8y9@data, by = "id")
map8y9 <- ggplot(data = shapefile_df_8y9id, aes(x = long, y = lat, group = group, fill=Cook))+geom_polygon()+
		ggtitle("Índice de Cook de predominancia política \nRegiones VIII y IX - Distritos Electorales")+
		opt1+opt2+opt3+opt4

#####Regiones 10 y 14:
subgeodata_10y14=geodata[which(geodata$NOM_REG == "Región de Los Ríos"|geodata$NOM_REG == "Región de Los Lagos"),]
subgeodata_10y14@data$id <- rownames(subgeodata_10y14@data)
shapefile_df_10y14 <- fortify(subgeodata_10y14,region="id")
shapefile_df_10y14id <- merge(shapefile_df_10y14, subgeodata_10y14@data, by = "id")
map10y14 <- ggplot(data = shapefile_df_10y14id, aes(x = long, y = lat, group = group, fill=Cook))+geom_polygon()+
		ggtitle("Índice de Cook de predominancia política \nRegiones X y XIV - Distritos Electorales")+
		opt1+opt2+opt3+opt4

#####Regiones 11 y 12:
subgeodata_11y12=geodata[which(geodata$NOM_REG == "Región de Aysén del Gral.Ibañez del Campo"|geodata$NOM_REG == "Región de Magallanes y Antártica Chilena"),]
subgeodata_11y12@data$id <- rownames(subgeodata_11y12@data)
shapefile_df_11y12 <- fortify(subgeodata_11y12,region="id")
shapefile_df_11y12id <- merge(shapefile_df_11y12, subgeodata_11y12@data, by = "id")
map11y12 <- ggplot(data = shapefile_df_11y12id, aes(x = long, y = lat, group = group, fill=Cook))+geom_polygon()+
		ggtitle("Índice de Cook de predominancia política \nRegiones XI y XII - Distritos Electorales")+
		opt1+opt2+opt3+opt4

#####Provincia de Stgo
subgeodata_STGO=geodata[which(geodata$NOM_PROV == "Santiago"),]
subgeodata_STGO@data$id <- rownames(subgeodata_STGO@data)
shapefile_df_STGO <- fortify(subgeodata_STGO,region="id")
shapefile_df_STGOid <- merge(shapefile_df_STGO, subgeodata_STGO@data, by = "id")
mapSTGO <- ggplot(data = shapefile_df_STGOid, aes(x = long, y = lat, group = group, fill=Cook))+geom_polygon()+
		ggtitle("Índice de Cook de predominancia política \nProvincia de Santiago - Distritos Electorales")+
		opt1+opt2+opt3+opt4

#####Solo RM
subgeodata_13=geodata[which(geodata$NOM_REG == "Región Metropolitana de Santiago"),]
subgeodata_13@data$id <- rownames(subgeodata_13@data)
shapefile_df_13 <- fortify(subgeodata_13,region="id")
shapefile_df_13id <- merge(shapefile_df_13, subgeodata_13@data, by = "id")
map13 <- ggplot(data = shapefile_df_13id, aes(x = long, y = lat, group = group, fill=Cook))+geom_polygon()+
		ggtitle("Índice de Cook de predominancia política \nRegión Metropolitana - Distritos Electorales")+
		opt1+opt2+opt3+opt4

###Interactive version
mapa15y1i <- ggplotly(map15y1)
mapa6y7i <- ggplotly(map6y7) 
map13i <- ggplotly(map13)
mapaSTGOi <- ggplotly(mapSTGO)
mapa11y12i <- ggplotly(map11y12)
mapa10y14i <- ggplotly(map10y14)
mapa4y5i <- ggplotly(map4y5)
mapa2y3i <- ggplotly(map2y3)
mapa8y9i <- ggplotly(map8y9)

library(gridExtra)
grid.arrange(map15y1,map2y3,map4y5,map6y7, ncol=4,nrow=1,bottom="",left="")
grid.arrange(map8y9,map10y14,map13,mapSTGO ,ncol=4,nrow=1,bottom="",left="")


###Saving as Images
ggsave("map15y1.jpeg",map15y1,"jpeg")
ggsave("map10y14.jpeg",map10y14,"jpeg")
ggsave("map4y5.jpeg",map4y5,"jpeg")
