So I found this git useful

https://github.com/mypalmike/csplitb

When I pip installed it I couldnt get it working from dos

So I did the following:

I created my own runner

import sys
from csplitb import CSplitB
csplitb = CSplitB("0000000053495A45", "../Zoom B1on System v1.30 Updater.exe", 3, "FX", ".ZDL")
csplitb.run()

and hence in my directory I got
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

So now to determine, from the OnOff patterns, which FX these are

This might do the trick?

$ for file in *.ZDL
> do
> strings $file | grep -A1 "__TI_internal"
> done
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_DYN_ZNR\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_SFX_Z_Syn\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_acoustic\Debug
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_AC_Bs_Pre\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_Ag_Amp\Debug
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_BassDrive\Debug
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSDRV_Bass_Muff\Debug
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_Bass_BB\Debug
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_Bass_Pre\Debug
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSDRV_Ba_Boost\Debug
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSDRV_Ba_Dist_1\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_B_MAN\Debug
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSDRV_Ba_Metal\Debug
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSDRV_Bass_OD\Debug
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_DI5\Debug
__TI_internal
C:\project\ZDL\D242_StompShare\forBASS\ZDL_BASSPREAMP_DI_Plus\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_FlipTop\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSAMP_GKrueger\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_Heaven\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_HRT3500\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_Mark_B\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_Monotone\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSAMP_SMR\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_SuperB\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_SVT\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_SFX_4VoiceSyn\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_REV_Air\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_REV_Arena\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_SFX_AutoPan\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_BendCho\Debug
__TI_internal
C:\Project\ZDL\D262\ZDL_MOD_HPS\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_MojoRolle\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_MultiTapD\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_PitchDly\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_MOD_RingMod\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_FLT_RndmFLTR\Debug
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_MOD_StereoCho\Debug
__TI_internal
C:\project\ZDL\D237\ZDL_FLT_Step\Debug
__TI_internal
C:\Project\ZDL\D262\ZDL_DLY_TapeEcho\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_TrgHldDly\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_REV_TiledRoom\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_VinFLNGR\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_WarpPhase\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_SFX_Z_Organ\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Z_Tron\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_T_Scream\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_B_FzSmile\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_squeak\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSAMP_acoustic\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_BASSAMP_SVT\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_PDL_B_PDLMNP\Debug
__TI_internal
C:\project\ZDL\D264\ZDL_SFX_4VoiceSyn\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_REV_Air\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_REV_Arena\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_SFX_AutoPan\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_BendCho\Debug
__TI_internal
C:\Project\ZDL\D262\ZDL_MOD_HPS\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_MojoRolle\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_MultiTapD\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_PitchDly\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_MOD_RingMod\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_FLT_RndmFLTR\Debug
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_MOD_StereoCho\Debug
__TI_internal
C:\project\ZDL\D237\ZDL_FLT_Step\Debug
__TI_internal
C:\Project\ZDL\D262\ZDL_DLY_TapeEcho\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_DLY_TrgHldDly\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_REV_TiledRoom\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_VinFLNGR\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_MOD_WarpPhase\Debug
__TI_internal
C:\project\ZDL\D242\ZDL_SFX_Z_Organ\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Z_Tron\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_T_Scream\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_B_FzSmile\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_squeak\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_PDL_B_PDLMNP\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_PDL_B_PDLPIT\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_T_Scream\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_B_FzSmile\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_BASSDRV_Ba_squeak\Debug
__TI_internal
C:\Project\ZDL\D249\ZDL_DYN_160_Comp\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_A_Filter\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_SFX_BitCrush\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_SFX_Bomber\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Bottom_B\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_BaAutoWah\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_MOD_Ba_Chorus\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Ba_Cry\Debug
__TI_internal
C:\Project\ZDL\D249\ZDL_MOD_Ba_Detune\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_MOD_Ba_Ensmbl\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_MOD_BaFlanger\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Ba_GEQ\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_MOD_Ba_Octave\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_PDL_B_PDLMNP\Debug
__TI_internal
C:\Project\ZDL\D264\ZDL_PDL_B_PDLPIT\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Ba_PEQ\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_MOD_Ba_Pitch\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_SFX_Ba_Synth\Debug
__TI_internal
C:\Project\ZDL\D250\ZDL_MOD_CORONATRI\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_SFX_Defret\Debug
__TI_internal
C:\Project\ZDL\D262\ZDL_DLY_Delay\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_MOD_DuoPhase\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_DYN_D_Comp\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_REV_EarlyRef\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_FLT_Exciter\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_DLY_FilterDly\Debug
__TI_internal
C:\Project\ZDL\D262\ZDL_REV_Hall\Debug
__TI_internal
C:\Project\ZDL\D237\ZDL_REV_HD_Hall\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_DYN_Limiter\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_DLY_ModDelay2\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_DYN_M_Comp\Debug
__TI_internal
C:\Project\ZDL\D262\ZDL_FLT_M_Filter\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_DYN_OptComp\Debug
__TI_internal
C:\Project\ZDL\D250\ZDL_REV_PerticleR\Debug
__TI_internal
C:\Project\ZDL\D237\ZDL_MOD_Phaser\Debug
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_MOD_PitchSHFT\Debug
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_REV_Room\Debug
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_DLY_ReverseDL\Debug
__TI_internal
C:\Project\ZDL\D262\ZDL_FLT_SeqFLTR\Debug
__TI_internal
C:\project\ZDL\D222\ZDL_REV_SLAPBACK\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_MOD_Slicer\Debug
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_DYN_SlowATTCK\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_FLT_Splitter\Debug
__TI_internal
C:\Project\ZDL\D242\ZDL_DLY_StereoDly\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_SFX_StdSyn\Debug
__TI_internal
C:\project\ZDL\D237\ZDL_DLY_StompDly\Debug
__TI_internal
C:\project\ZDL\D249\ZDL_SFX_SynTlk\Debug
__TI_internal
C:\Project\ZDL\D237\ZDL_MOD_TheVibe\Debug
__TI_internal
C:\Project\D237Base\Program\C6745V2\ZDL_MOD_Tremolo\Debug
