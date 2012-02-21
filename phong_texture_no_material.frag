/* A basic phong shader*/
 
 
uniform sampler2D color_map;
uniform int NumLights;
 
varying vec3 Position;
varying vec3 Normal;
varying vec2 texcoord;


void main( void )
{
 
        vec3  fvNormal         = normalize( Normal );
 
        vec4  fvTotalDiffuse = vec4(0.0);
 
        vec4 texture         = texture2D( color_map, texcoord );
 
        for(int lightNum = 0; lightNum  < NumLights; ++lightNum)
        {
                vec3  fvLightDirection = normalize( gl_LightSource[lightNum].position.xyz - Position );
                float fNDotL           = dot( fvNormal, fvLightDirection );
 
                if(fNDotL > 0.0)
                        fvTotalDiffuse         += texture * gl_LightSource[lightNum].diffuse * fNDotL;
 
        }
 
        vec4 v4_final_color = ( fvTotalDiffuse );
 
        if(gl_FrontMaterial.diffuse.a >= 0.99)
                v4_final_color.a = 1.0;
        else
                v4_final_color.a = gl_FrontMaterial.diffuse.a;
               
        gl_FragColor = v4_final_color;
 
}