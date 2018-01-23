@xlight:    'Noto Sans ExtraLight',
            'Noto Sans Arabic ExtraLight',
            'Noto Sans Armenian ExtraLight',
            'Noto Sans CJK JP Light',
            'Noto Sans Georgian ExtraLight',
            'Noto Sans Hebrew ExtraLight',
            'Noto Sans Khmer ExtraLight',
            'Noto Sans Lao ExtraLight',
            'Noto Sans Myanmar ExtraLight',
            'Noto Sans Tamil ExtraLight',
            'Noto Sans Thai ExtraLight',
            'Unifont Medium';
@light:     'Noto Sans Light',
            'Noto Sans Arabic Light',
            'Noto Sans Armenian Light',
            'Noto Sans CJK JP Light',
            'Noto Sans Georgian Light',
            'Noto Sans Hebrew Light',
            'Noto Sans Khmer Light',
            'Noto Sans Lao Light',
            'Noto Sans Myanmar Light',
            'Noto Sans Tamil Light',
            'Noto Sans Thai Light',
            'Unifont Medium';
@lighti:    'Noto Sans Light Italic',
            'Noto Sans Arabic Light',
            'Noto Sans Armenian Light',
            'Noto Sans CJK JP Light',
            'Noto Sans Georgian Light',
            'Noto Sans Hebrew Light',
            'Noto Sans Khmer Light',
            'Noto Sans Lao Light',
            'Noto Sans Myanmar Light',
            'Noto Sans Tamil Light',
            'Noto Sans Thai Light',
            'Unifont Medium';
@regular:   'Noto Sans Regular',
            'Noto Sans Arabic Regular',
            'Noto Sans Armenian Regular',
            'Noto Sans CJK JP Regular',
            'Noto Sans Georgian Regular',
            'Noto Sans Hebrew Regular',
            'Noto Sans Khmer Regular',
            'Noto Sans Lao Regular',
            'Noto Sans Myanmar Regular',
            'Noto Sans Tamil Regular',
            'Noto Sans Thai Regular',
            'Unifont Medium';
@medium:    'Noto Sans Medium',
            'Noto Sans Arabic Medium',
            'Noto Sans Armenian Medium',
            'Noto Sans CJK JP Medium',
            'Noto Sans Georgian Medium',
            'Noto Sans Hebrew Medium',
            'Noto Sans Khmer Medium',
            'Noto Sans Lao Medium',
            'Noto Sans Myanmar Medium',
            'Noto Sans Tamil Medium',
            'Noto Sans Thai Medium',
            'Unifont Medium';
@bold:      'Noto Sans Bold',
            'Noto Sans Arabic Bold',
            'Noto Sans Armenian Bold',
            'Noto Sans CJK JP Bold',
            'Noto Sans Georgian Bold',
            'Noto Sans Hebrew Bold',
            'Noto Sans Khmer Bold',
            'Noto Sans Lao Bold',
            'Noto Sans Myanmar Bold',
            'Noto Sans Tamil Bold',
            'Noto Sans Thai Bold',
            'Unifont Medium';

Map {
  background-color: @water;
  buffer-size: @buffer;
  font-directory: url(./fonts);
}

#waterareas_gen[zoom>=4],
#waterareas[zoom>=13] {
  polygon-fill: @water;
}

#waterways_gen[zoom>=10][zoom<13],
#waterways[zoom>=13] {
  line-color: @water;
  line-cap: round;
  line-join: round;
  line-width: 1;
  [zoom>=14] {
    line-width: 3;
  }
}
