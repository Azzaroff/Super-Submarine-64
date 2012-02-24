void main()
{
  //gl_FragColor = vec4(0.0, 1.0, 1.0, 1.0);
  gl_FragColor.r = gl_Color.r * 0.9;
  gl_FragColor.g = gl_Color.g * 0.7;
  gl_FragColor.b = gl_Color.b;
  

}
