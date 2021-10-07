%define _disable_ld_no_undefined 1
%global optflags %optflags -Wno-error=format-security -fno-strict-aliasing -fcommon

%define develname %mklibname usal -d
%define libusal %mklibname usal 0
%define librols %mklibname rols 0

Summary:	A command line CD/DVD-Recorder
Name:		cdrkit
Version:	1.1.11
Release:	22
License:	GPLv2+
Group:		Archiving/Cd burning
Url:		http://cdrkit.org/
Source0:	http://cdrkit.org/releases/%{name}-%{version}.tar.gz
Patch1:		cdrkit-1.1.8-werror.patch
Patch2:		cdrkit-1.1.9-efi-boot.patch
Patch4:		cdrkit-1.1.9-no_mp3.patch
Patch5:		cdrkit-1.1.9-buffer_overflow.patch
Patch6:		cdrkit-1.1.10-build-fix.patch
Patch7:		cdrkit-1.1.11-manpagefix.patch
Patch8:		cdrkit-1.1.11-rootstat.patch
Patch9:		cdrkit-1.1.11-usalinst.patch
Patch10:	cdrkit-1.1.11-readsegfault.patch
Patch11:	cdrkit-1.1.11-format.patch
Patch12:	cdrkit-1.1.11-handler.patch
Patch13:	cdrkit-1.1.11-dvdman.patch
Patch14:	cdrkit-1.1.11-paranoiacdda.patch
Patch15:	cdrkit-1.1.11-utf8.patch
Patch16:	cdrkit-1.1.11-cmakewarn.patch
Patch17:	cdrkit-1.1.11-memset.patch
Patch19:	cdrkit-1.1.11-ppc64le_elfheader.patch
Patch20:	cdrkit-1.1.11-werror_gcc5.patch
Patch21:	cdrkit-1.1.11-devname.patch
Patch22:	cdrkit-1.1.11-sysmacros.patch
Patch23:	cdrkit-1.1.11-gcc10.patch
BuildRequires:	cmake
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(libcdio_paranoia)
BuildRequires:	magic-devel
BuildRequires:	pkgconfig(zlib)
BuildRequires:	rpm-helper
BuildRequires:	cdda-devel
Requires(pre):	shadow
Requires(pre,post):	rpm-helper
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
Requires(pre,post,postun):	rpm-helper

%description icedax
icedax reads audio CDs, outputting a wav file.

%package genisoimage
Summary:	Creates an image of an ISO9660 filesystem
Group:		Archiving/Cd burning
Provides:	mkisofs
Provides:	genisoimage
Requires(post,postun):	rpm-helper

%description genisoimage
genisoimage is used to create ISO 9660 file system images for creating
CD-ROMs. Now includes support for making bootable "El Torito" CD-ROMs.

%package isotools
Group:		Archiving/Cd burning
Summary:	Collection of ISO files related tools
Provides:	cdrecord-isotools
Requires(pre):	shadow
Requires(pre,postun):	rpm-helper

%description isotools
This package is a collection of ISO 9660 commands to dump and test images:
isodebug, isodump, isoinfo, isovfy, devdump.

%package -n %{develname}
Summary:	Development files for using cdrkit's libraries
Group:		Development/C
Requires:	%{libusal} = %{EVRD}
Requires:	%{librols} = %{EVRD}

%description -n %{develname}
Development files for using cdrkit's libraries

%prep
%setup -q

%patch1 -p1 -b .werror
%patch2 -p1 -b .efi
%patch4 -p1 -b .no_mp3
%patch5 -p1 -b .buffer_overflow
%patch6 -p1 -b .build-fix
%patch7 -p1 -b .manpagefix
%patch8 -p1 -b .rootstat
%patch9 -p1 -b .usalinst
%patch10 -p1 -b .readsegfault
%patch11 -p1 -b .format
%patch12 -p1 -b .handler
%patch13 -p1 -b .dvdman
%patch14 -p1 -b .paranoiacdda
# not using -b since otherwise backup files would be included into rpm
%patch15 -p1
%patch16 -p1 -b .cmakewarn
%patch17 -p1 -b .edcspeed
%patch19 -p1 -b .elfheader
%patch20 -p1 -b .werror_gcc5
%patch21 -p1 -b .devname
%patch22 -p1 -b .sysmacros

# we do not want bundled paranoia library
rm -rf libparanoia

find . -type f -print0 | xargs -0 perl -pi -e 's#/usr/local/bin/perl#/usr/bin/perl#g'
find doc -type f -print0 | xargs -0 chmod a-x

%build
%cmake
%make_build

%install
sed -i -e 's!local/bin/perl!bin/perl!' ./doc/icedax/tracknames.pl
%make_install -C build

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

%libpackage rols 0

%libpackage usal 0

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

%files -n %{develname}
%{_libdir}/*.so
%{_includedir}/usal
