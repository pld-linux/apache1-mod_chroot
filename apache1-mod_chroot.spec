%define		mod_name	chroot
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: makes running Apache in a secure chroot environment easy
Summary(pl):	Modu³ Apache'a do uruchamiania serwera w bezpiecznym ¶rodowisku chroot
Name:		apache1-mod_%{mod_name}
Version:	0.4
Release:	0.2
License:	GPL
Group:		Networking/Daemons
Source0:	http://core.segfault.pl/~hobbit/mod_chroot/dist/mod_chroot-%{version}.tar.gz
# Source0-md5:	abd2c8209b61b2a2fecdf10a61051060
URL:		http://core.segfault.pl/~hobbit/mod_chroot/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
Requires:	apache1 >= 1.3.33-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_chroot makes running Apache in a secure chroot environment easy.
You don't need to create a special directory hierarchy containing
/dev, /lib, /etc...

%description -l pl
mod_chroot u³atwia uruchamianie Apache'a w bezpiecznym ¶rodowisku
chroot. Nie trzeba tworzyæ specjalnej hierarchii katalogów /dev, /lib,
/etc, itp.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}
install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc CAVEATS ChangeLog INSTALL README
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
