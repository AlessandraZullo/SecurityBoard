sudo apt-get install autoconf libtool libusb-dev libpcsclite-dev build-essential
sudo apt install libglib2.0-dev
https://github.com/nfc-tools/libnfc/
tar -jxvf libnfc-1.8.1.tar.bz2
cd libnfc-1.8.1
autoreconf -vis
./configure --with-drivers=all --sysconfdir=/etc --prefix=/usr
make
sudo make install
nfc-list
git clone https://github.com/nfc-tools/mfoc-hardnested.git
sudo apt install liblzma-dev
autoreconf -vis
./configure
make && sudo make install
mfoc-hardnested -O test.dmp
