%define is_suse %(test -e /etc/SuSE-release && echo 1 || echo 0)
%define is_fedora %(test -e /etc/fedora-release && echo 1 || echo 0)
%define is_redhat %(test -e /etc/redhat-release && echo 1 || echo 0)

%if %{is_suse}
%define initscript dell_mdmon.suse
%endif
%if %{is_redhat} || %{is_fedora}
%define initscript dell_mdmon.rhel
%endif

Name: dell_mdleds
Version: 1.0
Release: 0
Requires: mdadm OpenIPMI /sbin/chkconfig
Vendor: Dell Inc.
Summary: Dell MDADM LED scripts
URL: http://linux.dell.com
Group: Utilities/System
License: GPL
BuildArch: i686 x86_64
Source0: dell_mdmon.rhel
Source1: dell_mdmon.suse
Source2: dell_mdleds

%description
This RPM provides the necessary scripts so that mdadm can set 
backplane LEDs (failure, identify) on Dell servers.

%prep
%build

%install
install -D -m755 %{_sourcedir}/dell_mdleds $RPM_BUILD_ROOT/usr/bin/dell_mdleds
install -D -m755 %{_sourcedir}/%{initscript} $RPM_BUILD_ROOT/etc/init.d/dell_mdmon

%clean

%files
%defattr(-,root,root)
/usr/bin/dell_mdleds
/etc/init.d/dell_mdmon

%post
# Post install script: add initscript
if [ -e /usr/lib/lsb/install_initd ] ; then
	/usr/lib/lsb/install_initd /etc/init.d/ipmi
	/usr/lib/lsb/install_initd /etc/init.d/dell_mdmon
elif [ -x /sbin/chkconfig ] ; then
	/sbin/chkconfig --add ipmi
	/sbin/chkconfig --add dell_mdmon
fi
service dell_mdmon start

%preun
# Pre uninstall script
if [ $1 = 0 ] ; then
	/etc/init.d/dell_mdmon stop
	if [ -x /usr/lib/lsb/remove_initd ] ; then
		/usr/lib/lsb/remove_initd dell_mdmon
	elif [ -x /sbin/chkconfig ] ; then
		/sbin/chkconfig --del dell_mdmon
	fi
fi

%changelog
