%global base_name woodstox
%global core_name %{base_name}-core
%global stax2_ver  3.1.1

Name:             %{core_name}
Version:          4.1.2
Release:          8%{?dist}
Summary:          High-performance XML processor
License:          ASL 2.0 or LGPLv2+
URL:              http://%{base_name}.codehaus.org/

Source0:          http://%{base_name}.codehaus.org/%{version}/%{core_name}-src-%{version}.tar.gz

Patch0:           %{name}-unbundling.patch
Patch1:           %{name}-fsf-address.patch

BuildArch:        noarch

BuildRequires:    felix-osgi-core
BuildRequires:    relaxngDatatype
BuildRequires:    msv-xsdlib
BuildRequires:    msv-msv
BuildRequires:    stax2-api
BuildRequires:    java-devel
BuildRequires:    maven-local
BuildRequires:    jpackage-utils


%description
Woodstox is a high-performance validating namespace-aware StAX-compliant
(JSR-173) Open Source XML-processor written in Java.
XML processor means that it handles both input (== parsing)
and output (== writing, serialization)), as well as supporting tasks
such as validation.

%package javadoc
Summary:          API documentation for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{base_name}-%{version}

cp src/maven/%{name}-asl.pom pom.xml
cp src/maven/%{name}-lgpl.pom pom-lgpl.xml

%patch0 -p1
%patch1 -p1

sed -i "s/@VERSION@/%{version}/g" pom.xml pom-lgpl.xml
sed -i "s/@REQ_STAX2_VERSION@/%{stax2_ver}/g" pom.xml pom-lgpl.xml

# removing bundled stuff
rm -rf lib
rm -rf src/maven
rm -rf src/resources
rm -rf src/samples
rm -rf src/java/org
rm -rf src/test/org
rm -rf src/test/stax2

# fixing incomplete source directory structure
mkdir src/main
mv -f src/java src/main/
mkdir src/test/java
mv -f src/test/wstxtest src/test/java/

# provided by JDK
%pom_remove_dep javax.xml.stream:stax-api

%mvn_file : %{name} %{name}-asl
%mvn_alias {org.codehaus.woodstox}:%{name}-asl @1:%{name}-lgpl

%build
# stax2 missing -> cannot compile tests -> tests skipped
%mvn_build -f

%install
%mvn_install

# install also LGPL version of POM
install -Dpm 644 pom-lgpl.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}-lgpl.pom

%files -f .mfiles
%doc release-notes/asl/ASL2.0 release-notes/lgpl/LGPL2.1 release-notes/asl/NOTICE
%{_mavenpomdir}/JPP-%{name}-lgpl.pom

%files javadoc -f .mfiles-javadoc
%doc release-notes/asl/ASL2.0 release-notes/lgpl/LGPL2.1

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.1.2-8
- Mass rebuild 2013-12-27

* Thu Aug 15 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.2-7
- Migrate away from mvn-rpmbuild (#997432)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.2-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 4.1.2-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Jaromir Capik <jcapik@redhat.com> - 4.1.2-1
- Initial version
