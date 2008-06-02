%define rel 4

Name:           gonzui
Version:        1.2
Release:        %mkrel %rel
Summary:        Source code search engine 
Group:          Development/Other
License:        GPL
URL:            http://gonzui.sourceforge.net/
Source0:        %{name}-%{version}.tar.bz2
Source1:        gonzui.init
Source2:        gonzuirc
Source3:        gonzui.logrotate
Patch1:         gonzui-1.2-multi_checkout.diff
Patch2:         gonzui-1.2-name_tagging.diff 
Patch3:         gonzui-1.2-svn_ssh.diff 
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  ruby-devel ruby-bdb
Requires:       ruby-bdb
Requires(pre):     rpm-helper
Requires(post):    rpm-helper
Requires(postun):  rpm-helper
Requires(preun):   rpm-helper


%description
Gonzui is a source code search engine for accelerating open source software 
development. In the open source software development, programmers frequently 
refer to source codes written by others.
 
Our goal is to help programmers develop programs effectively by creating a 
source code search engine that covers vast quantities of open source codes 
available on the Internet.

%prep
%setup -q
# more than one cvs
%patch1
# --name
%patch2
# svn+ssh support
%patch3

%build
%configure
%make

%check
#TODO

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
mkdir -p $RPM_BUILD_ROOT/%_initrddir/
cp %SOURCE1 $RPM_BUILD_ROOT/%_initrddir/%name
cp %SOURCE2 $RPM_BUILD_ROOT/%_sysconfdir/%{name}rc
mkdir -p $RPM_BUILD_ROOT/%_sysconfdir/logrotate.d/
cp %SOURCE3 $RPM_BUILD_ROOT/%_sysconfdir/logrotate.d/%{name}

mkdir -p $RPM_BUILD_ROOT/%_localstatedir/lib/%name
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc doc README AUTHORS ChangeLog NEWS
%config(noreplace)    %_sysconfdir/%{name}rc
%attr(0755,root,root) %_initrddir/%{name}
%_datadir/%name
%_bindir/%name-*

%exclude %dir %ruby_sitearchdir
%{ruby_sitelibdir}/*
%_localstatedir/lib/%name

%config(noreplace) %_sysconfdir/%{name}rc*
%config(noreplace) %_sysconfdir/logrotate.d/*

%pre
%_pre_useradd %{name} %_datadir/%name /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun 
%_postun_userdel %{name}

