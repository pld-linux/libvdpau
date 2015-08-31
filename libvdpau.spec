#
# Conditional build:
%if "%{pld_release}" == "ac"
%bcond_with		apidocs		# build and package API docs
%else
%bcond_without	apidocs		# do not build and package API docs
%endif

Summary:	Wrapper library for the Video Decode and Presentation API
Summary(pl.UTF-8):	Biblioteka pośrednia do API dekodowania i prezentacji video (Video Decode and Presentation API)
Name:		libvdpau
Version:	1.1.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://people.freedesktop.org/~aplattner/vdpau/%{name}-%{version}.tar.bz2
# Source0-md5:	2fa0b05a4f4d06791eec83bc9c854d14
Patch0:		link-X11.patch
URL:		http://freedesktop.org/wiki/Software/VDPAU
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpm >= 4.4.9-56
%if "%{pld_release}" == "ac"
BuildRequires:	XFree86-devel
%else
%{?with_apidocs:BuildRequires:	texlive-pdftex}
BuildRequires:	xorg-lib-libX11-devel >= 1.5
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-proto-dri2proto-devel >= 2.2
%endif
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
%if "%{pld_release}" == "ac"
Requires:	XFree86-devel
%else
Requires:	xorg-lib-libX11-devel
%endif
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for vdpau library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki vdpau.

%package static
Summary:	Static vdpau library
Summary(pl.UTF-8):	Statyczna biblioteka vdpau
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static vdpau library.

%description static -l pl.UTF-8
Statyczna biblioteka vdpau.

%package apidocs
Summary:	vdpau API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki vdpau
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API and internal documentation for vdpau library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki vdpau.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%if "%{pld_release}" == "ac"
X11_CFLAGS=" " X11_LIBS="-L%{_prefix}/X11R6/%{_lib} -lX11" \
%endif
%configure \
	--enable-documentation%{!?with_apidocs:=no} \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_trace.{la,a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_trace.so

%if %{with apidocs}
mv $RPM_BUILD_ROOT%{_docdir}/{%{name}/html,%{name}-apidocs}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog
%attr(755,root,root) %{_libdir}/libvdpau.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvdpau.so.1
%dir %{_libdir}/vdpau
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_trace.so.*.*.*
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_trace.so.1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vdpau_wrapper.cfg

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvdpau.so
%{_libdir}/libvdpau.la
%{_includedir}/vdpau
%{_pkgconfigdir}/vdpau.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvdpau.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/%{name}-apidocs
%endif
