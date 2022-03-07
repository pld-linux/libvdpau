#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Wrapper library for the Video Decode and Presentation API
Summary(pl.UTF-8):	Biblioteka pośrednia do API dekodowania i prezentacji video (Video Decode and Presentation API)
Name:		libvdpau
Version:	1.5
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://gitlab.freedesktop.org/vdpau/libvdpau/tags
Source0:	https://gitlab.freedesktop.org/vdpau/libvdpau/-/archive/%{version}/libvdpau-%{version}.tar.bz2
# Source0-md5:	148a192110e7a49d62c0bf9ef916c099
URL:		https://freedesktop.org/wiki/Software/VDPAU
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	texlive-dvips
BuildRequires:	texlive-latex
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	meson >= 0.41
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.736
%{?with_apidocs:BuildRequires:	texlive-pdftex}
BuildRequires:	xorg-lib-libX11-devel >= 1.5
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-proto-dri2proto-devel >= 2.2
Requires:	xorg-lib-libX11 >= 1.5
# withdrawn (and never useful) Mesa drivers
Obsoletes:	libvdpau-driver-mesa-r300 < 10
Obsoletes:	libvdpau-driver-mesa-softpipe < 10
Conflicts:	xorg-driver-video-nvidia-libs < 1:190.42-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VDPAU is the Video Decode and Presentation API for UNIX. It provides
an interface to video decode acceleration and presentation hardware
present in modern GPUs.

%description -l pl.UTF-8
VDPAU to skrót od Video Decode and Presentation API for UNIX.
Biblioteka ta dostarcza interfejs do akceleracji dekodowania oraz
prezentacji video obecnej we współczesnych procesorach graficznych.

%package devel
Summary:	Header files for vdpau library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki vdpau
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	xorg-lib-libX11-devel
Obsoletes:	libvdpau-static

%description devel
Header files for vdpau library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki vdpau.

%package apidocs
Summary:	vdpau API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki vdpau
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for vdpau library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki vdpau.

%prep
%setup -q

%build
%meson build \
	-Ddocumentation=%{__true_false apidocs}
%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%{__rm} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_trace.so

%if %{with apidocs}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/{%{name}/html,%{name}-apidocs}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING
%attr(755,root,root) %{_libdir}/libvdpau.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvdpau.so.1
%dir %{_libdir}/vdpau
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_trace.so.*.*.*
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_trace.so.1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vdpau_wrapper.cfg

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvdpau.so
%{_includedir}/vdpau
%{_pkgconfigdir}/vdpau.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/%{name}-apidocs
%endif
