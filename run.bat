@ECHO off

pip install -r requirements.txt
set PATH=%~dp0\lib\vips-dev-8.16\bin;%PATH%
python mrxs_to_svs_pyvips.py