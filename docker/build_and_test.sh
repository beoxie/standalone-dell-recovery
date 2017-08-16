#!/bin/sh -e
BASE=/build
OUTPUT=$BASE/out
BINARY=$OUTPUT/binary

#clone/build/install dell-recovery
mkdir -p $OUTPUT
cd $BASE
ln -s /bin/true /bin/make
python3 setup.py build
python3 setup.py install --install-layout=deb

#add in our customizations
cp standalone/overrides/* / -R
cp standalone/overrides/etc/skel/.fluxbox /root -R
for f in standalone/hooks/*; do
	sh "$f" || exit 1
done

#generate squashfs
rm -rf $BINARY
mkdir -p $BINARY/live
mkdir -p $OUTPUT/tmp/dev $OUTPUT/tmp/proc $OUTPUT/tmp/sys
mksquashfs	/bin  					\
		/etc					\
		$OUTPUT/tmp/dev				\
		/home					\
		/lib					\
		/lib32					\
		/lib64					\
		/libx32					\
		/media					\
		/mnt					\
		/opt					\
		$OUTPUT/tmp/proc			\
		/root					\
		/run					\
		/sbin					\
		$OUTPUT/tmp/sys				\
		/srv					\
		/tmp					\
		/usr					\
		/var					\
		$BINARY/live/filesystem.squashfs	\
		-e /usr/bin/fbsetbg			\
		-e /usr/lib/gcc/			\
		-e /var/lib/apt/			\
		-e /var/lib/dpkg/			\
		-e /usr/share/man/			\
		-e /usr/share/doc/			\
		-e /usr/lib/python3/dist-packages/git/ 	\
		-noappend				\
		-comp xz

#prepare non-squashfs content for ISO image
cp -R standalone/bootloader/* $BINARY
cp /boot/vmlinuz* $BINARY/live/vmlinuz
cp /boot/initrd* $BINARY/live/initrd.img
mkdir -p $BINARY/IMAGE

#generate ISO image
set -x
xorriso								\
	-as mkisofs 						\
	-R 							\
	-r							\
	-J							\
	-joliet-long						\
	-l							\
	-cache-inodes						\
	-iso-level 3						\
	-A "Dell Recovery"					\
	-p Dell							\
	-publisher Dell						\
	-o $OUTPUT/dell-recovery-standalone.iso			\
	-e boot/grub/efi.img					\
	-no-emul-boot						\
	-append_partition 2 0xef $BINARY/boot/grub/efi.img	\
	-partition_cyl_align all				\
	$BINARY
