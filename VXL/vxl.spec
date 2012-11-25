
Name:		vxl	
Version:	1.17.0	
Release:	7%{?dist}
Summary:	C++ Libraries for Computer Vision Research and Implementation
Group:		Development/Libraries
License:	BSD
URL:		http://vxl.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/vxl/vxl/1.17/vxl-1.17.0.tar.gz
Source2:	https://vxl.svn.sourceforge.net/svnroot/vxl/trunk/core/vxl_copyright.h
# Fedora has a distribution-specific include dir
Patch1:		0001-Added-include-path-for-geotiff.patch
Patch2:		0002-Added-soname-info-for-core-libraries.patch
# Use system rply and don't use mpeg2
Patch3:		0003-Use-system-rply.patch
Patch4:		0004-Added-more-soname.patch
Patch5:		0005-Do-not-build-OUL.patch
Patch6:		0006-BUG-rplyConfig.cmake-has-wrong-include-path.patch
Patch7:		0007-Arguments-of-ply_open-and-create-changed.-Thanks-to-.patch
Patch8:		0008-More-sonames.patch
Patch9:		0009-Bumped-up-version-to-1.14.patch
#TODO: Refers to contrib and is therefore not correct
Patch10:	0010-Use-system-FindEXPAT.patch
Patch11:	0011-Do-not-use-bundled-minizip.patch
Patch12:	0012-Added-Coin3D-Submitted-by-Volker-Frohlich.patch
Patch13:	0013-Added-SIMVoleon-Submitted-by-Volker-Frohlich.patch
Patch14:	0014-Added-additional-search-path-for-xerces-Submitted-by.patch
Patch15:	0015-Manage-KL-library-Submitted-by-Volker-Frohlich.patch
Patch16:	0016-Manage-KL-library-2-2-Submitted-by-Volker-Frohlich.patch
Patch17:	0017-Add-sonames-to-vpgl-lib.patch
Patch18:	0018-Added-sonames-to-vgui-vidl-vpdl-Qv-libs.patch
Patch19:	0019-Removed-box2m-which-requires-OpenCL-libraries.patch
Patch20:	0020-Included-missing-vcl_cstdio.h-header.patch
Patch21:	0021-Use-expatpp.h-which-is-provided-by-fedora-repos.patch
Patch22:	0022-Include-missing-vcl_cstdio.h-header.patch
Patch23:	0023-Remove-volm-because-of-error-in-function-prototype.patch

#KL is used in an "UNMAINTAINED_LIBRARY", vgel is only built on request

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake 
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	Coin2-devel
BuildRequires:	dcmtk-devel
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	expatpp-devel
BuildRequires:	freeglut-devel
BuildRequires:	klt-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libXmu-devel 
BuildRequires:	libXi-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libdc1394-devel
BuildRequires:	libgeotiff-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	minizip-devel
BuildRequires:	rply-devel
BuildRequires:	SIMVoleon-devel
BuildRequires:	shapelib-devel
BuildRequires:	texi2html
BuildRequires:	xerces-c-devel
BuildRequires:	zlib-devel

#GUI needs wx, a desktop file and an icon

%description
VXL (the Vision-something-Libraries) is a collection of C++ libraries designed
for computer vision research and implementation. It was created from TargetJr
and the IUE with the aim of making a light, fast and consistent system. 
VXL is written in ANSI/ISO C++ and is designed to be portable over many
platforms.


%package	doc
Summary:	Documentation for VXL library
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc

You should install this package if you would like to
have all the documentation

%package	devel
Summary:	Headers and development libraries for VXL
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel

You should install this package if you would like to
develop code based on VXL.

%prep
%setup -q -n vxl-git4e07960

cp %{SOURCE2} .

#Remove bundled library (let's use FEDORA's ones)
# v3p/netlib (made by f2c) dependency not removed because of heavily modifications
# QV is a Silicon Graphics' VRML parser from the 90s. Now unmantained.
for l in jpeg png zlib tiff geotiff rply dcmtk bzlib
do
	find v3p/$l -type f ! -name 'CMakeLists.txt' -execdir rm {} +
done

find contrib/brl/b3p/shapelib -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/brl/b3p/minizip -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/brl/b3p/expat -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/gel/vgel/kl -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/brl/b3p/expatpp -type f ! -name 'CMakeLists.txt' -execdir rm {} +

# v3p/mpeg2 lib in fedora is not enough to build the target. Moreover it is in rpmfusion repo

#TODO: Various
#vxl-devel.x86_64: E: invalid-soname /usr/lib64/libvvid.so libvvid.so

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1


#Fix lib / lib64 problem during install:
find . -name CMakeLists.txt -exec sed -i "s/INSTALL_TARGETS([ ]*\/lib/INSTALL_TARGETS(\/lib\$\{LIB_SUFFIX\}/;" {} +

# Fix executable permissions on source file
find . -name "*.h" | xargs chmod ugo-x
find . -name "*.cxx" | xargs chmod ugo-x
find . -name "*.txx" | xargs chmod ugo-x

