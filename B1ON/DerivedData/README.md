So I found this git useful

https://github.com/mypalmike/csplitb

When I pip installed it I couldnt get it working from dos

So I did the following:

I created my own runner

```
import sys
from csplitb import CSplitB
csplitb = CSplitB("0000000053495A45", "../Zoom B1on System v1.30 Updater.exe", 3, "FX", ".ZDL")
csplitb.run()
```
and hence in my directory I got
```
04/08/2021  20:59            12,288 FX000.ZDL
04/08/2021  20:59            16,384 FX001.ZDL
04/08/2021  20:59            24,576 FX002.ZDL
04/08/2021  20:59            20,480 FX003.ZDL
04/08/2021  20:59            28,672 FX004.ZDL
04/08/2021  20:59            20,480 FX005.ZDL
04/08/2021  20:59            16,384 FX006.ZDL
04/08/2021  20:59            16,384 FX007.ZDL
04/08/2021  20:59            20,480 FX008.ZDL
04/08/2021  20:59            16,384 FX009.ZDL
...
04/08/2021  20:59            12,288 FX135.ZDL
04/08/2021  20:59            16,384 FX136.ZDL
04/08/2021  20:59           199,730 FX137.ZDL
```
So now to determine, from the OnOff patterns, which FX these are

This might do the trick?

