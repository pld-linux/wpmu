# TODO
# - gettext mo to system dir, add all possible languages?
Summary:	WordPress MU
Name:		wordpress-mu
Version:	2.8.5.2
Release:	1.6
License:	GPL
Group:		Applications/Publishing
#Source0:	http://mu.wordpress.org/latest.tar.gz
Source0:	http://mu.wordpress.org/%{name}-%{version}.tar.gz
# Source0-md5:	7d733e276cb5983f58a39365bc97b81e
URL:		http://mu.wordpress.org/
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

%package setup
Summary:	Wordpress MU setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji Wordpress
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial WordPress MU installation.
You should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfiguracji WordPress
MU po pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%prep
%setup -q -n %{name}

rm wp-content/themes/index.php
rm wp-content/mu-plugins/index.php
rm wp-content/mu-plugins/readme.txt
rm wp-content/plugins/index.php
rm wp-content/plugins/readme.txt

find '(' -name '*.php' -o -name '*.js' -o -name '*.html' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_sysconfdir},%{_appdir}/wp-content/languages}

cp -a . $RPM_BUILD_ROOT%{_appdir}
cp -a wp-config-sample.php $RPM_BUILD_ROOT%{_sysconfdir}/wp-config.php
rm $RPM_BUILD_ROOT%{_appdir}/htaccess.dist

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	%banner -e %{name} <<-EOF
	To finish your configuration DO NOT FORGET to:

	1) Create some MySQL database owned by some user
	2) Edit the file: %{_sysconfdir}/wp-config.php
	3) Install %{name}-setup
	4) Run a browser and visit: http://`hostname`/wordpress/wp-admin/install.php
EOF
fi

%post setup
chmod 660 %{_sysconfdir}/wp-config.php
chown root:http %{_sysconfdir}/wp-config.php

%postun setup
if [ "$1" = "0" ]; then
	chmod 640 %{_sysconfdir}/wp-config.php
	chown root:http %{_sysconfdir}/wp-config.php
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
%dir %attr(750,root,http) %{_sysconfdir}
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/wp-config.php

%{_appdir}/README.txt
%{_appdir}/license.txt
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

%files setup
%defattr(644,root,root,755)
#%attr(755,root,root) %{_bindir}/wp-secure
#%attr(755,root,root) %{_bindir}/wp-setup
#%{_appdir}/wp-secure.sh
#%{_appdir}/wp-setup.sh
%{_appdir}/wp-admin
