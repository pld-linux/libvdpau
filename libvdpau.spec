Summary:	Wrapper library for the Video Decode and Presentation API
Summary(pl.UTF-8):	Biblioteka pośrednia do API dekodowania i prezentacji video (Video Decode and Presentation API)
Name:		libvdpau
Version:	0.2
Release:	0.1
License:	MIT
Group:		Libraries
Source0:	http://people.freedesktop.org/~aplattner/vdpau/%{name}-%{version}.tar.gz
# Source0-md5:	e0641a208839eb88fe7c01ee5af83735
URL:		http://freedesktop.org/wiki/Software/VDPAU
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
# same as in xorg-driver-video-nvidia.spec
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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/vdpau
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
