Name:           python-uranium
Version:        3.4.1
Release:        1%{?dist}
Summary:        A Python framework for building desktop applications
License:        LGPLv3+
URL:            https://github.com/Ultimaker/Uranium
Source0:        %{url}/archive/%{version}.tar.gz#/Uranium-%{version}.tar.gz
Patch0:         0001-fix-uranium-tests.patch

BuildRequires:  python3-devel
BuildRequires:  /usr/bin/doxygen
BuildRequires:  /usr/bin/msgmerge
BuildRequires:  cmake
BuildRequires:  git

# Tests
BuildRequires:  python3-arcus == %{version}
BuildRequires:  python3-numpy
BuildRequires:  python3-scipy
BuildRequires:  python3-qt5
BuildRequires:  python3-pytest

BuildArch:      noarch

# There are Python plugins in /usr/lib/uranium
# We need to byte-compile it with Python 3
%global __python %{__python3}

%description
Uranium is a Python framework for building 3D printing related applications.

%package -n python3-uranium
Summary:        %{summary}
Provides:       uranium = %{version}-%{release}
%{?python_provide:%python_provide python3-uranium}

Requires:       python3-arcus == %{version}
Requires:       python3-numpy
Requires:       python3-scipy
Requires:       python3-qt5
Recommends:     python3-numpy-stl

%description -n python3-uranium
Uranium is a Python framework for building 3D printing related applications.

%package doc
Summary: Documentation for %{name} package

%description doc
Documentation for Uranium, a Python framework for building 3D printing
related applications.

%prep
%autosetup -n Uranium-%{version} -p1 -S git
#%patch0 -p1

# empty file. appending to the end to make sure we are not overriding
# a non empty file in the future
echo '# empty' >> UM/Settings/ContainerRegistryInterface.py

%build
# there is no arch specific content, so we set LIB_SUFFIX to nothing
# see https://github.com/Ultimaker/Uranium/commit/862a246bdfd7e25541b04a35406957612c6f4bb7
%{cmake} -DLIB_SUFFIX:STR= .
make %{?_smp_mflags}
make doc

%check
pip3 freeze

# https://github.com/Ultimaker/Uranium/issues/345
#%{__python3} -m pytest -v -k "not test_emptyPlugin"


%install
make install DESTDIR=%{buildroot}

# Move the cmake files
mv %{buildroot}%{_datadir}/cmake* %{buildroot}%{_datadir}/cmake

# Sanitize the location of locale files
pushd %{buildroot}%{_datadir}
mv uranium/resources/i18n locale
ln -s ../../locale uranium/resources/i18n
rm locale/uranium.pot
rm locale/*/uranium.po
popd

%find_lang uranium


%files -n python3-uranium -f uranium.lang
%license LICENSE
%doc README.md
%{python3_sitelib}/UM
%{_datadir}/uranium
# Own the dir not to depend on cmake:
%{_datadir}/cmake
%{_prefix}/lib/uranium


%files doc
%license LICENSE
%doc html


%changelog
* Wed May 02 2018 Miro Hrončok <mhroncok@redhat.com> - 3.3.0-1
- Update to 3.3.0 (#1571792)
- Skip test_emptyPlugin

* Mon Mar 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-1
- Update to 3.2.1 (#1523904)
- Force install to /usr/lib and keep this noarch

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 10 2017 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-1
- Update to 3.1.0 (#1523904)
- No need to sed dist-packages out anymore
- getMimeTypeForFile fails no more
- but some others tests are, add a fix

* Fri Oct 20 2017 Charalampos Stratakis <cstratak@redhat.com> - 3.0.3-1
- Update to 3.0.3 (#1504439)

* Wed Aug 30 2017 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-2
- Relocate Japanese locale to ja

* Wed Aug 30 2017 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-1
- Update to 2.7.0 (#1486741)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-2
- Fix the test_uniqueName test failure

* Wed Jun 28 2017 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-1
- Update to 2.6.1
- Skip test_uniqueName test (reported)

* Tue Jun 27 2017 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-1
- Update to 2.6.0

* Wed May 03 2017 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-2
- Actually include the cmake files (needed for cura)

* Wed Apr 26 2017 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-1
- Initial package

