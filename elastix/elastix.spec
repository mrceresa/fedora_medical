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

# Contacted upstream to optionally use system wide ANNlib
Patch1: elastix-0001-Find-system-wide-ANN.patch
Patch2: elastix-0002-Conditional-build-bundled-lib.patch
Patch3: elastix-0003-Use-ANN-lib-dir.patch
Patch4: elastix-0004-Set-module-path.patch
Patch5: elastix-0005-Added-install-target-for-libs.patch
Patch6: elastix-0006-Add-rpath-for-internal-libs-only.patch

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

%package        doc
Summary:        Documentation for elastix
Group:          Documentation
BuildArch:      noarch

%description    doc
%{summary}.
This package contains additional documentation.

%prep
%setup -qc elastix_v%{_ver_major}.%{_ver_minor}
pushd src/
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
popd

# remove bundled libs
rm -rf src/Common/KNN/ann_1.1

# Copy user manual
cp -a %{SOURCE1} .

# Provide FindANN.cmake
cp -a %{SOURCE2} src/

%build
mkdir -p %{_target_platform}

pushd %{_target_platform}
%cmake 	../src \
    -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"\
	-DELASTIX_BUILD_TESTING=ON\
	-DITK_DIR=/usr/lib64/cmake/InsightToolkit\
	-DUSE_ALL_COMPONENTS=ON\
	-DELASTIX_USE_MEVISDICOMTIFF=ON\
	-DUSE_KNNGraphAlphaMutualInformationMetric=ON\
    -DINSTALL_LIB_PATH=%{_lib}/%{name}/ 
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%check
make test -C %{_target_platform}

%files
%{_bindir}/*
%{_libdir}/%{name}/*.so

%files doc
%doc elastix_manual_v%{_ver_major}.%{_ver_minor}.pdf

#%post -p /sbin/ldconfig
#%postun -p /sbin/ldconfig

%changelog
* Mon Jul 08 2013 Mario Ceresa mrceresa fedoraproject org - 4.6-1
- Updated release
- Updated spec to changes in guidelines
- Added user manual
- Install libraries as private plugins

* Wed Mar 23 2011 Mario Ceresa mrceresa fedoraproject org - 4.4-1
- Initial release

