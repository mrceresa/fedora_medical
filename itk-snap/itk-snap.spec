%define _ver_major      2
%define _ver_minor      4
%define _ver_release    0

Name:           itk-snap
Summary:       	Semi-automatic segmentation of 3D medical images
Version:        %{_ver_major}.%{_ver_minor}.%{_ver_release}
Release:        1%{?dist}
License:        GPL 
Group:          Applications/Engineering
Source0:        http://sourceforge.net/projects/itk-snap/files/itk-snap/%{_ver_major}.%{_ver_minor}.%{_ver_release}/itksnap-%{_ver_major}.%{_ver_minor}.%{_ver_release}-20121121-source.tar.gz
URL:            http://www.itksnap.org
Patch0:         itksnap-0001-Removed-explicit-version-because-it-does-not-detect-.patch

BuildRequires:  cmake
BuildRequires:  vtk-devel
BuildRequires:  InsightToolkit-devel
BuildRequires:  fltk-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel

%description

SNAP is a software application used to segment structures in 3D medical images.
It provides semi-automatic segmentation using active contour methods, 
as well as manual delineation and image navigation. In addition to these 
core functions, SNAP provides a number of supporting utilities. 

Some of the core advantages of SNAP include:

* Linked cursor for seamless 3D navigation
* Manual segmentation in three orthogonal planes at once
* Friendly UI for selecting active contour segmentation parameters
* Support for many different 3D image formats, including NIfTI
* Support for concurrent, linked viewing and segmentation of multiple images
* Limited support for color images (e.g., diffusion tensor maps)
* 3D cut-plane tool for fast post-processing of segmentation results
* Extensive tutorial 

%prep
%setup -q -n itksnap-%{_ver_major}.%{_ver_minor}.%{_ver_release}

%patch0 -p1
%build

mkdir -p %{_target_platform}
pushd %{_target_platform}

%cmake .. \
       -DBUILD_SHARED_LIBS:BOOL=ON \
       -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"\
       -DCMAKE_VERBOSE_MAKEFILE=ON\
       -DCMAKE_CXX_FLAGS:STRING="-fpermissive"

popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%check
make test -C %{_target_platform} || exit 0

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%files
%doc LICENSE README.txt NOTICE


%changelog
* Sat May 25 2013 Mario Ceresa <mrceresa@gmail.com> - 2.4.0-1
- Initial package
