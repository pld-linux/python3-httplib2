#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (prebuilt docs are included in the sdist)
%bcond_without	tests	# unit tests

Summary:	A comprehensive HTTP client library
Summary(pl.UTF-8):	Obszerna biblioteka klienta HTTP
Name:		python3-httplib2
Version:	0.32.0
Release:	1
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://github.com/httplib2/httplib2/releases
Source0:	https://github.com/httplib2/httplib2/archive/v%{version}/httplib2-%{version}.tar.gz
# Source0-md5:	e1957615f10320440973e5f36e5d8fed
Patch0:		python-httplib2.certfile.patch
URL:		https://github.com/httplib2/httplib2
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PySocks >= 1.7.1
BuildRequires:	python3-cryptography >= 45
BuildRequires:	python3-pyparsing >= 3.1
BuildRequires:	python3-pyparsing < 4
BuildRequires:	python3-pytest >= 6.2.5
BuildRequires:	python3-pytest-cov >= 4.1.0
BuildRequires:	python3-pytest-forked >= 1.6.0
BuildRequires:	python3-pytest-randomly >= 3.12.0
BuildRequires:	python3-pytest-timeout >= 1.4.2
BuildRequires:	python3-pytest-xdist >= 3.5.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	ca-certificates
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A comprehensive HTTP client library, httplib2.py supports many
features left out of other HTTP libraries. Supports:
- HTTP and HTTPS
- Keep-Alive
- Authentication
- Caching
- All Methods
- Redirects
- Compression
- Lost update support
- Unit Tested

%description -l pl.UTF-8
httplib2.py to obszerna biblioteka klienta HTTP, obsługująca wiele
cech pomijanych przez inne biblioteki. Obsługuje:
- HTTP i HTTPS
- Keep-Alive
- uwierzytelnianie
- buforowanie
- wszystkie metody
- przekierowania
- kompresję
- Lost update
- podlega testom jednostkowym.

%package apidocs
Summary:	API documentation for Python httplib2 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona httplib2
Group:		Documentation

%description apidocs
API documentation for Python httplib2 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona httplib2.

%prep
%setup -q -n httplib2-%{version}
%patch -P 0 -p1

%build
%py3_build

%if %{with tests}
# proxy tests cause the next test to fail with "previous item was not torn down properly", reason unknown
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin,pytest_forked,pytest_timeout \
PYTHONPATH=$(pwd)/build-3/lib \
%{__python3} -m pytest tests -k 'not test_functional_socks5 and not test_functional_noproxy_star_http and not test_functional_noproxy_star_https'
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/httplib2/cacerts.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.md
%{py3_sitescriptdir}/httplib2
%{py3_sitescriptdir}/httplib2-%{version}-py*.egg-info

%files apidocs
%defattr(644,root,root,755)
%doc doc/html/{_static,*.html,*.js}
