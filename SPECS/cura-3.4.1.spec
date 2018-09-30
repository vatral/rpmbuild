Name:           cura
Epoch:          1
Version:        3.4.1
Release:        1%{?dist}
Summary:        3D printer control software

# https://lists.fedoraproject.org/archives/list/legal@lists.fedoraproject.org/thread/MOUNX6I3POCDMYWBNJ7JPLLIKVYWVRBJ/
License:        LGPLv3+

URL:            https://ultimaker.com/en/products/cura-software
Source0:        https://github.com/Ultimaker/Cura/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

# There are Python plugins in /usr/lib/cura
# We need to byte-compile it with Python 3
%global __python %{__python3}

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  dos2unix
BuildRequires:  gettext
BuildRequires:  git
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-uranium == %{version}

Requires:       open-sans-fonts
Requires:       python3-pyserial
Requires:       python3-savitar == %{version}
Requires:       python3-uranium == %{version}
Requires:       python3-zeroconf
Requires:       qt5-qtquickcontrols
Requires:       qt5-qtquickcontrols2
Requires:       CuraEngine == %{epoch}:%{version}
Requires:       cura-fdm-materials == %{version}

# Workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1494278
Requires:       libglvnd-devel

# So that it just works
Requires:       3dprinter-udev-rules

%description
Cura is a project which aims to be an single software solution for 3D printing.
While it is developed to be used with the Ultimaker 3D printer, it can be used
with other RepRap based designs.

Cura prepares your model for 3D printing. For novices, it makes it easy to get
great results. For experts, there are over 200 settings to adjust to your
needs. As it's open source, our community helps enrich it even more.

%prep
%autosetup -p1 -S git -n Cura-%{version}

# The setup.py is only useful for py2exe, remove it, so noone is tempted to use it
rm setup.py

# Wrong end of line encoding
dos2unix docs/How_to_use_the_flame_graph_profiler.md

# Wrong shebang
sed -i '1s=^#!/usr/bin/\(python\|env python\)3*=#!%{__python3}=' cura_app.py


%build
%{cmake} -DCURA_VERSION:STRING=%{version} -DLIB_SUFFIX:STR= .
make %{?_smp_mflags}

# rebuild locales
cd resources/i18n
rm *.pot
for DIR in *; do
  pushd $DIR
  for FILE in *.po; do
    msgfmt $FILE.po -o LC_MESSAGES/${FILE%po}mo || :
  done
  popd
done
cd -


%install
make install DESTDIR=%{buildroot}

