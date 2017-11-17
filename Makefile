import:
	env PGHOST=/var/run/postgresql/ imposm3 import -mapping mapping.yml -read tmp/pbf/nord-pas-de-calais-latest.osm.pbf -connection="postgis:///pianoforte" -write -overwritecache -deployproduction
deploy:
	node ~/Code/js/kosmtik/index.js deploy forte.yml --localconfig localconfig-forte.js
	node ~/Code/js/kosmtik/index.js deploy piano.yml --localconfig localconfig-piano.js
