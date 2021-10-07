@echo off
forfiles /m *.dat /C "cmd /c python checkme.py @file"
rem for /f %%g in ('*.dat') do python checkme.py %%g
@echo on