%build
%cmake -DCMAKE_VERBOSE_MAKEFILE=ON \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DVXL_FORCE_B3P_EXPAT:BOOL=OFF \
	-DVXL_FORCE_V3P_DCMTK:BOOL=OFF \
	-DVXL_FORCE_V3P_GEOTIFF:BOOL=OFF \
	-DVXL_USING_NATIVE_KL=ON \
	-DVXL_FORCE_V3P_JPEG:BOOL=OFF \
	-DVXL_FORCE_V3P_MPEG2:BOOL=OFF \
	-DVXL_FORCE_V3P_PNG:BOOL=OFF \
	-DVXL_FORCE_V3P_TIFF:BOOL=OFF \
	-DVXL_FORCE_V3P_ZLIB:BOOL=OFF \
	-DVXL_FORCE_V3P_RPLY:BOOL=OFF \
	-DVXL_USING_NATIVE_ZLIB=ON \
	-DVXL_USING_NATIVE_JPEG=ON \
	-DVXL_USING_NATIVE_PNG=ON \
	-DVXL_USING_NATIVE_TIFF=ON \
	-DVXL_USING_NATIVE_GEOTIFF=ON \
	-DVXL_USING_NATIVE_EXPAT=ON \
	-DVXL_USING_NATIVE_SHAPELIB=ON \
	-DVXL_USING_NATIVE_BZLIB2=ON \
	-DBUILD_VGUI=OFF \
	-DBUILD_BGUI3D=OFF \
	-DBUILD_OXL:BOOL=ON \
	-DBUILD_BRL=OFF \
	-DBUILD_CORE_GEOMETRY:BOOL=ON \
	-DBUILD_CORE_IMAGING:BOOL=ON \
	-DBUILD_CORE_NUMERICS:BOOL=ON \
	-DBUILD_CORE_PROBABILITY:BOOL=ON \
	-DBUILD_CORE_SERIALISATION:BOOL=ON \
	-DBUILD_CORE_UTILITIES:BOOL=ON \
	-DBUILD_CORE_VIDEO:BOOL=ON \
	-DBUILD_EXAMPLES:BOOL=OFF \
	-DBUILD_TESTING:BOOL=OFF \
	-DBUILD_DOCUMENTATION:BOOL=ON \
	-DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo" \
	-DCMAKE_CXX_FLAGS:STRING="-fpermissive" \
	-DPYTHON_LIBRARY=/usr/lib64/libpython2.7.so .

# Why is expat stated, but not shapelib?
# DCMDK Cmake -- Included in bundle, but why?
#BUILD_VGUI? NO, it depends on box2m which in turns relies on OPENCL which is not available in FEDORA
#wxwidgets seems to be found
#Multiple versions of QT found please set DESIRED_QT_VERSION
#TODO: Xerces for brl
#TODO: Testing?
#BR: coin2, coin3 (coin3d) brl, bbas

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%check
ctest .

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc core/vxl_copyright.h
%{_libdir}/*.so.*
%{_bindir}/*
#%{_datadir}/%{name}/

%files devel
%{_datadir}/%{name}
%{_includedir}/%{name}
%{_libdir}/*.so

%files doc
%doc %{_docdir}/*




%changelog
* Sun Nov 25 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-7%{?dist}
- Changed source0 path to point to vxl 1.17
- 

* Fri Nov 02 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-6%{?dist}
- Patched to build BRL
- Updated to last version

* Mon Oct 29 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-5%{?dist}
- Removed expatpp bundled library and added corresponding BR
- Removed bundled bzip


* Thu Oct 18 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-4%{?dist}
- Fixed missing oxl_vrml lib
- Turn on compilation of BRL

* Sun Oct 14 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-3%{?dist}
- More fixes from Volker's post https://bugzilla.redhat.com/show_bug.cgi?id=567086#c42
- 

* Wed Oct 10 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-2%{?dist}
- Added patches 12-16 from https://bugzilla.redhat.com/show_bug.cgi?id=567086#c42
- Minor rework of the spec file as pointed out by Volker in the previous link

* Wed Oct 10 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-1%{?dist}
- Updated to new version
- Reworked patches to the new version
- Disabled BRL because it gives a compilation error

* Fri May 27 2011 Mario Ceresa mrceresa fedoraproject org vxl 1.14.0-1%{?dist}
- Updated to new version
- Added BR doxygen (thanks to Ankur for noticing it)
- Changed patch naming schema
- Work around a rply related bug (patches 3-6)
- Thanks to Thomas Bouffon for patch 7-8
- Patches 9-10 address http://www.itk.org/pipermail/insight-users/2010-July/037418.html
- Fixed 70 missing sonames in patch 11
- Removed bundled expact, shapelib, minizip, dcmtk
- Force brl build
- Use system shipped FindEXPAT


* Tue Mar 23 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-4%{?dist}
- sed patch to add ${LIB_SUFFIX} to all lib install target
- Added soname version info to vil vil_algo lib

* Sun Mar 21 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-3%{?dist}
- Applied patch to build against newly packaged rply

* Tue Mar 2 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-2%{?dist}
- Applied patch from debian distribution to force the generation of versioned lib

* Sat Feb 19 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-1%{?dist}
- Initial RPM Release

