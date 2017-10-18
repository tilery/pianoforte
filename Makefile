import:
	env PGHOST=/var/run/postgresql/ imposm3 import -mapping mapping.yml -read tmp/pbf/lebanon-latest.osm.pbf -connection="postgis:///overcoat" -write -overwritecache -deployproduction
deploy:
	node ~/Code/js/kosmtik/index.js deploy piano.yml --localconfig localconfig-piano.js
	node ~/Code/js/kosmtik/index.js deploy forte.yml --localconfig localconfig-forte.js
