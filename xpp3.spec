%global pkg_name xpp3
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%define oversion 1.1.3_8

Summary:        XML Pull Parser
Name:           %{?scl_prefix}%{pkg_name}
Version:        1.1.3.8
Release:        11.7%{?dist}
Epoch:          0
License:        ASL 1.1
URL:            http://www.extreme.indiana.edu/xgws/xsoap/xpp/mxp1/index.html
Source0:        http://www.extreme.indiana.edu/dist/java-repository/xpp3/distributions/xpp3-%{oversion}_src.tgz
Source1:        http://mirrors.ibiblio.org/pub/mirrors/maven2/xpp3/xpp3/1.1.3.4.O/xpp3-1.1.3.4.O.pom
Source2:        http://mirrors.ibiblio.org/pub/mirrors/maven2/xpp3/xpp3_xpath/1.1.3.4.O/xpp3_xpath-1.1.3.4.O.pom
Source3:        http://mirrors.ibiblio.org/pub/mirrors/maven2/xpp3/xpp3_min/1.1.3.4.O/xpp3_min-1.1.3.4.O.pom
Patch0:         %{pkg_name}-link-docs-locally.patch
BuildRequires:  %{?scl_prefix}javapackages-tools
BuildRequires:  %{?scl_prefix}ant
BuildRequires:  %{?scl_prefix}junit
BuildRequires:  %{?scl_prefix}xml-commons-apis
Requires:       %{?scl_prefix}junit
Requires:       %{?scl_prefix}xml-commons-apis

BuildArch:      noarch

%description
XML Pull Parser 3rd Edition (XPP3) MXP1 is an XmlPull
parsing engine that is based on ideas from XPP and in
particular XPP2 but completely revised and rewritten to
take best advantage of latest JIT JVMs such as Hotspot in JDK 1.4.

%package minimal
Summary:        Minimal XML Pull Parser
Requires:       %{?scl_prefix}junit
Requires:       %{?scl_prefix}xml-commons-apis

%description minimal
Minimal XML pull parser implementation.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{oversion}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# remove all binary libs
find -name \*.jar -delete

%patch0
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
export CLASSPATH=$(build-classpath xml-commons-apis junit)
ant xpp3 junit apidoc
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}

# JARs
install -p -m 644 build/%{pkg_name}-%{oversion}.jar \
    %{buildroot}%{_javadir}/%{pkg_name}.jar
install -p -m 644 build/%{pkg_name}_xpath-%{oversion}.jar \
    %{buildroot}%{_javadir}/%{pkg_name}-xpath.jar
install -p -m 644 build/%{pkg_name}_min-%{oversion}.jar \
    %{buildroot}%{_javadir}/%{pkg_name}-minimal.jar

# POMs
install -p -m 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}.pom
install -p -m 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}-xpath.pom
install -p -m 644 %{SOURCE3} %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}-minimal.pom

# XMvn metadata
%add_maven_depmap
%add_maven_depmap JPP-%{pkg_name}-xpath.pom %{pkg_name}-xpath.jar
%add_maven_depmap JPP-%{pkg_name}-minimal.pom %{pkg_name}-minimal.jar -f minimal

# Javadocs
cp -pr doc/api/* %{buildroot}%{_javadocdir}/%{name}
%{?scl:EOF}

%files -f .mfiles
%doc README.html LICENSE.txt doc/*

%files minimal -f .mfiles-minimal
%doc LICENSE.txt

%files javadoc
%doc %{_javadocdir}/%{name}

%changelog
* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3.8-11.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3.8-11.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3.8-11.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3.8-11.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3.8-11.3
- SCL-ize requires and build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3.8-11.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3.8-11.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.1.3.8-11
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3.8-10
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Jun 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3.8-9
- General specfile cleanup
- Update to current packaging guidelines

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1.3.8-4
- Fix pom filenames (Resolves rhbz#655829)
- Changes according to new guidelines (versionless jars)
- Fix few packaging problems (post/postun deps)

* Mon Jun 14 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.3.8-3.4
- Add maven poms and depmaps.

* Wed Mar 10 2010 Peter Lemenkov <lemenkov@gmail.com> - 0:1.1.3.8-3.3
- *-javadoc must also require jpackage-utils (for %%{_javadocdir})

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1.3.8-1.2
- fix license tag
- drop jpp tag

* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.8-1jpp.1
- Import
- Fix per Fedora spec

* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.8-1jpp
- Upgrade to 1.1.3.8
- Remove vendor and distribution tags

* Mon Feb 27 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.4-1.o.2jpp
- First JPP 1.7 build

* Tue Dec 20 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.o.1jpp
- Upgrade to 1.1.3.4-O
- Now includes xpath support

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.d.2jpp
- Build with ant-1.6.2

* Tue Jun 01 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.d.1jpp
- Update to 1.1.3.4

* Mon May  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.3jpp
- Fix non-versioned javadoc symlinking.

* Mon Apr 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.2jpp
- Include non-versioned javadoc symlink.

* Tue Apr  1 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.1jpp
- First JPackage release.
