HERE's how I got the Docker running

1 - ensure the VM has access to your Zoom pedal
2 - I built an image with the below in it
3 - I ran it interactively
3.0 - as root, allow access to all X11 hosts - naughty I know

xhost +

3.1 - sometimes I need 3 runs to get it working
3.2 - remove the containers

```
sudo docker run -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-h $HOSTNAME -v $HOME/.Xauthority:/home/lyonn/.Xauthority -it --rm \
--device /dev/snd python-zpf:latest
```
Cool.

When running these python 3 scripts note you will need
```
sudo apt-get install python-tk
sudo apt-get install python3-tk 
sudo apt-get install python-imaging-tk
sudo apt-get remove python3-pil python3-pil.imagetk python-pil.imagetk python-pil
sudo apt-get install python3-pil.imagetk # Note that python3-pil installed as a dependency
sudo apt install -y jackd2
sudo apt install -y jackd1
sudo apt install -y alsa-tools
sudo apt install -y alsa-utils
sudo apt install -y libasound2-dev
sudo apt-get install -y libjack-dev
```
pip3 install these

Use a virtual env?
```
python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt
```
## this should install the following
cython
tk
pillow
construct
json5
mido
python-rtmidi

The rtmidi is incompatible with the mido!
