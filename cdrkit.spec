%define name	cdrkit
%define release	%mkrel 5
%define version	1.1.6

Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Summary:	A command line CD/DVD-Recorder
Group:		Archiving/Cd burning
URL:		http://cdrkit.org/
Source:		http://cdrkit.org/releases/%{name}-%{version}.tar.gz
Requires(pre):	/usr/sbin/groupadd rpm-helper
Obsoletes:	cdrecord-dvdhack =< 4:2.01-0.a15.2mdk cdrecord =< 4:2.01.01-0.a11-3mdv
Provides:	cdrecord-dvdhack = 4:2.01.01-1mdv cdrecord = 4:2.01.01-1mdv
BuildRequires:	libcap-devel cmake zlib-devel

%package icedax
Summary:	CD-Audio to .wav converter
Group:		Sound
Obsoletes:	cdrecord-cdda2wav <= 4:2.01.01-0.a11.3mdv
Provides:	cdrecord-cdda2wav
Requires(pre):	rpm-helper

%package genisoimage
Group:		Archiving/Cd burning
Obsoletes:	mkisofs <= 1:2.01.01-0.a11.3mdv
Provides:	mkisofs
Summary:	Creates an image of an ISO9660 filesystem

%package isotools
Group:		Archiving/Cd burning
Obsoletes:	cdrecord-isotools
Provides:	cdrecord-isotools
Conflicts:	cdrecord =< 4:2.01.01-0.a11.3mdv
Summary:	Collection of ISO files related tools
Requires(pre):	/usr/sbin/groupadd rpm-helper

%description
wodim allows you to create CDs and DVDs on a CD-Recorder or DVD-Recorder
(SCSI/ATAPI). It supports data, audio, mixed, multi-session, CD+, DVD,
DVD-Video discs etc.

%description icedax
icedax reads audio CDs, outputting a wav file.

%description genisoimage
genisoimage is used to create ISO 9660 file system images for creating
CD-ROMs. Now includes support for making bootable "El Torito" CD-ROMs.

%description isotools
This package is a collection of ISO 9660 commands to dump and test images:
isodebug, isodump, isoinfo, isovfy, devdump.

%prep
%setup -q -n %{name}-%{version}

%build
%make

%install
perl -pi -e 's!local/bin/perl!bin/perl!' ./doc/icedax/tracknames.pl
%makeinstall PREFIX=%{buildroot}%{_prefix}

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(-,root,root) %doc FAQ TODO FORK VERSION START INSTALL ABOUT doc/DOC-OVERVIEW doc/PORTABILITY doc/READMEs doc/WHY doc/plattforms doc/wodim/

%attr(755,root,cdwriter) %{_bindir}/wodim
%attr(755,root,cdwriter) %{_bindir}/readom
%attr(755,root,cdwriter) %{_sbindir}/netscsid
%attr(644,root,root) %{_mandir}/man1/wodim.1.*
%attr(644,root,root) %{_mandir}/man1/list_audio_tracks.1.*
%attr(644,root,root) %{_mandir}/man1/readom.1.*

%files isotools
%attr(-,root,root) %doc FAQ TODO FORK VERSION START INSTALL ABOUT
%attr(755,root,cdwriter) %{_bindir}/devdump
%attr(755,root,cdwriter) %{_bindir}/isodebug
%attr(755,root,cdwriter) %{_bindir}/isodump
%attr(755,root,cdwriter) %{_bindir}/isoinfo
%attr(755,root,cdwriter) %{_bindir}/isovfy
%attr(644,root,root) %{_mandir}/man1/devdump.1.*
%attr(644,root,root) %{_mandir}/man1/isodump.1.*
%attr(644,root,root) %{_mandir}/man1/isoinfo.1.*
%attr(644,root,root) %{_mandir}/man1/isovfy.1.*
%attr(644,root,root) %{_mandir}/man1/isodebug.1.*

%files genisoimage
%attr(-,root,root) %doc FAQ TODO FORK VERSION START INSTALL ABOUT
%attr(755,root,root) %{_bindir}/genisoimage
%attr(755,root,root) %{_bindir}/dirsplit
%attr(644,root,root) %{_mandir}/man1/genisoimage.1.*
%attr(644,root,root) %{_mandir}/man5/genisoimagerc.5.*
%attr(644,root,root) %{_mandir}/man1/dirsplit.1.*

%files icedax
%attr(-,root,root) %doc FAQ TODO FORK VERSION START INSTALL ABOUT doc/icedax 
%attr(755,root,cdwriter) %{_bindir}/icedax
%attr(755,root,cdwriter) %{_bindir}/cdda2mp3
%attr(755,root,cdwriter) %{_bindir}/cdda2ogg
%attr(755,root,cdwriter) %{_bindir}/pitchplay
%attr(755,root,cdwriter) %{_bindir}/readmult
%attr(644,root,root) %{_mandir}/man1/readmult.1.*
%attr(644,root,root) %{_mandir}/man1/cdda2ogg.1.*
%attr(644,root,root) %{_mandir}/man1/icedax.1.*
%attr(644,root,root) %{_mandir}/man1/pitchplay.1.*
