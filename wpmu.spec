# TODO
# - gettext mo to system dir, add all possible languages?
Summary:	WordPress MU
Summary(en.UTF-8):	WordPress µ
Name:		wordpress-mu
Version:	2.8.6
Release:	0.25
License:	GPL
Group:		Applications/Publishing
Source0:	http://mu.wordpress.org/%{name}-%{version}.tar.gz
# Source0-md5:	dfa27af33afe0c206933e509edd5835c
URL:		http://mu.wordpress.org/
Source1:	apache.conf
Patch0:		pld.patch
Source2:	lighttpd.conf
Requires:	php-gettext
Requires:	php-mysql
Requires:	php-pcre
Requires:	php-xml
Requires:	php-xmlrpc
Requires:	webapps
Requires:	webserver(php) >= 5.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
WordPress MU, or multi-user is WordPress port of having hundreds of
thousands of blogs with a single install of WordPress.

%description -l en.UTF-8
WordPress µ, or multi-user is WordPress port of having hundreds of
thousands of blogs with a single install of WordPress.

%package setup
Summary:	Wordpress MU setup package
Summary(en.UTF-8):	Wordpress µ setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji Wordpress
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial WordPress MU installation.
You should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l en.UTF-8
Install this package to configure initial WordPress µ installation.
You should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfiguracji WordPress
MU po pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%prep
%setup -qc
mv %{name}/* .; rmdir %{name}
# undos
find '(' -name '*.php' -o -name '*.js' -o -name '*.html' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'

%patch0 -p1

rm wp-content/themes/index.php
rm wp-content/mu-plugins/index.php
rm wp-content/mu-plugins/readme.txt
rm wp-content/plugins/index.php
rm wp-content/plugins/readme.txt

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sbindir},%{_sysconfdir},%{_appdir}/wp-content/{languages,blogs.dir}}

cp -a . $RPM_BUILD_ROOT%{_appdir}
cp -a $RPM_BUILD_ROOT{%{_appdir}/wp-config-sample.php,%{_sysconfdir}/wp-config.php}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -a $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf
rm $RPM_BUILD_ROOT%{_appdir}/{README.txt,license.txt}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	%banner -e %{name} <<-EOF
	To setup configuration using web wizard:

	- Install %{name}-setup
	- Create empty MySQL database (mysqladmin create wpmu)
	- Open web browser at: http://$(hostname)/wordpress/wp-admin/install.php
EOF
fi

%post setup
chmod 660 %{_sysconfdir}/wp-config.php
chown root:http %{_sysconfdir}/wp-config.php
chmod 775 %{_appdir} %{_appdir}/wp-content
chown root:http %{_appdir} %{_appdir}/wp-content

%postun setup
if [ "$1" = "0" ]; then
	chmod 640 %{_sysconfdir}/wp-config.php
	chown root:http %{_sysconfdir}/wp-config.php
	chmod 755 %{_appdir} %{_appdir}/wp-content
	chown root:root %{_appdir} %{_appdir}/wp-content
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.txt license.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/wp-config.php

%{_appdir}/wp-content/blogs.php

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/wp-includes
%{_appdir}/wp-content/index.php
%dir %{_appdir}/wp-content
%dir %{_appdir}/wp-content/languages
%dir %{_appdir}/wp-content/plugins
%dir %{_appdir}/wp-content/mu-plugins

%dir %{_appdir}/wp-content/themes
%{_appdir}/wp-content/themes/classic
%{_appdir}/wp-content/themes/default
%{_appdir}/wp-content/themes/home

%attr(775,root,http) %{_appdir}/wp-content/blogs.dir

# -setup package
%exclude %{_appdir}/index-install.php
%exclude %{_appdir}/wp-config-sample.php

%files setup
%defattr(644,root,root,755)
#%attr(755,root,root) %{_sbindir}/wpmu-secure
#%attr(755,root,root) %{_sbindir}/wpmu-setup
#%{_appdir}/wp-secure.sh
#%{_appdir}/wp-setup.sh
%{_appdir}/htaccess.dist
%{_appdir}/index-install.php
%{_appdir}/wp-config-sample.php
%{_appdir}/wp-admin
