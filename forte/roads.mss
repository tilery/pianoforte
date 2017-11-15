/*  LOW ZOOMS  */

#roads_gen::low[type='primary'][zoom>=10][zoom<12],
#roads_gen::low[type='trunk'][zoom>=8][zoom<12],
#roads_gen::low[type='motorway'][zoom>=7][zoom<12],
#roads_gen::low[type='secondary'][zoom>=11][zoom<12] {
  casing/line-width: 2;
  casing/line-color: @road_case;
  casing/line-join: round;
  casing/line-cap: butt;
  line-join: round;
  line-cap: butt;
  line-width: 1;
  line-color: @road_fill;
  [zoom<=8] {
    casing/line-width: 0.6;
    line-width: 0.6;
    line-color: @road_case;
  }
  [zoom>=11][type!='secondary'] {
    casing/line-width: 3;
    line-width: 2;
  }
  [type='motorway'][zoom>=9],
  [type='trunk'][zoom>=9] {
    line-color: @highway_fill;
  }
}

#roads::simple[type='minor'][zoom>=13][zoom<15],
#roads::simple[type='tertiary'][zoom>=12][zoom<15],
#roads::simple[type='secondary'][zoom>=12][zoom<14] {
  line-color: @road_fill;
  line-width: 1.2;
  [type='minor'] {
    line-width: 0.5;
  }
}


#roads::casing[type='minor'][zoom>=15],
#roads::casing[type='secondary'][zoom>=14],
#roads::casing[type='tertiary'][zoom>=15],
#roads::casing[type='primary'][zoom>=12],
#roads::casing[type='primary_link'][zoom>=12],
#roads::casing[type='trunk'][zoom>=12],
#roads::casing[type='trunk_link'][zoom>=12],
#roads::casing[type='motorway_link'][zoom>=12],
#roads::casing[type='motorway'][zoom>=12] {
  line-color: @road_case;
  line-width: 3;
  line-join: round;
  [zoom>=14][tunnel=1] {
    line-dasharray: 5,5;
    line-color: darken(@road_case, 10);
  }
  [zoom>=14][bridge=1] {
    line-color: darken(@road_case, 30);
  }
  [zoom>=13] {
    line-width: 4;
    [type='motorway'] {
        line-width: 6;
    }
  }
  [zoom>=15] {
    line-width: 5;
    [type='minor'] {
        line-width: 3;
    }
    [type='motorway'] {
        line-width: 8;
    }
  }
  [zoom>=17] {
    line-width: 9;
    [type='minor'] {
        line-width: 6;
    }
    [type='motorway'] {
        line-width: 11;
    }
  }
  [zoom<=10] {
    line-width: 0.5;
  }
}
#roads[type='path'][zoom>=15],
#roads[type='minor'][zoom>=15],
#roads[type='secondary'][zoom>=14],
#roads[type='tertiary'][zoom>=15],
#roads[type='primary'][zoom>=12],
#roads[type='primary_link'][zoom>=12],
#roads[type='trunk'][zoom>=12],
#roads[type='trunk_link'][zoom>=12],
#roads[type='motorway_link'][zoom>=12],
#roads[type='motorway'][zoom>=12] {
  line-color: @road_fill;
  line-join: round;
  line-cap: square;
  line-width: 2;
  [type='trunk'],
  [type='trunk_link'][zoom>=14],
  [type='motorway_link'][zoom>=14],
  [type='motorway'] {
    line-color: @highway_fill;
    [zoom>=14][tunnel=1] {
      line-color: lighten(@highway_fill, 10);
    }
  }
  [zoom>=13] {
    line-width: 3;
    [type='motorway'] {
      line-width: 5;
    }
  }
  [zoom>=15] {
    line-width: 4;
    [type='minor'] {
      line-width: 2;
    }
    [type='path'] {
      line-dasharray: 10,5;
      line-width: 0.5;
    }
    [type='motorway'] {
      line-width: 7;
    }
  }
  [zoom>=16] {
    [type='path'] {
      line-width: 0.7;
    }
  }
  [zoom>=17] {
    line-width: 8;
    [type='minor'] {
      line-width: 5;
    }
    [type='path'] {
      line-width: 1.2;
    }
    [type='motorway'] {
      line-width: 10;
    }
  }
}

#road_label::shield[type='secondary'][zoom>=15][reflen>=1][reflen<=6],
#road_label::shield[type='primary'][zoom>=13][reflen>=1][reflen<=6],
#road_label::shield[type='trunk'][zoom>=12][reflen>=1][reflen<=6],
#road_label::shield[type='motorway'][zoom>=9][reflen>=1][reflen<=6] {
  shield-name: "[ref].replace('·', '\n')";
  shield-size: 9;
  shield-line-spacing: -4;
  shield-file: url('icon/shield/road-[reflen].svg');
  shield-face-name: @light;
  shield-fill: #333;
  shield-spacing: 100;
  shield-margin: 10;
  shield-min-padding: 1;
  shield-repeat-distance: 100;
  [zoom>=14] {
    shield-repeat-distance: 100;
    shield-transform: scale(1.25,1.25);
    shield-size: 11;
  }
}

#road_label[type='path'][zoom>=16],
#road_label[type='minor'][zoom>=15],
#road_label[type='secondary'][zoom>=14],
#road_label[type='tertiary'][zoom>=14],
#road_label[type='primary'][zoom>=14],
#road_label[type='trunk'][zoom>=14],
#road_label[type='motorway'][zoom>=13] {
  text-name: '[name]';
  [lang='fr'] {
    text-name: '[name].replace("^Chemin", "Ch.").replace("^Avenue", "Av.").replace("^Rue", "R.").replace("^Route", "Rte").replace("^Boulevard", "Bd")';
  }
  text-face-name: @xlight;
  text-placement: line;
  text-fill: @road_text;
  text-halo-fill: @halo;
  text-halo-radius: 1.5;
  text-repeat-distance: 60;
  text-size: 11;
  text-avoid-edges: true;
  text-character-spacing: 0;
  [zoom>=15] {
    text-margin: 10;
    text-dy: 4;
    text-character-spacing: 0.5;
    text-face-name: @light;
  }
  [zoom>=16] {
    text-size: 13;
  }
  [zoom>=17] {
    text-size: 14;
  }
}
