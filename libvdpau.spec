Summary:	Wrapper library for the Video Decode and Presentation API
Summary(pl.UTF-8):	Biblioteka pośrednia do API dekodowania i prezentacji video (Video Decode and Presentation API)
Name:		libvdpau
Version:	0.3
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://people.freedesktop.org/~aplattner/vdpau/%{name}-%{version}.tar.gz
# Source0-md5:	2ae5b15d6ede1c96f0fa0aefcc573297
URL:		http://freedesktop.org/wiki/Software/VDPAU
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
# libvdpau isn't arch-specific, but currently only nvidia driver is available
# (xorg-driver-video-nvidia.spec)
Conflicts:	xorg-driver-video-nvidia-libs < 1:190.42-2
ExclusiveArch:	%{ix86} %{x8664}
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

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_trace.{la,a}

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
%attr(755,root,root) %ghost %{_libdir}/vdpau/libvdpau_trace.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvdpau.so
%{_libdir}/libvdpau.la
%{_includedir}/vdpau
%{_pkgconfigdir}/vdpau.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvdpau.a
