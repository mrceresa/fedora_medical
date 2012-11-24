
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Summary:        Insight Toolkit library for medical image processing
Name:           InsightToolkit
Version:        3.20.1
Release:        1%{?dist}
License:        BSD
Group:          Applications/Engineering
Vendor:         Insight Software Consortium
Source0:        https://github.com/mrceresa/ITK/zipball/v3.20.1_fc15.zip
Source1:        http://downloads.sourceforge.net/project/itk/itk/2.4/ItkSoftwareGuide-2.4.0.pdf
URL:            http://www.itk.org/

# Thanks to Mathieu Malaterre for pointing out the following patch
# The patch was retrieved from http://itk.org/gitweb?p=ITK.git;a=patch;h=93833edb2294c0190af9e6c0de26e9485399a7d3
#Patch1:		0001-Fix-vtkmetaio.patch
#Patch2:         0002-Fix-install-dir.patch
#Patch3:         0003-Remove-applications-because-this-is-now-a-separate-I.patch
#Patch4:         0004-Fix-cstddef-inclusion-for-gcc-4.6.patch
#Patch5:         0005-Provide-a-target-for-vtkmetaio.patch

BuildRequires:  cmake >= 2.6.0
BuildRequires:  libxml2-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  zlib-devel
BuildRequires:  fftw3-devel
BuildRequires:  libjpeg-devel
BuildRequires:  gdcm-devel
BuildRequires:  vxl-devel
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

%prep
%setup -q -n mrceresa-ITK-69c640a

#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1

#Remove bundled library (let's use FEDORA's ones)

#for l in itkzlib zlib itkpng itktiff gdcm
# Leave itkpng because new libpng changed apis
for l in itkzlib zlib itktiff gdcm
do
	find Utilities/$l -type f ! -name 'CMakeLists.txt' -execdir rm {} +
done

# remove CVS dirs, if they exist
find -name CVS -type d | xargs rm -rf

# copy guide into the appropriate directory
cp %{SOURCE1} .

# remove applications: they are shipped separately now
rm -rf Applications/

# remove utilities that are under review request in Fedora:
#rm -rf Utilities/netlib
#rm -rf Utilities/openjpeg

# remove utilities that still needs to be packaged in Fedora
#rm -rf Utilities/NrrdIO
#rm -rf Utilities/DICOMParser
#rm -rf Utilities/itkjpeg

### end of removing

%build
%cmake -DBUILD_SHARED_LIBS:BOOL=ON \
       -DBUILD_EXAMPLES:BOOL=ON \
       -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"\
       -DCMAKE_VERBOSE_MAKEFILE=ON\
       -DBUILD_TESTING=OFF\
       -DITK_USE_ORIENTED_IMAGE_DIRECTION:BOOL=ON \
       -DITK_IMAGE_BEHAVES_AS_ORIENTED_IMAGE:BOOL=ON \
       -DITK_USE_CENTERED_PIXEL_COORDINATES_CONSISTENTLY=ON \
       -DITK_USE_REVIEW:BOOL=ON \
       -DITK_USE_REVIEW_STATISTICS=ON \
       -DITK_USE_PATENTED:BOOL=OFF \
       -DITK_USE_SYSTEM_TIFF=ON \
       -DITK_USE_SYSTEM_PNG=OFF \
       -DITK_USE_SYSTEM_ZLIB=ON \
       -DITK_USE_SYSTEM_LIBXML2=ON \
       -DITK_USE_SYSTEM_GDCM=ON \
       -DITK_USE_SYSTEM_VXL=ON \
       -DITK_USE_SYSTEM_EXPAT=ON \
       -DCMAKE_CXX_FLAGS:STRING="-fpermissive" .

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Install examples
mkdir -p %{buildroot}%{_datadir}/%{name}/examples
cp -r Examples/* %{buildroot}%{_datadir}/%{name}/examples/

# remove copyrighted material
rm -rf %{buildroot}%{_datadir}/%{name}/examples/Patented

#mv $RPM_BUILD_ROOT%{_libdir}/%{name}/*.cmake $RPM_BUILD_ROOT%{_datadir}/%{name}/

# Install ldd config file
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo %{_libdir}/%{name} > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}
%dir %{_datadir}/%{name}
#In order to recognize /usr/lib64/InsightToolkit we need to ship a proper file for /etc/ld.so.conf.d/
%config %{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{_bindir}/itkTestDriver
%{_bindir}/DicomSeriesReadImageWrite2
%{_libdir}/%{name}/*.so.*

%doc Copyright/*


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%package        devel
Summary:        Insight Toolkit
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel

Insight Toolkit Library Header Files and Link Libraries

%files devel
%defattr(-,root,root)
%doc README.html
%doc ItkSoftwareGuide-2.4.0.pdf
%{_libdir}/%{name}/*.so
%{_includedir}/%{name}/
%{_libdir}/%{name}/*.cmake

%package        examples
Summary:        C++, Tcl and Python example programs/scripts for ITK
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}

%description examples
ITK examples

%files          examples
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}/examples
%{_datadir}/%{name}/examples/*



%package        doc
Summary:        Documentation for ITK
Group:          Documentation

%description    doc
ITK doc

%files          doc
%defattr(-,root,root,-)
#%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/*


%changelog
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


