# TODO
# - gettext mo to system dir, add all possible languages?
# - system jquery, scriptaculos, prototype, swfobject 2.1
# - no system codepress 0.9.6: codepress.js is modified
# - no system tinymce 3.2.7: themes and "inlinepopups", "media", "paste" plugins are modified
%define		php_min_version 5.2.1
Summary:	WordPress MU
Summary(en.UTF-8):	WordPress µ
Name:		wpmu
Version:	2.9.2
Release:	3
License:	GPL v2
Group:		Applications/Publishing
Source0:	http://mu.wordpress.org/wordpress-mu-%{version}.tar.gz
# Source0-md5:	3dff1dd886414ef80ffddba7a33172bf
URL:		http://mu.wordpress.org/
Source1:	apache.conf
Source2:	lighttpd.conf
Source3:	http://www.bisente.com/%{name}.lua
# Source3-md5:	97df526f5261f57a3bbaaadac0bd112a
Patch0:		pld.patch
Patch1:		wp_queries.patch
Patch2:		configpath.patch
Patch3:		simplepie.patch
Patch4:		rss_post_author.patch
Patch5:		pear-text-diff.patch
Patch6:		atomlib.patch
BuildRequires:	/usr/bin/php
BuildRequires:	rpm-php-pearprov
Requires:	js-swfobject >= 2.1
Requires:	php-atomlib >= 0.4
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-gettext
Requires:	php-mysql
Requires:	php-pcre
Requires:	php-pear-Text_Diff
Requires:	php-simplepie >= 1.2
Requires:	php-xml
Requires:	webapps
Requires:	webserver(php)
Obsoletes:	wordpress-mu
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# no pear deps
%define		_noautopear	pear

# exclude optional php dependencies
%define		_noautophp	php-date php-ftp php-dom php-gd php-hash php-iconv php-json php-libxml php-mbstring php-openssl php-simplexml php-spl php-tokenizer php-xmlreader

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

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
Obsoletes:	wordpress-mu-setup

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

%package theme-default
Summary:	Wordpress MU default theme
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description theme-default
WordPress Default by Michael Heilemann

The default WordPress theme based on the famous Kubrick.

%package theme-classic
Summary:	Wordpress MU classic theme
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description theme-classic
WordPress Classic by Dave Shea

The original WordPress theme that graced versions 1.2.x and prior.

%package theme-home
Summary:	Wordpress MU home theme
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description theme-home
WordPress mu Homepage by Michael Heilemann

WordPress mu homepage theme based on the famous Kubrick.

%prep
%setup -qc
mv wordpress-mu/* .; rmdir wordpress-mu
# undos
find '(' -name '*.php' -o -name '*.js' -o -name '*.html' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'

%patch -P0 -p1

rm wp-content/themes/index.php
rm wp-content/mu-plugins/index.php
rm wp-content/mu-plugins/readme.txt
rm wp-content/plugins/index.php
rm wp-content/plugins/readme.txt
rm wp-content/index.php

# remove *.dev js/.css
find -name *.dev.js | xargs rm -v
find -name *.dev.css | xargs rm -v

# system swfobject
rm wp-includes/js/swfobject.js

# system simplepie
rm wp-includes/class-simplepie.php

# system php-pear-Text_Diff
rm -rf wp-includes/Text/Diff*
rmdir wp-includes/Text

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

# Extract $wp_queries to separate file so these could be re-loaded when blog changes
sed -ne '/global $wp_queries;/,/WP_FIRST_INSTALL$/p' wp-admin/includes/schema.php > wp-admin/includes/schema-wp_queries.php
sed -i -e '/global $wp_queries;/,/WP_FIRST_INSTALL$/d' wp-admin/includes/schema.php
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
php -l wp-admin/includes/schema.php
php -l wp-admin/includes/schema-wp_queries.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sbindir},%{_sysconfdir},%{_appdir}/wp-content/languages,/var/{lib,log}/wpmu}

cp -a . $RPM_BUILD_ROOT%{_appdir}
touch $RPM_BUILD_ROOT%{_sysconfdir}/wp-config.php
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}
cp -a $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf
rm $RPM_BUILD_ROOT%{_appdir}/{README.txt,license.txt,htaccess.dist}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	%banner -e %{name} <<-EOF
	To setup configuration using web wizard:

	- Install %{name}-setup
	- Create empty MySQL database (mysqladmin create wpmu)
	- Open web browser at: http://$(hostname)/wpmu/index.php
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
%doc README.txt license.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/wp-config.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/wpmu.lua

%{_appdir}/wp-content/blogs.php

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/wp-includes
%dir %{_appdir}/wp-content
%dir %{_appdir}/wp-content/languages
%dir %{_appdir}/wp-content/plugins
%dir %{_appdir}/wp-content/mu-plugins

%dir %{_appdir}/wp-content/themes

# needed for daily moderation
%{_appdir}/wp-admin

%attr(775,root,http) /var/lib/wpmu
%attr(775,root,http) /var/log/wpmu

# -setup package
%exclude %{_appdir}/index-install.php
%exclude %{_appdir}/wp-config-sample.php

%files setup
%defattr(644,root,root,755)
%{_appdir}/index-install.php
%{_appdir}/wp-config-sample.php

%files theme-default
%defattr(644,root,root,755)
%{_appdir}/wp-content/themes/default

%files theme-classic
%defattr(644,root,root,755)
%{_appdir}/wp-content/themes/classic

%files theme-home
%defattr(644,root,root,755)
%{_appdir}/wp-content/themes/home
