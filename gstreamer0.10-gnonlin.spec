#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc

%define		gst_major_ver	0.10
%define		gst_req_ver	0.10.30
%define		gstpb_req_ver	0.10.30
Summary:	GStreamer extension library for non-linear editing
Summary(pl.UTF-8):	Biblioteka rozszerzenia GStreamera do edycji nieliniowej
Name:		gstreamer0.10-gnonlin
Version:	0.10.17
Release:	2
License:	LGPL v2+
Group:		Applications/Multimedia
Source0:	http://gstreamer.freedesktop.org/src/gnonlin/gnonlin-%{version}.tar.bz2
# Source0-md5:	0c9e5a8f771b087fac9afa459399112e
Patch0:		gstreamer-common-gtkdoc.patch
URL:		http://gnonlin.sourceforge.net/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.10
BuildRequires:	docbook-dtd412-xml
BuildRequires:	glib2-devel >= 1:2.22
BuildRequires:	gstreamer0.10-devel >= %{gst_req_ver}
BuildRequires:	gstreamer0.10-plugins-base-devel >= %{gstpb_req_ver}
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.8}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python >= 2.1
BuildRequires:	rpm-build >= 4.6
Requires:	glib2 >= 1:2.22
Requires:	gstreamer0.10 >= %{gst_req_ver}
Requires:	gstreamer0.10-plugins-base >= %{gstpb_req_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gnonlin is a plugin for GStreamer which provides support for writing
non-linear audio and video editing applications. It introduces the
concept of a timeline.

%description -l pl.UTF-8
Gnonlin to wtyczka dla GStreamera pozwalająca na pisanie aplikacji do
nieliniowej edycji dźwięku i obrazu. Wprowadza pojęcia "linii czasu".

%package apidocs
Summary:	Gnonlin API documentation
Summary(pl.UTF-8):	Dokumentacja API Gnonlin
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
Gnonlin API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Gnonlin.

%prep
%setup -q -n gnonlin-%{version}
cd common
%patch -P0 -p1

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4 -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--enable-gtk-doc%{!?with_apidocs:=no} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_major_ver}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README RELEASE
%attr(755,root,root) %{_libdir}/gstreamer-%{gst_major_ver}/libgnl.so

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnonlin-0.10
%endif
