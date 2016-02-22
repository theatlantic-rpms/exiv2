
## enable experimental cmake build support (or not)
## still lacks some features, like visibility
#define cmake_build 1

Summary: Exif and Iptc metadata manipulation library
Name:	 exiv2
Version: 0.25
Release: 3%{?dist}

License: GPLv2+
URL: 	 http://www.exiv2.org/
Source0: http://www.exiv2.org/exiv2-%{version}%{?pre:-%{pre}}.tar.gz

## upstream patches

## upstreamable patches
# support LIB_SUFFIX, and avoid hard-coded rpath while we're at it
Patch50: exiv2-0.25-cmake_LIB_SUFFIX.patch
Patch51: exiv2-0.24-cmake_mandir.patch
Patch52: exiv2-0.24-doxygen_config.patch

%if 0%{?cmake_build}
BuildRequires: cmake
%endif
BuildRequires: expat-devel
BuildRequires: gettext
BuildRequires: pkgconfig
BuildRequires: zlib-devel
# docs
BuildRequires: doxygen graphviz libxslt

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
A command line utility to access image metadata, allowing one to:
* print the Exif metadata of Jpeg images as summary info, interpreted values,
  or the plain data for each tag
* print the Iptc metadata of Jpeg images
* print the Jpeg comment of Jpeg images
* set, add and delete Exif and Iptc metadata of Jpeg images
* adjust the Exif timestamp (that's how it all started...)
* rename Exif image files according to the Exif timestamp
* extract, insert and delete Exif metadata (including thumbnails),
  Iptc metadata and Jpeg comments

%package devel
Summary: Header files, libraries and development documentation for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package libs
Summary: Exif and Iptc metadata manipulation library
%description libs
A C++ library to access image metadata, supporting full read and write access
to the Exif and Iptc metadata, Exif MakerNote support, extract and delete 
methods for Exif thumbnails, classes to access Ifd and so on.

%package doc
Summary: Api documentation for %{name}
BuildArch: noarch
%description doc
%{summary}.


%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}

%patch50 -p1 -b .cmake_LIB_SUFFIX
%patch51 -p1 -b .cmake_mandir
%patch52 -p1 -b .doxygen_config


%build

# exiv2: embedded copy of exempi should be compiled with BanAllEntityUsage
# https://bugzilla.redhat.com/show_bug.cgi?id=888769
export CPPFLAGS="-DBanAllEntityUsage=1"

%if 0%{?cmake_build}
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DEXIV2_ENABLE_BUILD_PO:BOOL=ON \
  -DEXIV2_ENABLE_BUILD_SAMPLES:BOOL=OFF \
  ..

make %{?_smp_mflags}
make doc -k ||:
popd
%else
%configure \
  --disable-rpath \
  --disable-static 

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}
make doc -k ||:
%endif


%install
%if 0%{?cmake_build}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%else
make install DESTDIR=%{buildroot}

## fix perms on installed lib
ls -l     %{buildroot}%{_libdir}/libexiv2.so.*
chmod 755 %{buildroot}%{_libdir}/libexiv2.so.*
%endif

%find_lang exiv2

## unpackaged files
rm -fv %{buildroot}%{_libdir}/pkgconfig/exiv2.lsm
rm -fv %{buildroot}%{_libdir}/libexiv2.la


%check
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion exiv2)" = "%{version}"
test -x %{buildroot}%{_libdir}/libexiv2.so


%files 
%doc COPYING README
%{_bindir}/exiv2
%{_mandir}/man1/*

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs -f exiv2.lang
%{_libdir}/libexiv2.so.14*

%files devel
%{_includedir}/exiv2/
%{_libdir}/libexiv2.so
%{_libdir}/pkgconfig/exiv2.pc

%files doc
%doc doc/html


%changelog
* Mon Feb 22 2016 Rex Dieter <rdieter@fedoraproject.org> 0.25-3
- embedded copy of exempi should be compiled with BanAllEntityUsage (#888769)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 22 2015 Rex Dieter <rdieter@fedoraproject.org> 0.25-1
- exiv2-0.25 (#1234185)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Rex Dieter <rdieter@fedoraproject.org> 0.24-6
- rebuild (gcc5)

* Thu Feb 19 2015 Rex Dieter <rdieter@fedoraproject.org> 0.24-5
- rebuild (gcc5)

* Mon Jan 05 2015 Rex Dieter <rdieter@fedoraproject.org> 0.24-4
- CVE-2014-9449 exiv2: buffer overflow in RiffVideo::infoTagsHandler (#1178909)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.24-1
- exiv2-0.24, abi bump
- -doc subpkg
- ready experimental cmake buildsystem support

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Rex Dieter <rdieter@fedoraproject.org> 0.23-3
- empty html doc dir (#848025)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Rex Dieter <rdieter@fedoraproject.org> 0.23-1
- exiv2-0.23
- abi bump

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-5
- Rebuilt for c++ ABI breakage

* Mon Jan 16 2012 Rex Dieter <rdieter@fedoraproject.org> 0.22-4
- better rpath handling
- revert locale change, move back to -libs

* Mon Jan 16 2012 Rex Dieter <rdieter@fedoraproject.org> 0.22-3
- move locale files to main pkg (from -libs)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> 0.22-1
- exiv2-0.22

* Tue Sep 27 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21.1-3
- New Tamron 70-300 mm lens improperly recognized (#708403)

* Mon Sep 26 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21.1-2
- gthumb crashes because of bug in exiv2 0.21.1 (#741429)

* Sat Feb 26 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21.1-1
- exiv2-0.21.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21-2
- Move ldconfig scriptlet calls to -libs (#672361)

* Wed Dec 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.21-1
- exiv2-0.21

* Sun May 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.20-1
- exiv2-0.20

* Wed Dec 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.19-1
- exiv2-0.19 (#552275)

* Sun Dec 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-3
- -libs unconditional
- tighten deps using %%?_isa

* Fri Aug 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-2
- (again) drop -fvisibility-inlines-hidden (#496050)

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-1
- exiv2-0.18.2
- drop visibility patch

* Fri Apr 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.1-1
- exiv2-0.18.1
- drop -fvisibility-inlines-hidden (#496050)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> 0.18-1
- exiv2-0.18

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.17.2-2
- rebuild for pkgconfig deps

* Mon Jun 23 2008 Rex Dieter <rdieter@fedoraproject.org> 0.17.1-1
- exiv2-0.17.1

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> 0.16-2
- respin (gcc43)
- gcc43 patch

* Sun Jan 13 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-1
- eviv2-0.16

* Mon Dec 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.3.pre1
- CVE-2007-6353 (#425924)

* Mon Nov 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.2.pre1
- -libs subpkg toggle (f8+)

* Tue Nov 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.1.pre1
- exiv2-0.16-pre1

* Tue Sep 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-4
- -libs: -Requires: %%name

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-3
- -libs subpkg to be multilib-friendlier (f8+)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-2
- License: GPLv2+

* Thu Jul 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-1
- exiv2-0.15

* Mon Apr 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.14-1
- exiv2-0.14

* Tue Nov 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.12-1
- exiv2-0.12

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-3
- respin

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-2
- BR: zlib-devel

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-1
- exiv2-0.11

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.10-2
- fc6 respin

* Sat Jun 03 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.10-1
- 0.10

* Wed May 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-3
- cleanup %%description
- set eXecute bit on installed lib.
- no_rpath patch
- deps patch (items get (re)compiled on *every* call to 'make')

* Wed May 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-2
- %%post/%%postun: /sbin/ldconfig

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-1
- first try
