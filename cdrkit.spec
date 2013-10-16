Summary:	A command line CD/DVD-Recorder
Name:		cdrkit
Version:	1.1.11
Release:	9
License:	GPLv2+
Group:		Archiving/Cd burning
Url:		http://cdrkit.org/
Source0:	http://cdrkit.org/releases/%{name}-%{version}.tar.gz
Patch0:		cdrkit-1.1.9-wformat-error.patch
# (helio) fix build with cmake 2.8
Patch2:         cdrkit-1.1.9-cmake2.8-build.patch
# (fc) 1.1.9-3mdv fix buffer overflow in wodim (Fedora)
Patch4:		cdrkit-1.1.9-buffer_overflow.patch
Patch5:         cdrkit-1.1.9-efi-boot.patch
BuildRequires:	cmake
BuildRequires:	bzip2-devel
BuildRequires:	libcap-devel
BuildRequires:	magic-devel
BuildRequires:	pkgconfig(zlib)
Requires(pre):	shadow-utils
Requires(pre):	rpm-helper
Provides:	cdrecord-dvdhack = 4:2.01.01-1
Provides:	cdrecord = 4:2.01.01-1

%description
wodim allows you to create CDs and DVDs on a CD-Recorder or DVD-Recorder
(SCSI/ATAPI). It supports data, audio, mixed, multi-session, CD+, DVD,
DVD-Video discs etc.

%package icedax
Summary:	CD-Audio to .wav converter
Group:		Sound
Provides:	cdrecord-cdda2wav
Requires(pre):	rpm-helper

%description icedax
icedax reads audio CDs, outputting a wav file.

%package genisoimage
Summary:	Creates an image of an ISO9660 filesystem
Group:		Archiving/Cd burning
Provides:	mkisofs
Provides:	genisoimage

%description genisoimage
genisoimage is used to create ISO 9660 file system images for creating
CD-ROMs. Now includes support for making bootable "El Torito" CD-ROMs.

%package isotools
Group:		Archiving/Cd burning
Summary:	Collection of ISO files related tools
Provides:	cdrecord-isotools
Requires(pre):	shadow-utils
Requires(pre):	rpm-helper

%description isotools
This package is a collection of ISO 9660 commands to dump and test images:
isodebug, isodump, isoinfo, isovfy, devdump.

%prep
%setup -q
%apply_patches

%build
%cmake

%make

%install
sed -i -e 's!local/bin/perl!bin/perl!' ./doc/icedax/tracknames.pl
%makeinstall_std -C build

%pre
%_pre_groupadd cdwriter

%postun
%_postun_groupdel cdwriter
if [ "$1" = "0" ]; then
  update-alternatives --remove cdrecord %{_bindir}/wodim
  update-alternatives --remove readcd %{_bindir}/readom
fi

%pre icedax
%_pre_groupadd cdwriter

%post icedax
update-alternatives --install %{_bindir}/cdda2wav cdda2wav %{_bindir}/icedax 10 \
    --slave %_mandir/man1/cdda2wav.1%{_extension} cdda2wav.1%{_extension} %_mandir/man1/icedax.1%{_extension}

%postun icedax
%_postun_groupdel cdwriter
if [ "$1" = "0" ]; then
  update-alternatives --remove cdda2wav %{_bindir}/icedax
fi

%pre isotools
%_pre_groupadd cdwriter

%postun isotools
%_postun_groupdel cdwriter

%post
update-alternatives --install %{_bindir}/cdrecord cdrecord %{_bindir}/wodim 10 \
    --slave %_mandir/man1/cdrecord.1%{_extension} cdrecord.1%{_extension} %_mandir/man1/wodim.1%{_extension}
update-alternatives --install %{_bindir}/readcd readcd %{_bindir}/readom 10 \
    --slave %_mandir/man1/readcd.1%{_extension} readcd.1%{_extension} %_mandir/man1/readom.1%{_extension}

%post genisoimage
update-alternatives --install %{_bindir}/mkisofs mkisofs %{_bindir}/genisoimage 10 \
    --slave %_mandir/man1/mkisofs.1%{_extension} mkisofs.1%{_extension} %_mandir/man1/genisoimage.1%{_extension}
update-alternatives --install %{_bindir}/mkhybrid mkhybrid %{_bindir}/genisoimage 10 \
    --slave %_mandir/man1/mkhybrid.1%{_extension} mkhybrid.1%{_extension} %_mandir/man1/genisoimage.1%{_extension}

%postun genisoimage
if [ "$1" = "0" ]; then
  update-alternatives --remove mkisofs %{_bindir}/genisoimage
  update-alternatives --remove mkhybrid %{_bindir}/genisoimage
fi

%files
%doc FAQ TODO FORK VERSION START ABOUT doc/DOC-OVERVIEW doc/PORTABILITY doc/READMEs doc/WHY doc/plattforms doc/wodim/
%{_bindir}/wodim
%{_bindir}/readom
%{_sbindir}/netscsid
%{_mandir}/man1/wodim.1*
%{_mandir}/man1/list_audio_tracks.1*
%{_mandir}/man1/readom.1*

%files isotools
%{_bindir}/devdump
%{_bindir}/isodebug
%{_bindir}/isodump
%{_bindir}/isoinfo
%{_bindir}/isovfy
%{_mandir}/man1/devdump.1*
%{_mandir}/man1/isodump.1*
%{_mandir}/man1/isoinfo.1*
%{_mandir}/man1/isovfy.1*
%{_mandir}/man1/isodebug.1*

%files genisoimage
%{_bindir}/genisoimage
%{_bindir}/dirsplit
%{_mandir}/man1/genisoimage.1*
%{_mandir}/man5/genisoimagerc.5*
%{_mandir}/man1/dirsplit.1*

%files icedax
%{_bindir}/icedax
%{_bindir}/cdda2mp3
%{_bindir}/cdda2ogg
%{_bindir}/pitchplay
%{_bindir}/readmult
%{_mandir}/man1/readmult.1*
%{_mandir}/man1/cdda2ogg.1*
%{_mandir}/man1/icedax.1*
%{_mandir}/man1/pitchplay.1*

