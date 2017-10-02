#boundary[admin_level=2][zoom>=2][zoom<5],
#boundary[admin_level=3][zoom>=4][zoom<5],
#boundary[admin_level=4][zoom>=4][zoom<5],
#boundary[admin_level<=4][zoom>=5][zoom<11],
#boundary[admin_level<=8][zoom>=11][zoom<13],
#boundary[admin_level<=10][zoom>=13] {
  [admin_level=2] {
    outline/line-color: lighten(@admin_2, 25%);
    outline/line-width: 2;
    [zoom>=8] {
      outline/line-width: 3;
    }
  }
  eraser/line-color: white;
  eraser/line-width: 1;
  eraser/comp-op: darken;
  line-color: @admin_2;
  line-width: 1;
  [admin_level>2] {
    line-dasharray: 10,5;
    line-color: @admin_3;
    [admin_level>=6] {
      line-dasharray: 5,5;
      line-width: 0.8;
    }
  }
}

#boundary_label[admin_level<=4][zoom>=10],
#boundary_label[zoom>=13] {
  text-name: "'      '+[name]+'      '";
  text-fill: @admin_2_text;
  text-size: 11;
  text-placement: line;
  text-dy: -7;
  text-face-name: @lighti;
  text-halo-radius: 2;
  text-halo-fill: @admin_halo;
  text-min-padding: 50;
  text-min-distance: 50;
  text-spacing: 300;
  text-max-char-angle-delta: 10;
}
