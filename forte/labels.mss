/* ************************* */
/*          PLACE            */
/* ************************* */
#place[type='city'],
#place[type='town'],
#place[type='village'][zoom>=9] {
  text-name: '[name]';
  [lang='fr'] {
    text-name: '[name].replace("Saint-", "St-").replace("Sainte-", "Ste-")';
  }
  text-face-name: @light;
  text-placement: point;
  text-fill: @village_text;
  text-size: 12;
  text-halo-fill: @halo;
  text-halo-radius: 2;
  text-wrap-width: 40;
  text-label-position-tolerance: 20;
  text-character-spacing: 0.1;
  text-line-spacing: -2;
  [type='town'] {
    text-fill: @town_text;
    text-face-name: @regular;
  }
  [type='city'] {
    text-fill: @city_text;
    text-face-name: @medium;
  }
  [zoom<12] {
    text-min-distance: 30;
    text-min-padding: 1;
  }
  [zoom=12] {
    text-size: 13;
    [type='city'] {
      text-size: 14;
    }
  }
  [zoom>=13] {
    text-size: 14;
    [type='city'] {
      text-size: 15;
    }
  }
  [zoom>=14] {
    text-size: 15;
  }
}

#landuse_label[type='forest'][zoom=12],
#landuse_label[type='park'][zoom=12],
#landuse_label[type='residential'][zoom=12],
#landuse_label[type='commercial'][zoom=12],
#landuse_label[type='industrial'][zoom=12],
#landuse_label[type='wood'][zoom=12],
#landuse_label[zoom>=13] {
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
  text-wrap-width: 30;
  text-label-position-tolerance: 20;
  text-character-spacing: 0.1;
  text-line-spacing: -2;
  [zoom>=14] {
    text-size: 12;
  }
}
