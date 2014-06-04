%global pymajor 2
%global pyminor 7
%global pyver %{pymajor}.%{pyminor}
%global iusver %{pymajor}%{pyminor}
%global __python2 %{_bindir}/python%{pyver}
%global python2_sitelib  %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global __os_install_post %{__python27_os_install_post}
%global backport_name ssl_match_hostname
%global srcname backports.%{backport_name}

Name:           python%{iusver}-backports-%{backport_name}
Version:        3.4.0.2
Release:        2.ius%{?dist}
Summary:        The ssl.match_hostname() function from Python 3
Group:          Development/Languages
Vendor:         IUS Community Project
License:        Python
URL:            https://bitbucket.org/brandon/backports.ssl_match_hostname
Source0:        http://pypi.python.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python%{iusver}-devel
BuildRequires:  python%{iusver}-setuptools
Requires:       python%{iusver}-backports

%description
The Secure Sockets layer is only actually secure if you check the hostname in
the certificate returned by the server to which you are connecting, and verify
that it matches to hostname that you are trying to reach.

But the matching logic, defined in RFC2818, can be a bit tricky to implement on
your own. So the ssl package in the Standard Library of Python 3.2 now includes
a match_hostname() function for performing this check instead of requiring
every application to implement the check separately.

This backport brings match_hostname() to users of earlier versions of Python.
The actual code inside comes verbatim from Python 3.2.


%prep
%setup -qn %{srcname}-%{version}
mv src/backports/ssl_match_hostname/README.txt ./
mv src/backports/ssl_match_hostname/LICENSE.txt ./


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build


%install
%{__python2} setup.py install --optimize 1 --skip-build --root %{buildroot}
rm %{buildroot}%{python2_sitelib}/backports/__init__.py*

 
%files
%defattr(-,root,root,-)
%doc README.txt LICENSE.txt
%{python2_sitelib}/*


%changelog
* Wed Jun 04 2014 Carl George <carl.george@rackspace.com> - 3.4.0.2-2.ius
- Override __os_install_post to fix .pyc/pyo magic

* Wed May 07 2014 Carl George <carl.george@rackspace.com> - 3.4.0.2-1.ius
- Initial port from Fedora to IUS
- Define and use python2_sitelib and python2_sitearch
- Switch to using globals

* Sun Oct 27 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.4.0.2-1
- Update to upstream 3.4.0.2 for a security fix
- http://bugs.python.org/issue17997

* Mon Sep 02 2013 Ian Weller <iweller@redhat.com> - 3.4.0.1-1
- Update to upstream 3.4.0.1

* Mon Aug 19 2013 Ian Weller <iweller@redhat.com> - 3.2-0.5.a3
- Use python-backports instead of providing backports/__init__.py

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-0.4.a3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2-0.3.a3
- Add patch for CVE 2013-2099 https://bugzilla.redhat.com/show_bug.cgi?id=963260

* Tue Feb 05 2013 Ian Weller <iweller@redhat.com> - 3.2-0.2.a3
- Fix Python issue 12000

* Fri Dec 07 2012 Ian Weller <iweller@redhat.com> - 3.2-0.1.a3
- Initial package build
