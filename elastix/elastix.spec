%define _ver_major      4
%define _ver_minor      6

Name:elastix
Summary: Toolbox for rigid and nonrigid registration of images
Version: %{_ver_major}.%{_ver_minor}
Release: 1%{?dist}
License: BSD
Group: Development/Libraries
Source0: http://elastix.isi.uu.nl/elastix_sources_v%{_ver_major}.%{_ver_minor}.tar.bz2
Source1: http://elastix.isi.uu.nl/elastix_manual_v%{_ver_major}.%{_ver_minor}.pdf
Source2: FindANN.cmake
URL: http://elastix.isi.uu.nl/

Patch1: elastix-0001-use_system_ann.patch
#Patch2: 0002-Moved-up-version-declarations-because-I-need-to-use-.patch
#Patch3: 0004-Fix-lib-install-directories.patch

BuildRequires: cmake
BuildRequires: InsightToolkit-devel
BuildRequires: ann-devel

%description
elastix is a program that registers (matches/aligns) images. 
The authors use it in their research on the registration of medical image data, 
but it may be used for any type of images.

It supports many registration methods, composed of various transform models 
(rigid, affine, nonrigid), similarity measures (for example mutual information),
optimisation methods (for example gradient descent), interpolation methods
(nearest neighbour, linear, cubic), and multi-resolution schemes. 
Components can easily be plugged in, to allow the user to configure his/her own
registration methods.

%package devel
Summary: Development Libraries for elastix
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development Libraries and Headers for elastix.  You only need to install
this if you are developing programs that use the elastix library.

%prep
%setup -qc elastix_v%{_ver_major}.%{_ver_minor}
%patch1 -p0
#%patch2 -p1
#%patch3 -p1

# remove bundled libs
rm -rf src/Common/KNN/ann_1.1

# Provide FindANN.cmake
cp -a %{SOURCE2} src/

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}

%cmake 	../src \
    -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"\
	-DBUILD_SHARED_LIBS=ON\
	-DELASTIX_BUILD_TESTING=ON\
	-DITK_DIR=/usr/lib64/cmake/InsightToolkit\
	-DUSE_ALL_COMPONENTS=ON\
	-DUSE_MEVISDICOMTIFF=ON


popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%files
%{_bindir}/*
%{_libdir}/*.so.*


%files devel
#%dir %{_includedir}/%{name}/
#%doc Examples
#%{_includedir}/%{name}/*
%{_libdir}/*.so
#%{_datadir}/gdcm/*.cmake

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Mon Jul 08 2013 Mario Ceresa mrceresa fedoraproject org - 4.6-1
- Updated release
- Updated spec to new guidelines

* Wed Mar 23 2011 Mario Ceresa mrceresa fedoraproject org - 4.4-1
- Initial release
