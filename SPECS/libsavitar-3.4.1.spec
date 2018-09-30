Name:           libsavitar
Version:        3.4.1
Release:        1%{?dist}
Summary:        C++ implementation of 3mf loading with SIP Python bindings
License:        LGPLv3+
URL:            https://github.com/Ultimaker/libSavitar
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

Patch0:         %{name}-no-pugixml.patch

BuildRequires:  cmake
BuildRequires:  dos2unix
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  pugixml-devel
BuildRequires:  python3-devel
BuildRequires:  python3-sip-devel
BuildRequires:  /usr/bin/sip

%description
Savitar is a C++ implementation of 3mf loading with SIP Python bindings.
3mf is a 3D printing file format.

%package        devel

# The cmake scripts are BSD
License:        AGPLv3+ and BSD

Summary:        Development files for libsavitar
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Savitar is a C++ implementation of 3mf loading with SIP Python bindings.
3mf is a 3D printing file format.

Development files.

%package -n     python3-savitar
Summary:        Python 3 libSavitar bindings
%{?python_provide:%python_provide python3-savitar}

%description -n python3-savitar
Savitar is a C++ implementation of 3mf loading with SIP Python bindings.
3mf is a 3D printing file format.

The Python bindings.

%prep
%autosetup -n libSavitar-%{version} -p1 -S git

# Wrong end of line encoding
dos2unix README.md

# Bundling
rm pugixml -rf
sed -i 's|"../pugixml/src/pugixml.hpp"|<pugixml.hpp>|g' src/*.cpp src/*.h


%build
export CXXFLAGS="%{optflags} -Wl,--as-needed"
%{cmake} -DCMAKE_SKIP_RPATH:BOOL=ON .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README.md
%{_libdir}/libSavitar.so.*

%files devel
%license LICENSE cmake/COPYING-CMAKE-SCRIPTS
%{_libdir}/libSavitar.so
%{_includedir}/Savitar
# Own the dir not to depend on cmake:
%{_libdir}/cmake

%files -n python3-savitar
%license LICENSE
%doc README.md
%{python3_sitearch}/Savitar.so

%changelog
* Wed May 02 2018 Miro Hrončok <mhroncok@redhat.com> - 3.3.0-1
- Update to 3.3.0 (#1571783)

* Mon Mar 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-2
- Fix license tag (AGPLv3+ to LGPLv3+)

* Mon Mar 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-1
- Update to 3.2.1 (#1523886)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Dec 09 2017 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-1
- Update to 3.1.0 (#1523886)
- Don't sed lib -> lib64 (not needed now)

* Mon Oct 23 2017 Miro Hrončok <mhroncok@redhat.com> - 3.0.3-1
- Update to 3.0.3 (#1505189)

* Wed Aug 30 2017 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-1
- Update to 2.7.0 (#1486731)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-1
- Updated to 2.6.1 (#1465417)

* Tue Jun 27 2017 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-1
- Updated to 2.6.0 (#1465417)

* Wed May 03 2017 Miro Hrončok <mhroncok@redhat.com> - 0-0.1.20170501git1ad7ddb
- New package
