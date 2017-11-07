#station[type='bus_stop'][zoom>=18],
#station[type='station'][zoom>=15] {
  marker-clip: false;
  marker-file: url('icon/poi/railway-15.svg');
  [station='subway'] {
    marker-file: url('icon/poi/subway-15.svg');
  }
  [type='bus_stop'] {
    marker-file: url('icon/poi/bus_stop-15.svg');
  }
  [zoom=15] {
    marker-file: url('icon/poi/railway-11.svg');
    [station='subway'] {
      marker-file: url('icon/poi/subway-11.svg');
    }
    [type='bus_stop'] {
      marker-file: url('icon/poi/bus_stop-11.svg');
    }
  }
}

#aoi[type='courthouse'][zoom>=17],
#poi[type='courthouse'][zoom>=17],
#aoi[type='embassy'][zoom>=17],
#poi[type='embassy'][zoom>=17],
#aoi[type='university'][zoom>=16],
#poi[type='university'][zoom>=16],
#aoi[type='school'][zoom>=16],
#poi[type='school'][zoom>=16],
#aoi[type='police'][zoom>=16],
#poi[type='police'][zoom>=16],
#aoi[type='government'][zoom>=16],
#poi[type='government'][zoom>=16],
#aoi[type='fire_station'][zoom>=16],
#poi[type='fire_station'][zoom>=16],
#aoi[type='hospital'][zoom>=16],
#poi[type='hospital'][zoom>=16],
#aoi[type='townhall'][zoom>=14],
#poi[type='townhall'][zoom>=14] {
    marker-file: url('icon/poi/[type]-15.svg');
    [zoom<=15] {
      marker-file: url('icon/poi/[type]-11.svg');
    }
}

#aoi::label[type='courthouse'][zoom>=17],
#poi::label[type='courthouse'][zoom>=17],
#aoi::label[type='school'][zoom>=17],
#poi::label[type='school'][zoom>=17],
#aoi::label[type='embassy'][zoom>=17],
#poi::label[type='embassy'][zoom>=17],
#aoi::label[type='police'][zoom>=17],
#poi::label[type='police'][zoom>=17],
#aoi::label[type='government'][zoom>=17],
#poi::label[type='government'][zoom>=17],
#aoi::label[type='fire_station'][zoom>=17],
#poi::label[type='fire_station'][zoom>=17],
#aoi::label[type='hospital'][zoom>=16],
#poi::label[type='hospital'][zoom>=16],
#aoi::label[type='university'][zoom>=16],
#poi::label[type='university'][zoom>=16],
#aoi::label[type='townhall'][zoom>=15],
#poi::label[type='townhall'][zoom>=15],
#station::label[type='bus_stop'][zoom>=18],
#station::label[type='station'][station!='subway'][zoom>=15],
#station::label[type='station'][zoom>=16] {
  text-name: '[name]';
  text-face-name: @light;
  text-size: 11;
  [zoom>=17] {
    text-size: 12;
  }
  text-wrap-width: 60;
  text-fill: @poi_text;
  text-halo-fill: @halo;
  text-dy: 12;
  text-dx: 12;
  text-placement: point;
  text-halo-radius: 1.5;
  text-label-position-tolerance: 18;
  text-placement-type: simple;
  text-placements: 'S,N,W,E';
  text-avoid-edges: true;
  text-clip: false;
  text-character-spacing: 0;
}
