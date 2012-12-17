%define _short_name igtl
%define _ver_major      1
%define _ver_minor      9
%define _ver_release    7

Name:		lib%{_short_name}
Version:	%{_ver_major}.%{_ver_minor}.%{_ver_release}
Release:	1%{?dist}
Summary:	Free, open-source network communication library for image-guided therapy

License:	BSD
URL:		https://github.com/openigtlink/OpenIGTLink/
Source0:	https://github.com/openigtlink/OpenIGTLink/tarball/development/openigtlink-OpenIGTLink-00c007f.tar.gz

BuildRequires:	cmake

%description
OpenIGTLink provides a standardized mechanism for communications among computers
and devices in operating rooms (OR) for wide variety of image-guided therapy (IGT)
applications. Examples of such applications include:

* Stereotactic surgical guidance using optical position sensor.
* Intraoperative image guidance using real-time MRI.
* Robot-assisted intervention using robotic device and surgical planning software 

OpenIGTLink is a set of digital messaging formats and rules (protocol) used for data 
exchange on a local area network (LAN). The specification of OpenIGTLink and its 
reference implementation, the OpenIGTLink Library, are available free of charge 
for any purpose including commercial use. 

An OpenIGTLink interface is available in popular medical image processing and 
visualization software 3D Slicer.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n openigtlink-OpenIGTLink-00c007f


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake .. \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DBUILD_EXAMPLES:BOOL=ON \
    -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"\
    -DCMAKE_VERBOSE_MAKEFILE=ON\
    -DOpenIGTLink_INSTALL_LIB_DIR=%{_lib}/%{_short_name} \
    -DOpenIGTLink_INSTALL_PACKAGE_DIR=%{_lib}/%{_short_name}/cmake \
    -DBUILD_TESTING=ON \
    -DBUILD_DOCUMENTATION=ON

popd

make %{?_smp_mflags} -C %{_target_platform}

%install
rm -rf $RPM_BUILD_ROOT
%make_install -C %{_target_platform}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Install ldd config file
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo %{_libdir}/%{_short_name} > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_libdir}/igtl/*
#In order to recognize /usr/lib64/igtl we need to ship a proper file for /etc/ld.so.conf.d/
%config %{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{_libdir}/igtl/*.so.*

%files devel
%{_includedir}/igtl/*
%{_libdir}/igtl/*.so


%changelog
* Mon Dec 17 2012 Mario Ceresa mrceresa fedoraproject org libOpenIGTLink 1.9.7-1%{?dist}
- Initial import


