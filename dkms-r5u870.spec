%define module r5u870
%define name dkms-%{module}
%define version 0.11.0
%define release 7

Summary: Ricoh RY5U870 webcam driver
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://mediati.org/%{module}/%{module}-%{version}.tar.gz
# Link to the parent, else hal will ignore it
Patch0:	r5u870-0.11.0-set_device.patch
License: GPL
Group: System/Kernel and hardware
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url: https://wiki.mediati.org/R5u870
BuildArch: noarch
Requires(post): dkms
Requires(preun): dkms

%description
r5u870 is a driver for Ricoh RY5U870 webcams.

%prep
%setup -q -n %{module}-%{version}

%patch0 -p1

rm -f *.fw

cat > dkms.conf <<EOF
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}-%{release}
BUILT_MODULE_NAME[0]=r5u870
BUILT_MODULE_NAME[1]=usbcam
BUILT_MODULE_LOCATION[1]=usbcam
DEST_MODULE_LOCATION[0]=/kernel/drivers/media/video
DEST_MODULE_LOCATION[1]=/kernel/drivers/media/video
MODULES_CONF_EXTRACT_ALIASES[0]=yes
AUTOINSTALL=yes
EOF

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{version}-%{release}/
tar c . | tar x -C %{buildroot}/usr/src/%{module}-%{version}-%{release}/

%clean
rm -rf %{buildroot}

%post
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{module} -v %{version}-%{release}
:

%preun
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{module} -v %{version}-%{release} --all
:

%files
%defattr(-,root,root)
/usr/src/%{module}-%{version}-%{release}


%changelog
* Fri Mar 06 2009 Antoine Ginies <aginies@mandriva.com> 0.11.0-6mdv2009.1
+ Revision: 350652
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.11.0-5mdv2009.0
+ Revision: 244352
- rebuild

* Wed Apr 02 2008 Pascal Terjan <pterjan@mandriva.org> 0.11.0-3mdv2008.1
+ Revision: 191657
- Link to the device, else hal will ignore it and rights will be wrong (#39182)
- Add the aliases in /etc/modprobe.d/ so that it gets loaded instead of the generic uvcvideo (#39182 too)

* Fri Mar 21 2008 Olivier Blin <oblin@mandriva.com> 0.11.0-2mdv2008.1
+ Revision: 189450
- install usbcam module as well (#39182)

* Fri Feb 29 2008 Olivier Blin <oblin@mandriva.com> 0.11.0-1mdv2008.1
+ Revision: 176724
- 0.11.0
- remove 1837 patch (better one upstream)
- update URL

  + Thierry Vignaud <tvignaud@mandriva.com>
    - fix no-buildroot-tag

* Mon Dec 03 2007 Olivier Blin <oblin@mandriva.com> 0.10.0-1mdv2008.1
+ Revision: 114630
- initial r5u870 package
- create dkms-r5u870

