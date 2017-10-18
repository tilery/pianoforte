/*  LOW ZOOMS  */

#roads_gen::low[type='primary'][zoom>=10][zoom<12],
#roads_gen::low[type='trunk'][zoom>=9][zoom<12],
#roads_gen::low[type='motorway'][zoom>=7][zoom<12],
#roads_gen::low[type='secondary'][zoom>=11][zoom<12] {
  casing/line-width: 3;
  casing/line-color: @road_case;
  casing/line-join: round;
  casing/line-cap: butt;
  line-join: round;
  line-cap: butt;
  line-width: 2;
  line-color: @road_fill;
  [type='secondary'] {
    casing/line-width: 1.5;
    line-width: 1;
  }
  [type='motorway'][zoom>=10],
  [type='trunk'][zoom>=10] {
    // casing/line-width: 2.5;
    // line-width: 2;
    line-color: @highway_fill;
  }
  // [zoom<=10] {
  //   line-color: lighten(@road_case, 20);
  // }
  // [zoom<=8] {
  //   line-color: lighten(@road_case, 30);
  // }
}

#roads::simple[type='residential'][zoom>=13][zoom<15],
#roads::simple[type='unclassified'][zoom=14],
#roads::simple[type='service'][zoom=14],
#roads::simple[type='living_street'][zoom=14],
#roads::simple[type='tertiary'][zoom>=12][zoom<15],
#roads::simple[type='secondary'][zoom>=12][zoom<15] {
  line-color: @road_fill;
  line-width: 1.2;
  [type='service'],
  [type='residential'][zoom<14],
  [type='unclassified'] {
    line-width: 0.5;
  }
  [zoom>=16] {line-width: 2;}
}


#roads::casing[type='residential'][zoom>=15],
#roads::casing[type='unclassified'][zoom>=15],
#roads::casing[type='service'][zoom>=15],
#roads::casing[type='secondary'][zoom>=15],
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
    [type='service'],
    [type='residential'],
    [type='unclassified'] {
        line-width: 3;
    }
    [type='motorway'] {
        line-width: 8;
    }
  }
  [zoom>=17] {
    line-width: 9;
    [type='service'],
    [type='residential'],
    [type='unclassified'] {
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
#roads[type='residential'][zoom>=15],
#roads[type='unclassified'][zoom>=15],
#roads[type='service'][zoom>=15],
#roads[type='secondary'][zoom>=15],
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
  // [type='primary'] {
  //   line-color: @primary_fill;
  // }
  [zoom>=13] {
    line-width: 3;
    [type='motorway'] {
        line-width: 5;
    }
  }
  [zoom>=15] {
    line-width: 4;
    [type='service'],
    [type='residential'],
    [type='unclassified'] {
        line-width: 2;
    }
    [type='motorway'] {
      line-width: 7;
    }
  }
  [zoom>=17] {
    line-width: 8;
    [type='service'],
    [type='residential'],
    [type='unclassified'] {
        line-width: 5;
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
  shield-file: url('shield/road-[reflen].svg');
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

#road_label[type='living_street'][zoom>=14],
#road_label[type='residential'][zoom>=14],
#road_label[type='unclassified'][zoom>=14],
#road_label[type='service'][zoom>=14],
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
  text-halo-fill: @road_halo;
  text-halo-radius: 2;
  text-min-distance: 60;
  text-size: 12;
  text-avoid-edges: true;
  text-character-spacing: 0;
  [zoom=16] {
      text-size: 13;
  }
  [zoom>=17] {
      text-size: 14;
  }
}
