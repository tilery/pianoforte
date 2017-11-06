.poi[type='station'][zoom>=15] {
  marker-clip: false;
  marker-file: url('icon/poi/railway-15.svg');
  [station='subway'] {
    marker-file: url('icon/poi/subway-15.svg');
  }
  [zoom=15] {
    marker-file: url('icon/poi/railway-11.svg');
    [station='subway'] {
      marker-file: url('icon/poi/subway-11.svg');
    }
  }
}
.poi[type='station']::label[zoom>=16] {
  text-name: '[name]';
  text-face-name: @light;
  text-size: 11;
  [zoom>=17] {
    text-size: 12;
  }
  text-wrap-width: 40;
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
