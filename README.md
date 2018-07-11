# Piano-Forte

A world map in two flavours:

- Piano, when you need a very light background to put data on top of if
- Forte, when you need a generic purpose map


##  Forte

![screenshot from 2017-10-02 09-33-18](https://user-images.githubusercontent.com/146023/31072322-af868880-a767-11e7-8981-3d0bd8403cc8.png)
![screen shot 2017-10-31 at 18 50 50-fullpage](https://user-images.githubusercontent.com/146023/32240046-837f0386-be6c-11e7-813d-82bde3b35384.png)

## Piano

![screenshot from 2016-08-23 08-50-12](https://cloud.githubusercontent.com/assets/146023/17882745/bde02780-690e-11e6-9c8e-d422a8753956.png)
![screenshot from 2016-08-23 08-51-19](https://cloud.githubusercontent.com/assets/146023/17882746/bde0200a-690e-11e6-9e71-82482f118a54.png)


## Dependencies

* Python >= 3.6.x
* Gdal >= 2.2.x


## Local installation

Create a `pianoforte` PSQL database:

    sudo -u postgres createdb pianoforte -O youruser

Clone this repository:

    git clone https://github.com/tilery/pianoforte

Compile the world boundaries:

    make boundary

Download the PBF from Geofabrik:

    make download

Note: you can use another area by setting the `PBF` env var to the Geofabrik
relative path (default is: africa/egypt-latest.osm.pbf).

Import the PBF and the boundaries into the database:

    make import

Copy the localconfig sample, and change the db configuration inside:

    cp localconfig.js.sample localconfig.js

Run kosmtik with forte:

    kosmtik serve forte.yml

Or with piano:

    kosmtik serve piano.yml


## Remote deployment


See [pianoforte-deploy](https://github.com/tilery/pianoforte-deploy).
