
/* A basic phong shader*/


uniform sampler2D color_map;
uniform int NumLights;

varying vec3 Position;
varying vec3 Normal;
varying vec2 texcoord;
varying vec3 objectNormal;

void main( void )
{

	vec3  fvNormal         = normalize( Normal );
	vec3  fvViewDirection  = normalize( -Position );


	vec4  fvTotalAmbient = vec4(0.0);
	vec4  fvTotalDiffuse = vec4(0.0);
	vec4  fvTotalSpecular = vec4(0.0);

	vec4 texture         = texture2D( color_map, texcoord );
	float texture_lightness = texture.r*0.3 + texture.g*0.59 + texture.b*0.11;

	for(int lightNum = 0; lightNum  < NumLights; ++lightNum)
	{
		vec3  fvLightDirection = normalize( gl_LightSource[lightNum].position.xyz - Position );
		float fNDotL           = dot( fvNormal, fvLightDirection );

		if(fNDotL > 0.0)
		{

			if(texture_lightness > 0.0 && objectNormal.y < 0.5)
				fvTotalDiffuse         += texture * gl_LightSource[lightNum].diffuse * fNDotL;

			else
				fvTotalDiffuse         += gl_FrontMaterial.diffuse * gl_LightSource[lightNum].diffuse * fNDotL;

			vec3  fvReflection     = normalize( ( ( 2.0 * fvNormal ) * fNDotL ) - fvLightDirection );

			float fRDotV           = max( 0.0, dot( fvReflection, fvViewDirection ) );

			fvTotalSpecular        += gl_FrontMaterial.specular
                                    * gl_LightSource[int(lightNum)].specular
                                    * pow(fRDotV, gl_FrontMaterial.shininess);

		}

	}

	vec4 v4_final_color = ( fvTotalAmbient + fvTotalDiffuse + fvTotalSpecular );

	if(gl_FrontMaterial.diffuse.a >= 0.99)
		v4_final_color.a = 1.0;
	else
		v4_final_color.a = gl_FrontMaterial.diffuse.a;
		
	gl_FragColor = v4_final_color;

}
