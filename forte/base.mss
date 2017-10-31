/* ******* */
/* Palette */
/* ******* */
@land:              #eee;
@residential:       #dfdfdf;
@water:             #a9bfcc;
@industrial:        #e2dbde;
@neutral:           #e2e2e6;
@wetland:           #e3e9e2;
@wooded:            #9cc29c;
@grass:             #c1d8c1;
@sand:              #eee5b2;
@agriculture:       #92ab78;

@halo:              @land;

@admin:             #bea6a6;
@admin_2:           #537076;
@admin_3:           #a59c9b;
@admin_2_text:      @admin_2;
@admin_3_text:      @admin_3;

@building:          #cfcfcf;

@road_fill:         #ffffff;
@highway_fill:      #ffcc88;
@primary_fill:      #ffcc88;
@road_case:         #999;

@rail_fill:         #ccc;
@rail_case:         #999;

@city_text:         #222;
@town_text:         #222;
@village_text:      #222;
@landuse_text:      #333;

@road_text:         #222;

@buffer:            512;

/* *********** */
/* backgrounds */
/* *********** */

Map {
  background-color: @water;
  buffer-size: @buffer;
}
#land-low[zoom<10],
#land[zoom>=10] {
  polygon-fill: @land;
}
#landuse_gen[zoom<13],
#landuse[type="residential"][zoom>=11],
#landuse[zoom>=13] {
  #landuse_gen {
      polygon-opacity: 0.8;
  }
  #landuse_gen[zoom>=12] {
      polygon-opacity: 0.9;
  }
  polygon-fill: @neutral;  // Default.
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
      polygon-fill: @sand;
  }
  [type='basin'] {
      polygon-fill: @water;
  }
  [type='wetland'] {
      polygon-fill: @wetland;
  }
}

#waterareas {
  polygon-fill: @water;
}

#waterways {
  line-color: @water;
  line-cap: round;
  line-join: round;
  line-width: 1;
  [zoom>=14] {
    line-width: 3;
  }
}

/* ******** */
/* RAILWAYS */
/* ******** */
#railway[service!='yard'][zoom>=12],
#railway[zoom>=14] {
  outline/line-width: 0.5;
  outline/line-color: @rail_case;
  outline/line-cap: round;
  line-color: @rail_fill;
  line-width: 0.5;
  line-dasharray: 5,5;
  [zoom>=15] {
    outline/line-width: 1;
    line-width: 1;
  }
  [zoom>=15] {
    outline/line-width: 2;
    line-width: 2;
  }
  [zoom>=17] {
    outline/line-width: 3;
    line-width: 3;
  }
}


/* ****** */
/* BUILDINGS */
/* ****** */
#buildings[zoom>=14] {
  polygon-fill: @building;
  [zoom>=15] {
      line-color: #ddd;
      [type!="yes"] {
        polygon-fill: #ddd;
        line-color: #ccc;
      }
  }
}
