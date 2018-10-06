#landuse_label_gen[type='forest'][zoom=12],
#landuse_label_gen[type='park'][zoom=12],
#landuse_label_gen[type='residential'][zoom=12],
#landuse_label_gen[type='commercial'][zoom=12],
#landuse_label_gen[type='industrial'][zoom=12],
#landuse_label_gen[type='wood'][zoom=12],
#landuse_label_gen[zoom>=13][zoom<17],
#landuse_label[zoom>=17] {
  text-name: '[name]';
  [lang='fr'] {
    text-name: '[name].replace("Saint-", "St-").replace("Sainte-", "Ste-")';
  }
  text-face-name: @light;
  text-placement: point;
  text-fill: @landuse_text;
  text-size: 11;
  text-margin: 20;
  text-halo-fill: @halo;
  text-halo-radius: 2;
  text-wrap-width: 40;
  text-label-position-tolerance: 20;
  text-character-spacing: 0.1;
  text-line-spacing: -2;
  [zoom>=14] {
    text-size: 12;
  }
}


/* ************************* */
/*          ROADS            */
/* ************************* */
#road_label::shield[type='secondary'][zoom>=13][reflen>=1][reflen<=6],
#road_label::shield[type='primary'][zoom>=12][reflen>=1][reflen<=6],
#road_label::shield[type='trunk'][zoom>=9][reflen>=1][reflen<=6],
#road_label::shield[type='motorway'][zoom>=9][reflen>=1][reflen<=6] {
  shield-name: "[ref].replace('·', '\n')";
  shield-size: 9;
  shield-line-spacing: -4;
  shield-file: url('icon/shield/road-[reflen].svg');
  shield-face-name: @xlight;
  shield-fill: #333;
  shield-spacing: 200;
  shield-margin: 20;
  shield-min-padding: 1;
  [zoom>=12] {
    shield-margin: 50;
  }
  [zoom>=14] {
    shield-margin: 100;
    shield-transform: scale(1.25,1.25);
    shield-size: 11;
  }
}

#road_label[type='living_street'][zoom>=14],
#road_label[type='residential'][zoom>=14],
#road_label[type='unclassified'][zoom>=14],
#road_label[type='service'][zoom>=14],
#road_label[type='secondary'][zoom>=14],
#road_label[type='tertiary'][zoom>=14],
#road_label[type='primary'][zoom>=14],
#road_label[type='trunk'][zoom>=14],
#road_label[type='motorway'][zoom>=13] {
  text-name: '[name].replace("^Chemin", "Ch.").replace("^Avenue", "Av.").replace("^Rue", "R.").replace("^Route", "Rte").replace("^Boulevard", "Bd")';
  text-face-name: @xlight;
  text-placement: line;
  text-size: 10;
  text-fill: @road_text;
  text-halo-fill: @halo;
  text-halo-radius: 2;
  text-margin: 60;
  text-size: 11;
  text-avoid-edges: true;
  text-character-spacing: 0;
  [zoom=16] {
      text-size: 11;
  }
  [zoom>=17] {
      text-size: 12;
  }
}
