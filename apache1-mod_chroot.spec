%define		mod_name	chroot
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: makes running Apache in a secure chroot environment easy.
Name:		apache1-mod_%{mod_name}
Version:	0.2
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://core.segfault.pl/~hobbit/mod_chroot/dist/mod_chroot-%{version}.tar.gz
# Source0-md5:	85211cd8cafcfe64258e02291ea6439e
URL:		http://core.segfault.pl/~hobbit/mod_chroot/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.31
Requires(post,preun):	%{apxs}
Requires:	apache1 >= 1.3.31
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
mod_chroot makes running Apache in a secure chroot environment easy.
You don't need to create a special directory hierarchy containing
/dev, /lib, /etc...

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT

install -D mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL
%attr(755,root,root) %{_pkglibdir}/*.so
