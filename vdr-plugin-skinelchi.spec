
%define plugin	skinelchi
%define name	vdr-plugin-%plugin
%define version	0.1.1
%define prever	pre2
%define rel	10

Summary:	VDR plugin: Elchi VDR Skin-Plugin
Name:		%name
Version:	%version
%if %prever
Release:	%mkrel 0.%prever.%rel
%else
Release:	%mkrel %rel
%endif
Group:		Video
License:	GPL
URL:		http://www.vdr-portal.de/board/thread.php?threadid=41915
%if %prever
Source:		vdr-%plugin-%version%prever.tar.bz2
%else
Source:		vdr-%plugin-%version.tar.bz2
%endif
Patch0:		skinelchi-0.1.1pre2-i18n-1.6.patch
# warning: cannot pass objects of non-POD type ‘class cString’ through ‘...’; call will abort at runtime
Patch7:		skinelchi-non-pod-type.patch
# dpatches from e-tobi
Patch1:		03_const-warning-fixes.dpatch
Patch2:		90_vdr-skinelchi-0.1.1pre2.PatchCollection.dpatch
Patch3:		91_skinelchi-0.1.1pre2-1.5.0.dpatch
Patch4:		92_vdr-skinelchi-0.1.1_pre2-vdr-1.5.5-getfont.dpatch
Patch5:		93_vdr-1.5.15.dpatch

Patch6:		skinelchi-format-string.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.6.0-7
BuildRequires:	libMagick-devel
Requires:	vdr-abi = %vdr_abi

%description
VDR skin plugin, based on:
    - original-skins of vdr
    - Elchi for vdr 1.2.6 and enElchi/Elchi for text2skin
    - osdimage from brougs78

%vdr_chanlogo_notice

%prep
%if %prever
%setup -q -n %plugin-%version%prever
%else
%setup -q -n %plugin-%version
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%vdr_plugin_prep

perl -pi -e 's,/video/epgimages,%{_vdr_plugin_cachedir}/epgimages,' setup.c skinelchi.c

%vdr_plugin_params_begin %plugin
# optional path for epgimages (default: %{_vdr_plugin_cachedir}/epgimages)
var=ICACHE
param=--icache=ICACHE
# path for channel logos
var=LOGO_DIR
param=--logos=LOGO_DIR
default=%{_vdr_chanlogodir}
%vdr_plugin_params_end

cat > README.install.urpmi <<EOF
%vdr_chanlogo_notice
EOF

%build
VDR_PLUGIN_EXTRA_FLAGS="$(pkg-config --cflags ImageMagick++)"
%vdr_plugin_build HAVE_IMAGEMAGICK=1

%install
rm -rf %{buildroot}
%vdr_plugin_install

%clean
rm -rf %{buildroot}

%post
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc README HISTORY README.install.urpmi
