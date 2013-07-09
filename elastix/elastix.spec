Name: elastix
Summary: Toolbox for rigid and nonrigid registration of images
Version: 4.4
Release: 1%{?dist}
License: BSD
Group: Development/Libraries
Source: http://elastix.isi.uu.nl/elastix_sources_svn.tar.bz2
URL: http://elastix.isi.uu.nl/
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Patch1: 0001-Added-soname-info.-Watch-out-ANNlib-needs-to-be-unbu.patch
Patch2: 0002-Moved-up-version-declarations-because-I-need-to-use-.patch
Patch3: 0004-Fix-lib-install-directories.patch

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

elastix is a command line driven program. Most configuration settings are defined 
in a parameter file. This makes it possible to use scripts that run registrations
with varying parameters, on large databases of images, fully automatically. 
In this way the effect of each parameter can be thoroughly investigated and 
different methods can be compared systematically.

The program is aimed at research environments. For most applications a nice 
graphical user interface will be desired, and optimised parameter settings 
for the specific application.

%package devel
Summary: Development Libraries for elastix
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development Libraries and Headers for elastix.  You only need to install
this if you are developing programs that use the elastix library.

%prep
%setup -qn elastix_svn
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%cmake 	-DCMAKE_BUILD_TYPE:STRING="Release"\
	-DBUILD_SHARED_LIBS=OFF\
	-DITK_DIR=/usr/lib64/InsightToolkit\
	-DELASTIX_BUILD_TESTING=ON\
	-DELASTIX_USE_MEVISDICOMTIFF=ON\
	-DUSE_AffineDTITransformElastix=ON\
	-DUSE_BSplineInterpolatorFloat=ON\
	-DUSE_BSplineResampleInterpolatorFloat=ON\
	-DUSE_BSplineTransformWithDiffusion=ON\
	-DUSE_ConjugateGradientFRPR=ON\
	-DUSE_FixedShrinkingPyramid=ON\
	-DUSE_LinearInterpolator=ON\
	-DUSE_LinearResampleInterpolator=ON\
	-DUSE_MovingShrinkingPyramid=ON\
	-DUSE_MutualInformationHistogramMetric=ON\
	-DUSE_NearestNeighborInterpolator=ON\
	-DUSE_NearestNeighborResampleInterpolator=ON\
	-DUSE_RSGDEachParameterApart=ON\
	-DUSE_ViolaWellsMutualInformationMetric=ON\
	 src/

# Make sure all variables (KNN_libraries amog all) are correctly generated
%cmake src/


#make %{?_smp_mflags}
# Too much parallelism brakes the build (-j 8 on my pc)
make -j 4

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root)
#%dir %{_includedir}/%{name}/
#%doc Examples
#%{_includedir}/%{name}/*
%{_libdir}/*.so
#%{_datadir}/gdcm/*.cmake


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Wed Mar 23 2011 Mario Ceresa mrceresa gmailcom 4.4-1
- Initial release