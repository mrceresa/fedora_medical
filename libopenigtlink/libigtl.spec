%global _short_name igtl
%global _ver_major      1
%global _ver_minor      9
%global _ver_release    7

Name:		lib%{_short_name}
Version:	%{_ver_major}.%{_ver_minor}.%{_ver_release}
Release:	5%{?dist}
Summary:	Network communication library for image-guided therapy

License:	BSD
URL:		https://github.com/openigtlink/OpenIGTLink/
Source0:	https://github.com/openigtlink/OpenIGTLink/tarball/development/openigtlink-OpenIGTLink-00c007f.tar.gz

# Generate documentation: sent upstream https://github.com/openigtlink/OpenIGTLink/pull/6
Patch0:		%{name}-0001-Add-generation-of-doxygen-documentation.patch
Patch1:		%{name}-0002-Add-doxygen-and-papers-dir.patch
Patch2:		%{name}-0003-Use-original-doxyfile.patch

BuildRequires:	cmake
# For documentation:
BuildRequires:	tex(latex)
BuildRequires:	gnuplot
BuildRequires:	graphviz
BuildRequires:	doxygen
# Including fonts for fedora 18 and later
%if 0%{?fedora} >= 18
BuildRequires: tex-helvetic
BuildRequires: tex-symbol
BuildRequires: tex-times
%endif


%description
OpenIGTLink provides a standardized mechanism for communications among computers
and devices in operating rooms (OR) for wide variety of image-guided therapy 
(IGT) applications. Examples of such applications include:

* Stereotactic surgical guidance using optical position sensor.
* Intraoperative image guidance using real-time MRI.
* Robot-assisted intervention with robotic device + surgical planning software

OpenIGTLink is a set of digital messaging formats and rules (protocol) used 
for data exchange on a local area network (LAN). The specification of 
OpenIGTLink and its reference implementation, the OpenIGTLink Library, are 
available free of charge for any purpose including commercial use. 

An OpenIGTLink interface is available in popular medical image processing and 
visualization software 3D Slicer.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    doc
The %{name}-doc package contains documentation for %{name}

%prep
%setup -q -n openigtlink-OpenIGTLink-4caf9cf
%patch0 -p1
%patch1 -p1
%patch2 -p1

# Thanks to Jarry James for suggesting this handy fix to the documentation
sed s/dvips/pdftex/ Documents/Papers/InsightJournal2008/OpenIGTLinkIJ2008.tex

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake .. \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DBUILD_EXAMPLES:BOOL=ON \
    -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"\
    -DCMAKE_VERBOSE_MAKEFILE=ON\
    -DOpenIGTLink_INSTALL_LIB_DIR=%{_lib} \
    -DOpenIGTLink_INSTALL_PACKAGE_DIR=%{_datadir}/%{_short_name}/cmake \
    -DBUILD_TESTING=ON \
    -DBUILD_DOCUMENTATION=ON \
    -DPDFLATEX_COMPILER=%{_bindir}/pdflatex

popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Install documentation
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}

pushd %{_target_platform}
cp Documents/Papers/InsightJournal2008/OpenIGTLinkIJ2008.pdf %{buildroot}%{_docdir}/%{name}-%{version}/
cp -r Documents/Doxygen/html %{buildroot}%{_docdir}/%{name}-%{version}/
popd

%check
make test -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc LICENSE.txt README
%{_libdir}/*.so.*

%files devel
%dir %{_includedir}/%{_short_name}/
%dir %{_datadir}/%{_short_name}/
%{_includedir}/%{_short_name}/*
%{_libdir}/*.so
%{_datadir}/%{_short_name}/cmake/

%files          doc
#%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/OpenIGTLinkIJ2008.pdf
%{_docdir}/%{name}-%{version}/html/



%changelog
* Wed Dec 19 2012 Mario Ceresa <mrceresa at fedoraproject.org> 1.9.7-5%{?dist}
- Fixed compilation of documentation under f18+
- Fixed double inclusion of doc files
- Shortened summary
- Install libraries into _libdir and remove ldconfig file 
- Move cmake files to _datadir
- Commented patches


* Tue Dec 18 2012 Mario Ceresa <mrceresa at fedoraproject.org> 1.9.7-4%{?dist}
- Added documentation

* Mon Dec 17 2012 Mario Ceresa <mrceresa at fedoraproject.org> 1.9.7-3%{?dist}
- Added license and README file

* Mon Dec 17 2012 Mario Ceresa <mrceresa at fedoraproject.org> 1.9.7-2%{?dist}
- Fixing fedora-review detected errors:
-- Duplicate listing in libdir
-- Macro consistency improved
-- Using config noreplace
-- Use global instead of define
- Fixed dir ownership

* Mon Dec 17 2012 Mario Ceresa <mrceresa at fedoraproject.org> 1.9.7-1%{?dist}
- Initial import


