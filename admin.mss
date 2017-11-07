#boundary[admin_level=2][zoom>=2][zoom<5],
#boundary[admin_level=3][zoom>=4][zoom<5],
#boundary[admin_level=4][zoom>=4][zoom<5],
#boundary[admin_level<=4][zoom>=5][zoom<11],
#boundary[admin_level<=8][zoom>=11][zoom<13],
#boundary[admin_level<=10][zoom>=13] {
  [admin_level=2] {
    outline/line-color: lighten(@admin_2, 25%);
    outline/line-width: 2;
    outline/line-clip: true;
    [zoom>=8] {
      outline/line-width: 3;
    }
  }
  eraser/line-color: white;
  eraser/line-width: 1;
  eraser/comp-op: darken;
  eraser/line-clip: true;
  line-color: @admin_2;
  line-clip: true;
  line-width: 1;
  [admin_level>2] {
    line-dasharray: 10,5;
    line-color: @admin_3;
    [zoom>=14] {
      line-color: darken(@admin_3, 10);
    }
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
  text-halo-radius: 1.5;
  text-halo-fill: @halo;
  text-min-padding: 50;
  text-repeat-distance: 50;
  text-spacing: 300;
  text-max-char-angle-delta: 10;
  text-clip: true;
}
