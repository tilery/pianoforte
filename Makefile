import:
	env PGHOST=/var/run/postgresql/ imposm3 import -config imposm.conf -diff -read tmp/pbf/senegal-and-gambia-latest.osm.pbf -write -overwritecache -deployproduction
update:
	env PGHOST=/var/run/postgresql/ imposm3 run -config imposm.conf
deploy:
	node ~/Code/js/kosmtik/index.js deploy forte.yml --localconfig localconfig-forte.js
	node ~/Code/js/kosmtik/index.js deploy piano.yml --localconfig localconfig-piano.js
