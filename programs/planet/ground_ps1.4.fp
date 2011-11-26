#include "earth_params.h"
#include "../config.h"
#include "../stdlib.h"

uniform sampler2D specularMap_20;
uniform sampler2D baseMap_20;
uniform sampler2D cityLights_20;
uniform sampler2D cosAngleToDepth_20;
uniform sampler2D cloudMap_20;
uniform sampler2D noiseMap_20;
uniform sampler2D normalMap_20;

varying vec3 varTSLight;
varying vec3 varTSView;

float  cityLightTrigger(float fNDotLB) { return saturatef(4.0*fNDotLB); }

float fresnel(float fNDotV)
{
   return degamma(1.0-lerp(0.0,fNDotV,fFresnelEffect.x));
}

float expandPrecision(vec4 src)
{
   return dot(src,(vec4(1.0,256.0,65536.0,0.0)/131072.0));
}

float cosAngleToDepth(float fNDotV)
{
   vec2 res = vec2(1.0) / vec2(1024.0,128.0);
   vec2 mn = res * 0.5;
   vec2 mx = vec2(1.0)-res * 0.5;
   return expandPrecision(texture2D(cosAngleToDepth_20,clamp(vec2(fNDotV,fAtmosphereType),mn,mx),-8.0)) * fAtmosphereThickness;
}

float cosAngleToAlpha(float fNDotV)
{
   vec2 res = vec2(1.0) / vec2(1024.0,128.0);
   vec2 mn = res * 0.5;
   vec2 mx = vec2(1.0)-res * 0.5;
   return texture2D(cosAngleToDepth_20,clamp(vec2(fNDotV,fAtmosphereType),mn,mx)).a;
}

float  atmosphereLighting(float fNDotL) { return saturatef(2.0*fAtmosphereContrast*fNDotL); }
float  groundLighting(float fNDotL) { return saturatef(2.0*fGroundContrast*fNDotL); }

vec4 atmosphericScatter(vec4 dif, float fNDotV, float fNDotL, float fVDotL, vec3 fvShadow, vec3 fvAShadow)
{
   float  alpha = saturatef(2.0 * (cosAngleToAlpha(fNDotV) - 0.5));
   
   vec4 rv;
   
   vec3 absorption = lerp(sqr(fAtmosphereAbsorptionColor.rgb),vec3(1.0),saturatef(sqr(fNDotV*fNDotL*2.0)));
   float scattermuch = sqr(sqr(saturatef(1.0-fNDotV)));
   
   rv.rgb = regamma( dif.rgb*absorption*fvShadow 
                  +  atmosphereLighting(fNDotL)
                     *lerp(fMinScatterFactor, fMaxScatterFactor, scattermuch) 
                    *fAtmosphereScatterColor.rgb*fvAShadow );
   rv.a = dif.a * alpha;
   return rv;
}

void main()
{      
   vec2 texcoord = gl_TexCoord[0].xy;
   vec4 shadowcoord = gl_TexCoord[1];
   
   vec3 L = normalize(varTSLight);
   vec3 V = normalize(varTSView);
   vec3 N = expand( texture2D( normalMap_20, texcoord ).rgb ) * vec3(-1.0,1.0,1.0); // Do not normalize, to avoid aliasing
   vec3 R = -reflect(L,N);
   
   float  fNDotL           = saturatef( dot(N,L) ); 
   float  fNDotLs          = saturatef( L.z ); 
   float  fNDotLf          = L.z; 
   float  fNDotLB          = saturatef(-L.z + fCityLightTriggerBias.x);
   float  fRDotV           = saturatef( dot(R,V) );
   float  fNDotV           = saturatef( dot(N,V) );
   float  fNDotVs          = saturatef( V.z );
   float  fVDotL           = dot(L,V);
   
   vec4 fvTexColor         = texture2D( baseMap_20, texcoord );
   fvTexColor.rgb          = degamma_tex(fvTexColor.rgb);
   
   float  fGShadow         = texture2D( cloudMap_20, shadowcoord.xy ).a;
   fGShadow                = saturatef(fGShadow*fCloudLayerDensity);
   
   vec3 fvGShadow          = lerp( vec3(1.0), fvShadowColor.rgb, fGShadow );
   vec3 fvAShadow          = lerp( vec3(1.0), fvShadowColor.rgb, fGShadow*0.1 );
   
   vec4 fvSpecular         = degamma_tex(texture2D( specularMap_20, texcoord ));
   fvSpecular.rgb         *= fresnel(fNDotV);
   fRDotV                  = pow( fRDotV, fShininess.x*(0.01+0.99*fvSpecular.a)*256.0 );
   fvSpecular              = fvSpecular * gl_SecondaryColor * fRDotV;

   vec4 fvBaseColor;
   fvBaseColor.rgb         = gl_Color.rgb * groundLighting(fNDotL) * self_shadow(fNDotLs);
   fvBaseColor.a           = gl_Color.a;
   
   vec4 dif                = fvBaseColor * fvTexColor;
   vec4 spec               = 4.0*fvSpecular*self_shadow_smooth_ex(fNDotLs);

   gl_FragColor = atmosphericScatter( dif+spec, fNDotVs, fNDotLs, fVDotL, fvGShadow, fvAShadow );
}