```
$ for file in *.ZDL
> do
> echo $file
> strings $file | grep -A1 "__TI_internal"
> done
FX000.ZDL
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_DYN_ZNR\Debug
FX001.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_SFX_Z_Syn\Debug
FX002.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_acoustic\Debug
FX003.ZDL
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_AC_Bs_Pre\Debug
FX004.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_Ag_Amp\Debug
FX005.ZDL
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_BassDrive\Debug
FX006.ZDL
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSDRV_Bass_Muff\Debug
FX007.ZDL
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_Bass_BB\Debug
FX008.ZDL
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_Bass_Pre\Debug
FX009.ZDL
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSDRV_Ba_Boost\Debug
FX010.ZDL
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSDRV_Ba_Dist_1\Debug
FX011.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_B_MAN\Debug
FX012.ZDL
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSDRV_Ba_Metal\Debug
FX013.ZDL
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSDRV_Bass_OD\Debug
FX014.ZDL
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_DI5\Debug
FX015.ZDL
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_DI_Plus\Debug
FX016.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_FlipTop\Debug
FX017.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSAMP_GKrueger\Debug
FX018.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_Heaven\Debug
FX019.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_HRT3500\Debug
FX020.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_Mark_B\Debug
FX021.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_Monotone\Debug
FX022.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSAMP_SMR\Debug
FX023.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_SuperB\Debug
FX024.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_SVT\Debug
FX025.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_SFX_4VoiceSyn\Debug
FX026.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_REV_Air\Debug
FX027.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_REV_Arena\Debug
FX028.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_SFX_AutoPan\Debug
FX029.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_BendCho\Debug
FX030.ZDL
FX031.ZDL
__TI_internal
C:\Project\ZDL\D262\ZDL_MOD_HPS\Debug
FX032.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_MojoRolle\Debug
FX033.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_MultiTapD\Debug
FX034.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_PitchDly\Debug
FX035.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_MOD_RingMod\Debug
FX036.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_FLT_RndmFLTR\Debug
FX037.ZDL
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_MOD_StereoCho\Debug
FX038.ZDL
__TI_internal
C:\project\ZDL\D237\ZDL_FLT_Step\Debug
FX039.ZDL
__TI_internal
C:\Project\ZDL\D262\ZDL_DLY_TapeEcho\Debug
FX040.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_TrgHldDly\Debug
FX041.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_REV_TiledRoom\Debug
FX042.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_VinFLNGR\Debug
FX043.ZDL
FX044.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_WarpPhase\Debug
FX045.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_SFX_Z_Organ\Debug
FX046.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Z_Tron\Debug
FX047.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_T_Scream\Debug
FX048.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_B_FzSmile\Debug
FX049.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_squeak\Debug
FX050.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSAMP_acoustic\Debug
FX051.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_SVT\Debug
FX052.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_PDL_B_PDLMNP\Debug
FX053.ZDL
__TI_internal
C:\project\ZDL\D264\ZDL_SFX_4VoiceSyn\Debug
FX054.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_REV_Air\Debug
FX055.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_REV_Arena\Debug
FX056.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_SFX_AutoPan\Debug
FX057.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_BendCho\Debug
FX058.ZDL
FX059.ZDL
__TI_internal
C:\Project\ZDL\D262\ZDL_MOD_HPS\Debug
FX060.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_MojoRolle\Debug
FX061.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_MultiTapD\Debug
FX062.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_PitchDly\Debug
FX063.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_MOD_RingMod\Debug
FX064.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_FLT_RndmFLTR\Debug
FX065.ZDL
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_MOD_StereoCho\Debug
FX066.ZDL
__TI_internal
C:\project\ZDL\D237\ZDL_FLT_Step\Debug
FX067.ZDL
__TI_internal
C:\Project\ZDL\D262\ZDL_DLY_TapeEcho\Debug
FX068.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_TrgHldDly\Debug
FX069.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_REV_TiledRoom\Debug
FX070.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_VinFLNGR\Debug
FX071.ZDL
FX072.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_WarpPhase\Debug
FX073.ZDL
__TI_internal
C:\project\ZDL\D242\ZDL_SFX_Z_Organ\Debug
FX074.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Z_Tron\Debug
FX075.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_T_Scream\Debug
FX076.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_B_FzSmile\Debug
FX077.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_squeak\Debug
FX078.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_PDL_B_PDLMNP\Debug
FX079.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_PDL_B_PDLPIT\Debug
FX080.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_T_Scream\Debug
FX081.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_B_FzSmile\Debug
FX082.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_squeak\Debug
FX083.ZDL
__TI_internal
C:\Project\ZDL\D249\ZDL_DYN_160_Comp\Debug
FX084.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_A_Filter\Debug
FX085.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_SFX_BitCrush\Debug
FX086.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_SFX_Bomber\Debug
FX087.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Bottom_B\Debug
FX088.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_BaAutoWah\Debug
FX089.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_MOD_Ba_Chorus\Debug
FX090.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Ba_Cry\Debug
FX091.ZDL
__TI_internal
C:\Project\ZDL\D249\ZDL_MOD_Ba_Detune\Debug
FX092.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_MOD_Ba_Ensmbl\Debug
FX093.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_MOD_BaFlanger\Debug
FX094.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Ba_GEQ\Debug
FX095.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_MOD_Ba_Octave\Debug
FX096.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_PDL_B_PDLMNP\Debug
FX097.ZDL
__TI_internal
C:\Project\ZDL\D264\ZDL_PDL_B_PDLPIT\Debug
FX098.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Ba_PEQ\Debug
FX099.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_MOD_Ba_Pitch\Debug
FX100.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_SFX_Ba_Synth\Debug
FX101.ZDL
__TI_internal
C:\Project\ZDL\D250\ZDL_MOD_CORONATRI\Debug
FX102.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_SFX_Defret\Debug
FX103.ZDL
__TI_internal
C:\Project\ZDL\D262\ZDL_DLY_Delay\Debug
FX104.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_MOD_DuoPhase\Debug
FX105.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_DYN_D_Comp\Debug
FX106.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_REV_EarlyRef\Debug
FX107.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_FLT_Exciter\Debug
FX108.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_DLY_FilterDly\Debug
FX109.ZDL
__TI_internal
C:\Project\ZDL\D262\ZDL_REV_Hall\Debug
FX110.ZDL
__TI_internal
C:\Project\ZDL\D237\ZDL_REV_HD_Hall\Debug
FX111.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_DYN_Limiter\Debug
FX112.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_DLY_ModDelay2\Debug
FX113.ZDL
FX114.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_DYN_M_Comp\Debug
FX115.ZDL
__TI_internal
C:\Project\ZDL\D262\ZDL_FLT_M_Filter\Debug
FX116.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_DYN_OptComp\Debug
FX117.ZDL
__TI_internal
C:\Project\ZDL\D250\ZDL_REV_PerticleR\Debug
FX118.ZDL
FX119.ZDL
FX120.ZDL
FX121.ZDL
__TI_internal
C:\Project\ZDL\D237\ZDL_MOD_Phaser\Debug
FX122.ZDL
FX123.ZDL
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_MOD_PitchSHFT\Debug
FX124.ZDL
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_REV_Room\Debug
FX125.ZDL
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_DLY_ReverseDL\Debug
FX126.ZDL
__TI_internal
C:\Project\ZDL\D262\ZDL_FLT_SeqFLTR\Debug
FX127.ZDL
__TI_internal
C:\project\ZDL\D222\ZDL_REV_SLAPBACK\Debug
FX128.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_MOD_Slicer\Debug
FX129.ZDL
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_DYN_SlowATTCK\Debug
FX130.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Splitter\Debug
FX131.ZDL
__TI_internal
C:\Project\ZDL\D242\ZDL_DLY_StereoDly\Debug
FX132.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_SFX_StdSyn\Debug
FX133.ZDL
__TI_internal
C:\project\ZDL\D237\ZDL_DLY_StompDly\Debug
FX134.ZDL
__TI_internal
C:\project\ZDL\D249\ZDL_SFX_SynTlk\Debug
FX135.ZDL
__TI_internal
C:\Project\ZDL\D237\ZDL_MOD_TheVibe\Debug
FX136.ZDL
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_MOD_Tremolo\Debug
FX137.ZDL



```