Name:           libarcus
Version:        3.4.1
Release:        1%{?dist}
Summary:        Communication library between internal components for Ultimaker software
License:        LGPLv3+
URL:            https://github.com/Ultimaker/libArcus
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  protobuf-devel
BuildRequires:  python3-devel
BuildRequires:  python3-protobuf
BuildRequires:  python3-sip-devel
BuildRequires:  /usr/bin/sip
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  git

%description
Arcus library contains C++ code and Python 3 bindings for creating a socket in
a thread and using this socket to send and receive messages based on the
Protocol Buffers library. It is designed to facilitate the communication
between Cura and its backend and similar code.

%package        devel

# The cmake scripts are BSD
License:        AGPLv3+ and BSD

Summary:        Development files for libarcus
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Arcus library contains C++ code and Python 3 bindings for creating a socket in
a thread and using this socket to send and receive messages based on the
Protocol Buffers library. It is designed to facilitate the communication
between Cura and its backend and similar code.

Development files.

%package -n     python3-arcus
Summary:        Python 3 libArcus bindings
%{?python_provide:%python_provide python3-arcus}

%description -n python3-arcus
Arcus Python 3 bindings for creating a socket in a thread and using this
socket to send and receive messages based on the
Protocol Buffers library. It is designed to facilitate the communication
between Cura and its backend and similar code.

%prep
%autosetup -n libArcus-%{version} -p1 -S git

%build
%{cmake} -DBUILD_EXAMPLES:BOOL=OFF -DCMAKE_SKIP_RPATH:BOOL=ON .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README.md TODO.md
%{_libdir}/libArcus.so.*

%files devel
%license LICENSE cmake/COPYING-CMAKE-SCRIPTS
%doc examples/example.cpp examples/example.proto
%{_libdir}/libArcus.so
%{_includedir}/Arcus
# Own the dir not to depend on cmake:
%{_libdir}/cmake

%files -n python3-arcus
%license LICENSE
%doc README.md TODO.md
%doc examples/example.py
%{python3_sitearch}/Arcus.so

%changelog
* Wed May 02 2018 Miro Hrončok <mhroncok@redhat.com> - 3.3.0-1
- Update to 3.3.0 (#1571482)

* Mon Mar 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-1
- Update to 3.2.1 (#1523891)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Dec 09 2017 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-1
- Update to 3.1.0 (#1523891)
- Don't sed lib -> lib64 (not needed now)

* Wed Nov 29 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.0.3-3
- Rebuild for protobuf 3.5

* Mon Nov 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0.3-2
- Rebuild for protobuf 3.4

* Fri Oct 20 2017 Charalampos Statakis <cstratak@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Wed Aug 30 2017 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-1
- Update to 2.7.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-1
- Update to 2.6.1

* Tue Jun 27 2017 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-1
- Update to 2.6.0

* Tue Jun 13 2017 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-3
- Rebuilt for new protobuf 3.3.1

* Wed May 03 2017 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-2
- Clarify licensing information on cmake files

* Wed Apr 26 2017 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-1
- Update to 2.5.0

* Sat Mar 25 2017 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-1
- Initial package
