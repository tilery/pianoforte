/* ******* */
/* Palette */
/* ******* */
@land:              #ffffff;
@residential:       #f8f7f7;
@water:             #c5d2dd;
@admin:             #bea6a6;
@industrial:        #f7f4f5;
@neutral:           #e2e2e6;
@wetland:           #e3e9e2;
@grass:             #f0f2f0;
@wooded:            #f2f4f2;
@beach:             #eee5b2;
@agriculture:       #f4f1eb;

@road_fill:         #ffffff;
@road_case:         #9d9d9d;

@rail_fill:         #ddd;
@rail_case:         #aaa;

@city_text:         #222;
@city_halo:         @land;
@town_text:         #444;
@town_halo:         @land;
@village_text:      #444;
@village_halo:      @land;

@road_text:         #222;
@road_halo:         @land;

@regular:           'Fira Sans Regular';
@bold:              'Fira Sans Bold';
@medium:            'Fira Sans Medium';
@book:              'Fira Sans Book';
@xlight:            'Fira Sans ExtraLight';

@buffer:            512;

/* *********** */
/* backgrounds */
/* *********** */

Map {
  background-color: @water;
  buffer-size: @buffer;
}
#land {
  polygon-fill: @land;
}
#landuse_gen[zoom<14],
#landuse[type="residential"][zoom>=12],
#landuse[zoom>=14] {
  #landuse_gen {
      polygon-opacity: 0.8;
  }
  #landuse_gen[zoom>=12] {
      polygon-opacity: 0.9;
  }
  [type='grave_yard'],
  [type='college'],
  [type='school'],
  [type='education'],
  [type='sports_centre'],
  [type='stadium'],
  [type='university'],
  [type='cemetery'] {
      polygon-fill: @neutral;
  }
  [type='hospital'],
  [type='industrial'],
  [type='landfill'],
  [type='quarry'],
  [type='commercial'] {
      polygon-fill: @industrial;
  }
  [type='residential'],
  [type='retail'],
  [type='pedestrian'] {
      polygon-fill: @residential;
      [type='residential'][zoom>=14] {
          polygon-fill: @land;
      }
  }
  [type='golf_course'],
  [type='pitch'],
  [type='grass'],
  [type='grassland'],
  [type='park'],
  [type='garden'],
  [type='village_green'],
  [type='recreation_ground'],
  [type='picnic_site'],
  [type='camp_site'],
  [type='playground'],
  [type='common'],
  [type='scrub'],
  [type='meadow'],
  [type='heath'] {
      polygon-fill: @grass;
  }
  [type='forest'],
  [type='wood'] {
      polygon-fill: @wooded;
  }
  [type='farmland'],
  [type='farm'],
  [type='orchard'],
  [type='allotments'] {
      polygon-fill: @land;
  }
  [type='beach'],
  [type='desert'] {
      polygon-fill: @beach;
  }
  [type='basin'] {
      polygon-fill: @water;
  }
  [type='wetland'] {
      polygon-fill: @wetland;
  }
}

#waterway {
  polygon-fill: @water;
}

/* ************************* */
/* ADMINISTRATIVE BOUNDARIES */
/* ************************* */
#boundary[admin_level=4],
#boundary[admin_level=6],
#boundary[admin_level=8][zoom>=12],
#boundary[admin_level=9][zoom>=12] {
  eraser/line-color: @land;
  eraser/line-width: 1;
  eraser/comp-op: darken;
  line-color: @admin;
  line-width: 0.8;
  line-dasharray: 8,4;
  [zoom<12] {
    line-smooth: 0.2;
    line-simplify: 10;
    line-color: lighten(@admin, 15%);
  }
  [admin_level=4] {
      line-cap: butt;
      line-width: 1.5;
  }
  [admin_level=6] {
      line-cap: butt;
      line-width: 1;
      line-color: lighten(@admin, 15%);
  }
  [admin_level=8],
  [admin_level=9] {
    line-dasharray: 1,3;
    line-cap: round;
    [zoom>=13] {
        line-width: 1;
    }
  }
}
/* ******** */
/* RAILWAYS */
/* ******** */
#railway[zoom>=14] {
  outline/line-width: 1;
  outline/line-color: @rail_case;
  outline/line-cap: round;
  line-color: @rail_fill;
  line-width: 1;
  line-dasharray: 5,5;
  [zoom>=15] {
    outline/line-width: 2;
  line-width: 2;
  }
  [zoom>=17] {
    outline/line-width: 3;
  }
}


