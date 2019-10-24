library(ncdf4)
library(raster)
library(rgdal)


nc <- nc_open("GRIDCRO2D.nc")   #opening in ncdf to check it out

# Grab the lat and lon from the data
lat <- raster("GRIDCRO2D.nc", varname="LAT")
meanlat <- cellStats(lat, mean)
lon <- raster("GRIDCRO2D.nc", varname="LON")
meanlon <- cellStats(lon, mean)

# Convert to points and match the lat and lons
plat <- rasterToPoints(lat)
plon <- rasterToPoints(lon)
lonlat <- cbind(plon[,3], plat[,3])

# Specify the lonlat as spatial points with projection as long/lat
lonlat <- SpatialPoints(lonlat, proj4string = CRS("+proj=longlat +datum=WGS84"))

# Need the rgdal package to project it to the original coordinate system
library("rgdal")

# My best guess at the proj4 string from the information given
mycrs <- CRS(+proj=aea +lat_1=46.66666667 +lat_2=49.33333333 +lat_0=47.8591 +lon_0=-123.1088 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs)
plonlat <- spTransform(lonlat, CRSobj = mycrs)
# Take a look
plonlat
extent(plonlat)


# Yay! Now we can properly set the coordinate information for the raster
ras <- raster("GRIDCRO2D.nc", varname = "HT")   #opening with random variable using the raster package
# Fix the projection and extent
projection(ras) <- mycrs
extent(ras) <- extent(plonlat)
# Take a look
ras
plot(ras)


# Create resampling raster grid 
ref_grid <- extent(ras)    #using the extent of the initial ncdf to create a new blank raster file
ref_grid <- raster(ref_grid)   #makign the file
res(ref_grid) <- res(ras)      #making the resolution
values(ref_grid) <- 42 # dummy values
projection(ref_grid) <- crs("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0 ")  #changing projection

ref_grid  #looking

#TURN TO SHAPEFILE 
shape <- rasterToPolygons(ref_grid)   #making big shapefile 

str(shape)  #checking 


#SAVING 
writeOGR(obj=shape, dsn=getwd(), layer = "DummyValues",  driver="ESRI Shapefile")






