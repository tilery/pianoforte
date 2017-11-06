/* ************************* */
/*          PLACE            */
/* ************************* */
#place[type='city'],
#place[type='town'],
#place[type='village'][zoom>=9] {
  text-name:'[name].replace("Saint-", "St-").replace("Sainte-", "Ste-")';
  text-face-name: @xlight;
  text-placement:point;
  text-fill: @village_text;
  text-size: 11;
  text-halo-fill: @halo;
  text-halo-radius: 2;
  text-wrap-width: 30;
  text-label-position-tolerance: 20;
  text-character-spacing: 0.1;
  text-wrap-width: 30;
  text-wrap-character: '-';
  text-repeat-wrap-character: true;  // mapnik 3.x only
  text-line-spacing: -2;
  [zoom=12] {
    text-size: 12;
  }
  [type='town'] {
    text-fill: @town_text;
    text-halo-fill: @halo;
    text-face-name: @medium;
  }
  [type='city'] {
    text-fill: @city_text;
    text-halo-fill: @halo;
    text-face-name: @medium;
    text-transform: uppercase;
  }
  [zoom<12] {
    text-min-distance: 30;
    text-min-padding: 1;
  }
  [zoom>=13] {
    text-size: 12;
  }
  [zoom>=14] {
    text-size: 13;
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
  shield-min-distance: 20;
  shield-min-padding: 1;
  [zoom>=12] {
    shield-min-distance: 50;
  }
  [zoom>=14] {
    shield-min-distance: 100;
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
  text-min-distance: 60;
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
