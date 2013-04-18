%define _ver_major      4
%define _ver_minor      3
%define _ver_release    1

Name:           InsightToolkit
Summary:        Insight Toolkit library for medical image processing
Version:        %{_ver_major}.%{_ver_minor}.%{_ver_release}
Release:        6%{?dist}
License:        BSD
Group:          Applications/Engineering
Source0:        http://sourceforge.net/projects/itk/files/itk/%{_ver_major}.%{_ver_minor}/%{name}-%{version}.tar.gz
Source1:        http://downloads.sourceforge.net/project/itk/itk/2.4/ItkSoftwareGuide-2.4.0.pdf
URL:            http://www.itk.org/
Patch0:         %{name}-0001-Set-lib-lib64-according-to-the-architecture.patch
#Patch1:         %{name}-0002-Fixed-vnl_math-namespace-usage-for-compatibility-wit.patch
#Patch2:         %{name}-0003-ENH-Fix-vxl-vnl-namespace.patch
Patch3:         %{name}-0004-Fix_System_TIFF_Build.patch

# Thanks to Mathieu Malaterre for pointing out the following patch
# The patch was retrieved from http://itk.org/gitweb?p=ITK.git;a=patch;h=93833edb2294c0190af9e6c0de26e9485399a7d3
#Patch1:         0001-Fix-vtkmetaio.patch
#Patch2:         0002-Fix-install-dir.patch
#Patch3:         0003-Remove-applications-because-this-is-now-a-separate-I.patch
#Patch4:         0004-Fix-cstddef-inclusion-for-gcc-4.6.patch
#Patch5:         0005-Provide-a-target-for-vtkmetaio.patch

BuildRequires:  cmake
BuildRequires:  fftw-devel
BuildRequires:  gdcm-devel
BuildRequires:  hdf5-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libxml2-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-devel
BuildRequires:  vxl-devel
BuildRequires:  zlib-devel
#For documentation
BuildRequires:  graphviz
BuildRequires:  doxygen

%description

ITK is an open-source software toolkit for performing registration and 
segmentation. Segmentation is the process of identifying and classifying data
found in a digitally sampled representation. Typically the sampled
representation is an image acquired from such medical instrumentation as CT or
MRI scanners. Registration is the task of aligning or developing 
correspondences between data. For example, in the medical environment, a CT
scan may be aligned with a MRI scan in order to combine the information
contained in both.

ITK is implemented in C++ and its implementation style is referred to as 
generic programming (i.e.,using templated code). Such C++ templating means
that the code is highly efficient, and that many software problems are 
discovered at compile-time, rather than at run-time during program execution.

%package        devel
Summary:        Insight Toolkit
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel

%(summary).
Install this if you want to develop applications that use ITK.

%package        examples
Summary:        C++, Tcl and Python example programs/scripts for ITK
Group:          Development/Languages
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description examples
ITK examples

%package        doc
Summary:        Documentation for ITK
Group:          Documentation
BuildArch:      noarch

%description    doc
%{summary}.
This package contains additional documentation.



%prep
%setup -q

%patch0 -p1
#%patch1 -p1
#%patch2 -p1
%patch3 -p0

# copy guide into the appropriate directory
cp -a %{SOURCE1} .

# remove applications: they are shipped separately now
rm -rf Applications/

### end of removing

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}

%cmake .. \
       -DBUILD_SHARED_LIBS:BOOL=ON \
       -DBUILD_EXAMPLES:BOOL=OFF \
       -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"\
       -DCMAKE_VERBOSE_MAKEFILE=ON\
       -DBUILD_TESTING=ON\
       -DITKV3_COMPATIBILITY:BOOL=OFF \
       -DITK_BUILD_ALL_MODULES:BOOL=ON \
       -DITK_WRAP_PYTHON:BOOL=OFF \
       -DITK_WRAP_JAVA:BOOL=OFF \
       -DBUILD_DOCUMENTATION:BOOL=OFF \
       -DITK_USE_REVIEW:BOOL=ON \
       -DITK_USE_PATENTED:BOOL=OFF \
       -DITK_USE_SYSTEM_HDF5=ON \
       -DITK_USE_SYSTEM_JPEG=ON \
       -DITK_USE_SYSTEM_TIFF=ON \
       -DITK_USE_SYSTEM_PNG=ON \
       -DITK_USE_SYSTEM_ZLIB=ON \
       -DITK_USE_SYSTEM_GDCM=ON \
       -DITK_USE_SYSTEM_VXL=ON \
       -DITK_INSTALL_LIBRARY_DIR=%{_lib}/%{name} \
       -DITK_INSTALL_INCLUDE_DIR=include/%{name} \
       -DITK_INSTALL_PACKAGE_DIR=%{_lib}/%{name}/cmake \
       -DITK_INSTALL_RUNTIME_DIR:PATH=%{_bindir} \
       -DCMAKE_CXX_FLAGS:STRING="-fpermissive"

popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

# Install examples
mkdir -p %{buildroot}%{_datadir}/%{name}/examples
cp -ar Examples/* %{buildroot}%{_datadir}/%{name}/examples/

# Install ldd config file
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo %{_libdir}/%{name} > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

%check
make test -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%dir %{_datadir}/%{name}
%dir %{_libdir}/%{name}
#In order to recognize /usr/lib64/InsightToolkit we need to ship a proper file for /etc/ld.so.conf.d/
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{_bindir}/itkTestDriver
%{_libdir}/%{name}/*.so.*
%doc LICENSE README.txt NOTICE


%files devel
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/cmake/
%{_includedir}/%{name}/


%files examples
%{_datadir}/%{name}/examples


%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}/
%{_docdir}/ITK-%{_ver_major}.%{_ver_minor}/
%doc ItkSoftwareGuide-2.4.0.pdf


%changelog
* Thu Apr 18 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-6
- Removed unused patches

* Mon Apr 08 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-5
- Fixed failing tests

* Wed Apr 03 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-4
- Fixed build with USE_SYSTEM_TIFF

* Fri Mar 29 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-3
- Compiles against VXL with compatibility patches
- Enabled testing

* Tue Feb 12 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-2
- Reorganized sections
- Fixed patch naming
- Removed buildroot and rm in install section
- Removed cmake version constraint
- Changed BR libjpeg-turbo-devel to libjpeg-devel
- Preserve timestamp of SOURCE1 file.
- Fixed main file section
- Added noreplace

* Fri Jan 25 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-1
- Updated to 4.3.1
- Fixed conflicts with previous patches
- Dropped gcc from BR
- Fixed tabs-vs-space
- Improved description
- Re-enabled system tiff
- Clean up the spec
- Sanitize use of dir macro
- Re-organized docs
- Fixed libdir and datadir ownership

* Wed Dec 12 2012 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.2.1-4
- Included improvements to the spec file from Dan Vratil

* Tue Dec 4 2012 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.2.1-3
- Build against system VXL

* Mon Nov 26 2012 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.2.1-2
- Reorganized install paths

* Tue Nov 20 2012 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.2.1-1
- Updated to new version

* Wed Nov 30 2011 Mario Ceresa mrceresa fedoraproject org InsightToolkit 3.20.1-1
- Updated to new version
- Added binary morphology code

* Fri May 27 2011 Mario Ceresa mrceresa fedoraproject org InsightToolkit 3.20.0-5
- Added cstddef patch for gcc 4.6

* Mon Jan 24 2011 Mario Ceresa mrceresa@gmail.com InsightToolkit 3.20.0-4
- Added the ld.so.conf file

* Mon Nov 22 2010 Mario Ceresa mrceresa@gmail.com InsightToolkit 3.20.0-3
- Updated to 3.20 release
- Added vxl utility and review material
- Applied patch from upstream to fix vtk detection (Thanks to Mathieu Malaterre)
- Added patch to install in the proper lib dir based on arch value
- Added patch to set datadir as cmake configuration files dir

* Sun Dec  6 2009 Mario Ceresa mrceresa@gmail.com InsightToolkit 3.16.0-2
- Fixed comments from revision: https://bugzilla.redhat.com/show_bug.cgi?id=539387#c8

* Tue Nov 17 2009 Mario Ceresa mrceresa@gmail.com InsightToolkit 3.16.0-1
- Initial RPM Release


