/* ******* */
/* Palette */
/* ******* */
@land:              #eee;
@residential:       #dfdfdf;
@water:             #95adc1;
@industrial:        #e2dbde;
@emphasis:          #d6d6d2;
@wetland:           #e5e9e2;
@wooded:            #9cc29c;
@grass:             #c1d8c1;
@sand:              #ede5bb;
@agriculture:       #e5e8e2;

@halo:              @land;

@admin_2:           #5c7175;
@admin_3:           #aaa3a3;
@admin_2_text:      @admin_2;
@admin_3_text:      @admin_3;

@building:          #d2d2d2;
@building_case:     #c2c2c2;

@road_fill:         #ffffff;
@highway_fill:      #ffcc88;
@primary_fill:      #ffcc88;
@road_case:         #999;

@rail_fill:         #ccc;
@rail_case:         #777;

@country_text:      @admin_2;
@state_text:        #666;
@city_text:         #333;
@town_text:         #333;
@village_text:      #333;
@landuse_text:      #444;

@road_text:         #222;
@poi_text:          #222;

@buffer:            512;

/* *********** */
/* backgrounds */
/* *********** */

#land-low[zoom<10],
#land[zoom>=10] {
  polygon-fill: @land;
}
#landuse_gen[zoom>=4][zoom<13],
#landuse[type="residential"][zoom>=11],
#landuse[zoom>=13] {
  #landuse_gen {
      polygon-opacity: 0.7;
  }
  #landuse_gen[zoom>=12] {
      polygon-opacity: 0.8;
  }
  polygon-fill: @land;  // Default.
  [type='grave_yard'],
  [type='college'],
  [type='school'],
  [type='education'],
  [type='stadium'],
  [type='university'],
  [type='sports_centre'],
  [type='hospital'],
  [type='parking'],
  [type='cemetery'] {
      polygon-fill: @emphasis;
  }
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
  [type='track'],
  [type='pitch'],
  [type='grass'],
  [type='park'],
  [type='garden'],
  [type='village_green'],
  [type='recreation_ground'],
  [type='picnic_site'],
  [type='camp_site'],
  [type='playground'] {
    polygon-fill: @grass;
    line-color: darken(@grass, 5);
  }
  [type='golf_course'],
  [type='common'],
  [type='scrub'],
  [type='meadow'],
  [type='heath'],
  [type='grassland'],
  [type='allotments'] {
    polygon-fill: @grass;
  }
  [type='forest'],
  [type='wood'] {
    polygon-fill: @wooded;
  }
  [type='farmland'],
  [type='farm'],
  [type='orchard'] {
    polygon-fill: @agriculture;
    [zoom<=11] {
      polygon-opacity: 0.5;
    }
  }
  [type='beach'] {
    polygon-fill: @sand;
  }
  [type='sand'],
  [type='desert'] {
    polygon-fill: @sand;
    polygon-opacity: 0.4;
    [zoom>=14] {
      polygon-opacity: 0.5;
    }
    [zoom>=16] {
      polygon-opacity: 0.7;
    }
  }
  [type='basin'] {
      polygon-fill: @water;
  }
  [type='wetland'] {
      polygon-fill: @wetland;
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
  [service='yard'] {
    outline/line-color: lighten(@rail_fill, 5);
  }
  line-color: @rail_fill;
  line-width: 0.5;
  line-dasharray: 5,5;
  [zoom>=14] {
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
      line-color: @building_case;
      [type!="yes"] {
        polygon-fill: darken(@building, 5);
        line-color: darken(@building_case, 10);
      }
  }
}
