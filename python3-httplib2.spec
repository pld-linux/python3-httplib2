#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	A comprehensive HTTP client library
Summary(pl.UTF-8):	Obszerna biblioteka klienta HTTP
Name:		python3-httplib2
Version:	0.31.0
Release:	1
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://github.com/httplib2/httplib2/releases
Source0:	https://github.com/httplib2/httplib2/archive/v%{version}/httplib2-%{version}.tar.gz
# Source0-md5:	360cdbcdc8bbec3ce24c7bfff0d81e63
Patch0:		python-httplib2.certfile.patch
URL:		https://github.com/httplib2/httplib2
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pyparsing >= 2.4.2
BuildRequires:	python3-pyparsing < 4
BuildRequires:	python3-pytest >= 6.1.2
BuildRequires:	python3-pytest-cov >= 2.5.1
# >= 2.12.1
BuildRequires:	python3-pytest-forked >= 1.3.0
BuildRequires:	python3-pytest-randomly >= 1.2.3
BuildRequires:	python3-pytest-timeout >= 1.4.2
BuildRequires:	python3-six >= 1.10.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	ca-certificates
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

%prep
%setup -q -n httplib2-%{version}
%patch -P 0 -p1

%build
%py3_build

%if %{with tests}
# in python3 implementation system socks module is preferred over httplib2.socks, and the first is incompatible with test_socks5_auth
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin,pytest_timeout \
PYTHONPATH=$(pwd)/build-3/lib \
%{__python3} -m pytest tests -k 'not test_certs_file_from_builtin and not test_certs_file_from_environment and not test_ipv6 and not test_with_certifi_removed_from_modules and not test_noproxy_star and not test_server_not_found_error_is_raised_for_invalid_hostname and not test_socks5_auth'
%endif

%if %{with doc}
%{__make} -C doc html
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
