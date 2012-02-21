uniform sampler2D color_map;

varying vec2 texcoord;

void main( void )
{
   vec4 texcol  = texture2D( color_map, texcoord );
   gl_FragColor = texcol;
   
}
