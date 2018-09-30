Name:           CuraEngine
Epoch:          1
Version:        3.4.1
Release:        1%{?dist}
Summary:        Engine for processing 3D models into G-code instructions for 3D printers
License:        AGPLv3+
URL:            https://github.com/Ultimaker/%{name}
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  libarcus-devel == %{version}
BuildRequires:  polyclipping-devel >= 6.1.2
BuildRequires:  protobuf-devel
BuildRequires:  rapidjson-devel
BuildRequires:  cmake
BuildRequires:  git

Patch0:         %{name}-rpath.patch
Patch1:         %{name}-static-libstdcpp.patch

%description
%{name} is a C++ console application for 3D printing G-code generation. It
has been made as a better and faster alternative to the old Skeinforge engine.

This is just a console application for G-code generation. For a full graphical
application look at cura with is the graphical frontend for %{name}.

%prep
%autosetup -p1 -S git

# bundled libraries
rm -rf libs

# The -DCURA_ENGINE_VERSION does not work, so we sed-change the default value
sed -i 's/"DEV"/"%{version}"/' src/settings/settings.h

%build
%{cmake} -DBUILD_SHARED_LIBS:BOOL=OFF  -DCURA_ENGINE_VERSION:STRING=%{version} -DUSE_SYSTEM_LIBS:BOOL=ON -DCMAKE_CXX_FLAGS_RELEASE_INIT:STRING="%{optflags} -fPIC" .
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%check
# Smoke test
%{buildroot}%{_bindir}/%{name} help

%files
%doc LICENSE README.md
%{_bindir}/%{name}

%changelog
* Wed May 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1:3.3.0-1
- Updated to 3.3.0
- Make sure Fedora CXXFLAGS are used, also -fPIC
- Use new USE_SYSTEM_LIBS option instead of patch+sed

* Mon Mar 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1:3.2.1-1
- Updated to 3.2.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 10 2017 Miro Hrončok <mhroncok@redhat.com> - 1:3.1.0-1
- Updated to 3.1.0

* Wed Nov 29 2017 Igor Gnatenko <ignatenko@redhat.com> - 1:3.0.3-3
- Rebuild for protobuf 3.5

* Mon Nov 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:3.0.3-2
- Rebuild for protobuf 3.4

* Mon Oct 23 2017 Miro Hrončok <mhroncok@redhat.com> - 1:3.0.3-1
- Updated to 3.0.3

* Wed Aug 30 2017 Miro Hrončok <mhroncok@redhat.com> - 1:2.7.0-1
- Update to 2.7.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Miro Hrončok <mhroncok@redhat.com> - 1:2.6.1-1
- Updated to 2.6.1

* Tue Jun 27 2017 Miro Hrončok <mhroncok@redhat.com> - 1:2.6.0-1
- Updated to 2.6.0

* Wed Jun 14 2017 Miro Hrončok <mhroncok@redhat.com> - 1:2.5.0-2
- Rebuilt for new protobuf 3.3.1

* Wed May 03 2017 Miro Hrončok <mhroncok@redhat.com> - 1:2.5.0-1
- Updated to 2.5.0

* Sun Dec 04 2016 Miro Hrončok <mhroncok@redhat.com> - 1:2.3.1-1
- New version scheme -> Introduce Epoch
- Updated
- SPEC rewritten

* Sun Sep 18 2016 Miro Hrončok <mhroncok@redhat.com> - 15.04-4
- Rebuilt for new polyclipping (#1159525)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 15.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 06 2015 Miro Hrončok <mhroncok@redhat.com> - 15.04-2
- Set the VERSION variable

* Sun Jul 05 2015 Miro Hrončok <mhroncok@redhat.com> - 15.04-1
- Update to 15.04

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 14.12.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Dec 29 2014 Miro Hrončok <mhroncok@redhat.com> - 14.12.1-1
- Update to 14.12.1

* Thu Oct 23 2014 Miro Hrončok <mhroncok@redhat.com> - 14.03-3
- Rebuilt for new polyclipping

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 23 2014 Miro Hrončok <mhroncok@redhat.com> - 14.03-1
- New version 14.03

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 09 2014 Miro Hrončok <mhroncok@redhat.com> - 14.01-1
- New version 14.01
- polyclipping 6.1.x
- Now with make test
- Rebuilt against new polyclipping release

* Sat Dec 14 2013 Miro Hrončok <mhroncok@redhat.com> - 13.11.2-1
- New version 13.11.2
- Makefile seding changed to reflect changes
- Clipper usage no longer need patching

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.06.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Miro Hrončok <mhroncok@redhat.com> - 13.06.3-3
- Rebuilt for new polyclipping

* Thu Jul 04 2013 Miro Hrončok <mhroncok@redhat.com> - 13.06.3-2
- Added some explaining comments

* Sun Jun 23 2013 Miro Hrončok <mhroncok@redhat.com> - 13.06.3-1
- New package
