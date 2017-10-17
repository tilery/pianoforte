/* ************************* */
/*          PLACE            */
/* ************************* */
#place[type='city'],
#place[type='town'],
#place[type='village'][zoom>=9] {
  text-name:'[name].replace("Saint-", "St-").replace("Sainte-", "Ste-")';
  text-face-name: @light;
  text-placement:point;
  text-fill: @village_text;
  text-size: 12;
  text-halo-fill: @village_halo;
  text-halo-radius: 2;
  text-wrap-width: 30;
  text-label-position-tolerance: 20;
  text-character-spacing: 0.1;
  text-wrap-width: 30;
  text-wrap-character: '-';
  text-repeat-wrap-character: true;  // mapnik 3.x only
  text-line-spacing: -2;
  [zoom=12] {
    text-size: 13;
  }
  [type='town'] {
    text-fill: @town_text;
    text-halo-fill: @town_halo;
    text-face-name: @medium;
  }
  [type='city'] {
    text-fill: @city_text;
    text-halo-fill: @city_halo;
    text-face-name: @medium;
    text-transform: uppercase;
  }
  [zoom<12] {
    text-min-distance: 30;
    text-min-padding: 1;
  }
  [zoom>=13] {
    text-size: 13;
  }
  [zoom>=14] {
    text-size: 14;
  }
}

