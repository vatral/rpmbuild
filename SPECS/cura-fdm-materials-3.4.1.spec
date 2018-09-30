Name:           cura-fdm-materials
Version:        3.4.1
Release:        1%{?dist}
Summary:        Cura FDM Material database

# See https://github.com/Ultimaker/Cura/issues/1779 for clarification
License:        Public Domain


URL:            https://github.com/Ultimaker/fdm_materials
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  cmake
Requires:       cura == 1:%{version}

%description
Cura material files.

These files are needed to work with printers like Ultimaker 2+ and Ultimaker 3.

%prep
%autosetup -n fdm_materials-%{version} -p1

%build
%{cmake} .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}


%files
%license LICENSE
%{_datadir}/cura/resources/materials/

%changelog
* Wed May 02 2018 Miro Hrončok <mhroncok@redhat.com> - 3.3.0-1
- Update to 3.3.0 (#1572931)

* Tue Mar 20 2018 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-1
- Update to 3.2.1 (#1523960)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 10 2017 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-1
- Update to 3.1.0 (#1523960)

* Mon Oct 23 2017 Miro Hrončok <mhroncok@redhat.com> - 3.0.3-1
- Update to 3.0.3 (#1504321)

* Wed Aug 30 2017 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-1
- Update to 2.7.0 (#1486725)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-1
- New package

