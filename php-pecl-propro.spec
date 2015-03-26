%define		php_name	php%{?php_suffix}
%define		modname		propro
%define		status		stable
Summary:	%{modname} - Property proxy
Name:		%{php_name}-pecl-%{modname}
Version:	1.0.0
Release:	1
License:	BSD, revised
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	9c775035fd17c65f0162b7eb1b4f8564
URL:		http://pecl.php.net/package/propro/
BuildRequires:	%{php_name}-devel >= 3:5.3.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A reusable split-off of pecl_http's property proxy API.

In PECL status of this extension is: %{status}.

%package devel
Summary:	Header files for propro PECL extension
Group:		Development/Libraries
# does not require base
Requires:	php-devel >= 4:5.2.0

%description devel
Header files for propro PECL extension.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%{__libtoolize}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

install -D php_propro.h $RPM_BUILD_ROOT%{_includedir}/php/ext/propro/php_propro.h

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so

%files devel
%defattr(644,root,root,755)
%dir %{php_includedir}/ext/propro
%{php_includedir}/ext/propro/php_propro.h
