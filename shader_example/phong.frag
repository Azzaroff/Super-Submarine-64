
/* A basic phong shader*/


uniform int NumLights;

varying vec3 Position;
varying vec3 Normal;

void main( void )
{

	vec3  fvNormal         = normalize( Normal );
	vec3  fvViewDirection  = normalize( -Position );


	vec4  fvTotalAmbient = vec4(0.0);
	vec4  fvTotalDiffuse = vec4(0.0);
	vec4  fvTotalSpecular = vec4(0.0);

	for(int lightNum = 0; lightNum  < NumLights; ++lightNum)
	{
		vec3  fvLightDirection = normalize( gl_LightSource[lightNum].position.xyz - Position );
		float fNDotL           = dot( fvNormal, fvLightDirection );

		if(fNDotL > 0.0)
		{

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