# Sanitize the location of locale files
pushd %{buildroot}%{_datadir}
mv cura/resources/i18n locale
ln -s ../../locale cura/resources/i18n
rm locale/*/*.po
popd

# Unbundle fonts
rm -rf %{buildroot}%{_datadir}/%{name}/resources/themes/cura-light/fonts/
ln -s %{_datadir}/fonts/open-sans/ %{buildroot}%{_datadir}/%{name}/resources/themes/cura-light/fonts

%find_lang cura
%find_lang fdmextruder.def.json
%find_lang fdmprinter.def.json


%check
%{__python3} -m pip freeze
%{__python3} -m pytest -v

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files -f cura.lang -f fdmextruder.def.json.lang -f fdmprinter.def.json.lang
%license LICENSE
%doc README.md
# CHANGES is not updated since 15.x
# things in docs are developer oriented
%{python3_sitelib}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/icons/hicolor/128x128/apps/%{name}-icon.png
%{_datadir}/mime/packages/%{name}.xml
%{_bindir}/%{name}
%{_prefix}/lib/%{name}

%changelog
* Wed May 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1:3.3.0-1
- Update to 3.3.0
- Enable test_getPropertyFallThrough again

* Wed Mar 21 2018 Miro Hrončok <mhroncok@redhat.com> - 1:3.2.1-2
- Require qt5-qtquickcontrols2 in addition to qt5-qtquickcontrols

* Tue Mar 20 2018 Miro Hrončok <mhroncok@redhat.com> - 1:3.2.1-1
- Update to 3.2.1
- Force install to /usr/lib and keep this noarch
- Change the set of skipped tests

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 10 2017 Miro Hrončok <mhroncok@redhat.com> - 1:3.1.0-1
- Update to 3.1.0
- Disable most of the tests
- No longer needs to sed out dist-packages
- Move appdata to metainfo

* Mon Dec 04 2017 Miro Hrončok <mhroncok@redhat.com> - 1:3.0.3-5
- Mark the package with correct license

* Sun Dec 03 2017 Miro Hrončok <mhroncok@redhat.com> - 1:3.0.3-4
- Also apply the nvidia driver workaround on Fedora (#1520138)

* Tue Nov 21 2017 Miro Hrončok <mhroncok@redhat.com> - 1:3.0.3-3
- Require libglvnd-devel as a workaround for #1494278

* Fri Oct 27 2017 Miro Hrončok <mhroncok@redhat.com> - 1:3.0.3-2
- Add upstream commit to fix tests

* Mon Oct 23 2017 Miro Hrončok <mhroncok@redhat.com> - 1:3.0.3-1
- Update to 3.0.3
- Remove locale and desktop file changes (fixed upstream)

* Wed Aug 30 2017 Miro Hrončok <mhroncok@redhat.com> - 1:2.7.0-2
- Relocate Japanese locale to ja

* Wed Aug 30 2017 Miro Hrončok <mhroncok@redhat.com> - 1:2.7.0-1
- Update to 2.7.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Miro Hrončok <mhroncok@redhat.com> - 1:2.6.1-2
- Require cura-fdm-materials

* Wed Jun 28 2017 Miro Hrončok <mhroncok@redhat.com> - 1:2.6.1-1
- Updated to 2.6.1

* Wed May 10 2017 Miro Hrončok <mhroncok@redhat.com> - 1:2.5.0-2
- Require qt5-qtquickcontrols

* Wed May 03 2017 Miro Hrončok <mhroncok@redhat.com> - 1:2.5.0-1
- Update to modern Cura 2.x (introduce Epoch) (#1393176)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 15.04.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 03 2016 Miro Hrončok <mhroncok@redhat.com> - 15.04.4-5
- Explicitly run cura on X11 GDK backend (#1388953)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.04.4-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Mar 25 2016 Miro Hrončok <mhroncok@redhat.com> - 15.04.4-3
- Require 3dprinter-udev-rules

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 15.04.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Miro Hrončok <mhroncok@redhat.com> - 15.04.4-1
- New version

* Wed Jul 08 2015 Miro Hrončok <mhroncok@redhat.com> - 15.02.1-4
- No longer depend on pypy
- Simplify the launcher

* Mon Jul 06 2015 Miro Hrončok <mhroncok@redhat.com> - 15.02.1-3
- Patch for #1230281

* Mon Jul 06 2015 Miro Hrončok <mhroncok@redhat.com> - 15.02.1-2
- Require latest CuraEngine

* Mon Jul 06 2015 Miro Hrončok <mhroncok@redhat.com> - 15.02.1-1
- Update to 15.02.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.12.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Miro Hrončok <mhroncok@redhat.com> - 14.12.1-4
- Patch: Open directories with xdg-open (#1217961)

* Mon Apr 20 2015 Miro Hrončok <mhroncok@redhat.com> - 14.12.1-3
- Handle files from the command line (#1213220)

* Mon Mar 30 2015 Miro Hrončok <mhroncok@redhat.com> - 14.12.1-2
- Update the no firmware patch according to communication with Cura upstream

* Mon Dec 29 2014 Miro Hrončok <mhroncok@redhat.com> - 14.12.1-1
- Updated to 14.12.1
- No longer depend on firmware

* Sat Oct 25 2014 Miro Hrončok <mhroncok@redhat.com> - 14.09-1
- New version 14.09

* Tue Jun 24 2014 Miro Hrončok <mhroncok@redhat.com> - 14.06-2
- Require at least the firmware version originally bundled in git

* Mon Jun 23 2014 Miro Hrončok <mhroncok@redhat.com> - 14.06-1
- New version 14.06

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 14 2013 Miro Hrončok <mhroncok@redhat.com> - 13.11.2-1
- New version 13.11.2

* Wed Oct 16 2013 Miro Hrončok <mhroncok@redhat.com> - 13.10-1
- New upstream release with CuraEngine

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Miro Hrončok <mhroncok@redhat.com> - 13.04-2
- Remove resources directory before trying to create a symlink there

* Sat May 04 2013 Miro Hrončok <mhroncok@redhat.com> - 13.04-1
- New upstream release
- Fixed missing slice module

* Sat Apr 20 2013 Miro Hrončok <mhroncok@redhat.com> - 13.03-1
- New upstream release

* Tue Feb 19 2013 Miro Hrončok <mhroncok@redhat.com> - 12.12-3
- chmod 755 cura-stripper.sh
- Use firmware from ultimaker-marlin-firmware package
- removed bundling note

* Sun Jan 20 2013 Miro Hrončok <mhroncok@redhat.com> - 12.12-2
- Launcher is in Python now

* Sun Jan 13 2013 Miro Hrončok <mhroncok@redhat.com> - 12.12-1
- First version

