/* ************************* */
/*          PLACE            */
/* ************************* */
#country[zoom>=3][zoom<=7] {
  text-name: '[name]';
  text-face-name: @bold;
  text-placement: point;
  text-fill: @country_text;
  text-size: 14;
  text-halo-fill: @halo;
  text-halo-radius: 2;
  text-wrap-width: 40;
  text-label-position-tolerance: 20;
  text-character-spacing: 1;
}
#place_low[type='state'][zoom>=5][zoom<=10] {
  text-name: '[name]';
  text-face-name: @medium;
  text-placement: point;
  text-fill: @state_text;
  text-halo-fill: @halo;
  text-halo-radius: 1;
  text-size: 10;
  text-wrap-width: 40;
  [zoom>=7] {
    text-size: 11;
    text-wrap-width: 50;
  }
  [zoom>=8] {
    text-halo-radius: 2;
    text-line-spacing: 1;
  }
  [zoom>=9] {
    text-size: 12;
    text-character-spacing: 1;
    text-wrap-width: 80;
    text-line-spacing: 2;
  }
  [zoom>=10] {
    text-size: 14;
    text-character-spacing: 2;
  }
}
#city[capital='yes'][zoom>=4][zoom<=10],
#city[zoom>=7][zoom<=10],
#place_low[capital='yes'][zoom>=4][zoom<=10],
#place_low[type='city'][zoom>=7][zoom<=10],
#place_low[type='town'][zoom>=9][zoom<=10] {
  shield-file: url('icon/place/town.svg');
  #city[capital='no'],
  [type='city'] {
    shield-file: url('icon/place/city.svg');
  }
  [capital='yes'] {
    shield-file: url('icon/place/capital.svg');
  }
  shield-name:'[name]';
  shield-size: 11;
  shield-face-name: @regular;
  shield-halo-radius: 1;
  shield-wrap-width: 50;
  shield-fill: @town_text;
  shield-halo-fill: @halo;
  shield-placement-type: simple;
  shield-placements: 'NE,SW,NW,SE,E,W';
  shield-text-dy: 2;
  shield-text-dx: 2;
  shield-unlock-image: true;
  shield-min-distance: 10;
  #city[capital='no'],
  [type='city'] {
    shield-face-name: @medium;
    shield-fill: @city_text;
    shield-halo-fill: @halo;
    shield-text-dy: 4;
    shield-text-dx: 4;
  }
  [capital='yes'] {
    shield-face-name: @bold;
    shield-fill: @city_text;
    shield-halo-fill: @halo;
    shield-size: 12;
    shield-line-spacing: -2;
    shield-text-dx: 4;
  }
  [zoom>=9] {
    shield-size: 12;
  }
}
#place[type='city'][zoom>=10],
#place[type='town'][zoom>=10],
#place[type='village'][zoom>=9],
#place[type='minor'][zoom>=14] {
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
  text-margin: 30;
  text-min-padding: 1;
  [type='town'] {
    text-fill: @town_text;
    text-face-name: @regular;
  }
  [type='city'] {
    text-fill: @city_text;
    text-face-name: @medium;
  }
  [type='minor'] {
    text-margin: 50;
  }
  [zoom>=12] {
    text-margin: 10;
    text-min-padding: 1;
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
    [type='minor'] {
      text-size: 10;
    }
  }
}

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

#housenumber[zoom>=17][zoom<19][mod5=true],
#housenumber[zoom>=19] {
  text-name: '[housenumber]';
  text-placement: interior;
  text-face-name: @regular;
  text-fill: @road_text;
  text-halo-fill: @halo;
  text-halo-radius: 1;
  text-size: 8;
  text-margin: 5;
  [zoom>=18] {
    text-size: 9;
  }
}
