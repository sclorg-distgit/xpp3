%{?scl:%scl_package xpp3}
%{!?scl:%global pkg_name %{name}}

%global oversion 1.1.4c

Summary:        XML Pull Parser
Name:           %{?scl_prefix}xpp3
Version:        1.1.4
Release:        15.c.2%{?dist}
License:        ASL 1.1
URL:            http://www.extreme.indiana.edu/xgws/xsoap/xpp/mxp1/index.html
Source0:        http://www.extreme.indiana.edu/dist/java-repository/xpp3/distributions/xpp3-%{oversion}_src.tgz
Source1:        http://repo1.maven.org/maven2/xpp3/xpp3/%{oversion}/xpp3-%{oversion}.pom
Source2:        http://repo1.maven.org/maven2/xpp3/xpp3_xpath/%{oversion}/xpp3_xpath-%{oversion}.pom
Source3:        http://repo1.maven.org/maven2/xpp3/xpp3_min/%{oversion}/xpp3_min-%{oversion}.pom
Source4:        %{pkg_name}-%{oversion}-OSGI-MANIFEST.MF
Patch0:         %{pkg_name}-link-docs-locally.patch

BuildRequires:  %{?scl_prefix}javapackages-local
BuildRequires:  java-javadoc
BuildRequires:  zip
BuildRequires:  %{?scl_prefix}ant
BuildRequires:  %{?scl_prefix}junit

BuildArch:      noarch

%description
XML Pull Parser 3rd Edition (XPP3) MXP1 is an XmlPull
parsing engine that is based on ideas from XPP and in
particular XPP2 but completely revised and rewritten to
take best advantage of latest JIT JVMs such as Hotspot in JDK 1.4.

%package minimal
Summary:        Minimal XML Pull Parser

%description minimal
Minimal XML pull parser implementation.

%package javadoc
Summary:        Javadoc for %{pkg_name}
Requires:       java-javadoc

%description javadoc
Javadoc for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{oversion}
# remove all binary libs
find -name \*.jar -delete
# Remove class bundled from Axis (now it's bundled in JRE)
rm -rf src/java/builder/javax

%patch0

# "src/java/addons_tests" does not exist
sed -i 's|depends="junit_main,junit_addons"|depends="junit_main"|' build.xml

# relax javadoc linting
sed -i '/<javadoc/aadditionalparam="-Xdoclint:none"' build.xml

%build
export CLASSPATH=$(build-classpath junit)
ant xpp3 junit apidoc

# Add OSGi metadata
pushd build
mkdir META-INF
unzip -o %{pkg_name}-%{oversion}.jar META-INF/MANIFEST.MF
cat %{SOURCE4} >> META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u %{pkg_name}-%{oversion}.jar META-INF/MANIFEST.MF
popd

%install
%mvn_file ':{*}' @1
%mvn_package :xpp3_min minimal

%mvn_artifact %{SOURCE1} build/%{pkg_name}-%{oversion}.jar
%mvn_artifact %{SOURCE2} build/%{pkg_name}_xpath-%{oversion}.jar
%mvn_artifact %{SOURCE3} build/%{pkg_name}_min-%{oversion}.jar

# Javadocs
%mvn_install -J doc/api

%files -f .mfiles
%doc README.html doc/*.txt doc/*.html
%license LICENSE.txt

%files minimal -f .mfiles-minimal
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 1.1.4-15.c.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 1.1.4-15.c.1
- Automated package import and SCL-ization

* Tue May 16 2017 Mat Booth <mat.booth@redhat.com> - 1.1.4-15.c
- Remove unnecessary dep on xml-commons-apis
- Fix errors in javadoc generation

* Wed Mar 22 2017 Michael Simacek <msimacek@redhat.com> - 1.1.4-14.c
- Install jars directly into javadir

* Wed Mar 22 2017 Michael Simacek <msimacek@redhat.com> - 1.1.4-13.c
- Install with XMvn

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-12.c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 23 2016 Severin Gehwolf <sgehwolf@redhat.com> - 1.1.4-11.c
- Add OSGi metadata.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-10.c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.4-9.c
- Remove bundled javax.xml.namespace.QName class
- Resolves: rhbz#1299679

* Thu Dec 24 2015 gil cattaneo <puntogil@libero.it> 1.1.4-8.c
- convert %%defines to %%global

* Tue Jul 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.4-7.c
- Add build-requires on javapackages-local

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-6.c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 gil cattaneo <puntogil@libero.it> 1.1.4-5.c
- introduce license macro

* Tue Dec 9 2014 Alexander Kurtakov <akurtako@redhat.com> 1.1.4-4.c
- Drop useless Requires.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3.c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.4-2.c
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Michal Srb <msrb@redhat.com> - 1.1.4-1.c
- Update to upstream version 1.1.4c

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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
