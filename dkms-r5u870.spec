%define module r5u870
%define name dkms-%{module}
%define version 0.10.0
%define release %mkrel 1

Summary: Ricoh RY5U870 webcam driver 
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://avilella.googlepages.com/%{module}-%{version}.tgz
Patch0: r5u870-0.10.0-1837.patch
License: GPL
Group: System/Kernel and hardware
Url: http://www.qbik.ch/usb/devices/showdr.php?id=247
BuildArch: noarch
Requires(post): dkms
Requires(preun): dkms

%description
r5u870 is a driver for Ricoh RY5U870 webcams.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1 -b .1837
rm -f *.fw

cat > dkms.conf <<EOF
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}-%{release}
DEST_MODULE_LOCATION[0]="/kernel/drivers/media/video"
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