/* ******** */
/*  ROADS   */
/* ******** */
#roads_gen::casing[type='primary'][zoom>=12][zoom<13],
#roads_gen::casing[type='trunk'][zoom>=12][zoom<13],
#roads_gen::casing[type='motorway'][zoom>=12][zoom<13],
#roads_gen::casing[type='primary_link'][zoom>=12][zoom<13],
#roads_gen::casing[type='trunk_link'][zoom>=12][zoom<13],
#roads_gen::casing[type='motorway_link'][zoom>=12][zoom<13],
#roads::casing[type='residential'][zoom>=15],
#roads::casing[type='unclassified'][zoom>=15],
#roads::casing[type='service'][zoom>=15],
#roads::casing[type='secondary'][zoom>=15],
#roads::casing[type='tertiary'][zoom>=15],
#roads::casing[type='primary'][zoom>=13],
#roads::casing[type='primary_link'][zoom>=13],
#roads::casing[type='trunk'][zoom>=13],
#roads::casing[type='trunk_link'][zoom>=13],
#roads::casing[type='motorway_link'][zoom>=13],
#roads::casing[type='motorway'][zoom>=13] {
  line-color: @road_case;
  line-width: 2;
  line-join: round;
  [zoom>=13] {
    line-width: 3;
    [type='motorway'] {
        line-width: 5;
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
#roads_gen[type='primary'][zoom>=12][zoom<13],
#roads_gen[type='trunk'][zoom>=12][zoom<13],
#roads_gen[type='motorway'][zoom>=12][zoom<13],
#roads_gen[type='primary_link'][zoom>=12][zoom<13],
#roads_gen[type='trunk_link'][zoom>=12][zoom<13],
#roads_gen[type='motorway_link'][zoom>=12][zoom<13],
#roads[type='residential'][zoom>=15],
#roads[type='unclassified'][zoom>=15],
#roads[type='service'][zoom>=15],
#roads[type='secondary'][zoom>=15],
#roads[type='tertiary'][zoom>=15],
#roads[type='primary'][zoom>=13],
#roads[type='primary_link'][zoom>=13],
#roads[type='trunk'][zoom>=13],
#roads[type='trunk_link'][zoom>=13],
#roads[type='motorway_link'][zoom>=13],
#roads[type='motorway'][zoom>=13] {
  line-color: @road_fill;
  line-join: round;
  line-cap: square;
  line-width: 1;
  [zoom<=10] {
      line-width: 0;
  }
  [zoom>=13] {
    line-width: 2;
    [type='motorway'] {
        line-width: 4;
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
#roads_gen[type='primary'][zoom>=10][zoom<12],
#roads_gen[type='trunk'][zoom>=9][zoom<12],
#roads_gen[type='motorway'][zoom>=7][zoom<12],
#roads_gen[type='secondary'][zoom=12],
#roads[type='residential'][zoom=14],
#roads[type='unclassified'][zoom=14],
#roads[type='service'][zoom=14],
#roads[type='living_street'][zoom=14],
#roads[type='tertiary'][zoom>=12][zoom<15],
#roads[type='secondary'][zoom>=12][zoom<15] {
  line-color: @road_case;
  line-width: 1;
  [type='service'],
  [type='residential'],
  [type='unclassified'] {
    line-width: 0.5;
  }
  [type='motorway'][zoom>=10],
  [type='trunk'][zoom>=10] {
      line-width: 2;
  }
  [type='tertiary'][zoom<=12],
  [type='secondary'][zoom<=12],
  [zoom<=10] {
      line-color: lighten(@road_case, 20%);
  }
  [zoom<=8] {
      line-color: lighten(@road_case, 30%);
  }
  [zoom>=16] {line-width: 2;}
}


/* ****** */
/* BUILDINGS */
/* ****** */
#buildings[zoom>=14] {
  polygon-fill: #ebebeb;
  [zoom>=15] {
      line-color: #ddd;
      [type!="yes"] {
        polygon-fill: #ddd;
        line-color: #ccc;
      }
  }
}
