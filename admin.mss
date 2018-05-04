#disputed{
  line-width: 1;
  line-color: @admin_3;
  line-clip: true;
  line-dasharray: 4, 4;
  [zoom<12] {
    polygon-pattern-file: url('icon/pattern/disputed.svg');
    polygon-pattern-alignment: local;
  }
  [zoom<4] {
    polygon-pattern-file: url('icon/pattern/disputed_small.svg');
  }
  [zoom=9] {
    polygon-pattern-opacity: 0.8;
    line-opacity: 0.8;
  }
  [zoom>=10][zoom<12] {
    polygon-pattern-opacity: 0.4;
    line-opacity: 0.4;
  }
}
#itl_boundary_low[zoom>=1][zoom<6][maritime!='yes'],
#itl_boundary[zoom>=6] {
  line-width: 0.5;
  line-color: @admin_2;
  line-clip: true;
  [maritime='yes'] {
    line-dasharray: 10,5;
  }
  [zoom>=4] {
    line-width: 1;
  }
  [zoom>=9] {
    line-width: 2;
  }
}
#boundary[admin_level=3][zoom>=4][zoom<5],
#boundary[admin_level=4][zoom>=4][zoom<5],
#boundary[admin_level<=4][zoom>=5][zoom<12],
#boundary[admin_level<=8][zoom>=12] {
  eraser/line-color: @land;
  eraser/line-width: 1;
  eraser/comp-op: darken;
  eraser/line-clip: true;
  line-clip: true;
  line-width: 0.8;
  line-color: @admin_3;
  [zoom<6] {
    line-color: lighten(@admin_3, 5);
  }
  [zoom>=7] {
    line-dasharray: 10,5,5,5;
    line-width: 1;
    [admin_level>=6] {
      line-dasharray: 5,5,2,5;
    }
  }
  [zoom>=9] {
    line-color: darken(@admin_3, 20);
  }
}

#itl_boundary_label[zoom>=10],
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
