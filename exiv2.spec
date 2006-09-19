
Summary: Exif and Iptc metadata manipulation library
Name:	 exiv2
Version: 0.11
Release: 2%{?dist} 

License: GPL
Group:	 Applications/Multimedia
URL: 	 http://www.exiv2.org/
Source0: http://www.exiv2.org/exiv2-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: zlib-devel

Patch1: exiv2-0.11-no_rpath.patch
Patch2: exiv2-0.9.1-deps.patch
Patch3: exiv2-0.11-pkgconfig.patch


%description
Exiv2 comprises of a C++ library and a command line utility to access image
metadata. Exiv2 supports full read and write access to the Exif and Iptc
metadata, Exif MakerNote support, extract and delete methods for Exif
thumbnails, classes to access Ifd and so on.
The command line utility allows you to:
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
Group:	 Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
%description devel
%{summary}.


%prep
%setup -q

%patch1 -p1 -b .no_rpath
%patch2 -p1 -b .deps
%patch3 -p1 -b .pkgconfig


%build
%configure --disable-static 

make -C src %{?_smp_mflags} 


%install
rm -rf $RPM_BUILD_ROOT 

make -C src install DESTDIR=$RPM_BUILD_ROOT

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

# set eXecute bit on installed lib
chmod a+x $RPM_BUILD_ROOT%{_libdir}/libexiv2-*.so

## FIXME/TODO: patch installed exiv2-config to instead pull values from pkgconfig


%clean
rm -rf $FPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/exiv2
%{_libdir}/libexiv2-*.so
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_bindir}/exiv2-config
%{_includedir}/exiv2/
%{_libdir}/libexiv2.so
%{_libdir}/pkgconfig/exiv2.pc


%changelog
* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-2
- BR: zlib-devel

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-1
- 0.11

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
