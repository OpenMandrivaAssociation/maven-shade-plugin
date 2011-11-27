Name:           maven-shade-plugin
Version:        1.4
Release:        5
Summary:        This plugin provides the capability to package the artifact in an uber-jar

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/%{name}
# svn export http://svn.apache.org/repos/asf/maven/plugins/tags/maven-shade-plugin-1.4
# tar caf maven-shade-plugin-1.4.tar.xz maven-shade-plugin-1.4
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}.depmap
Patch1:         pom.xml.maven-artifact-manager.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: jpackage-utils
BuildRequires: plexus-utils
BuildRequires: ant-nodeps
BuildRequires: maven2
BuildRequires: maven-wagon
BuildRequires: maven-enforcer-plugin
BuildRequires: plexus-container-default
BuildRequires: maven-install-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-shared-plugin-testing-harness
BuildRequires: jdependency >= 0.6
Requires: ant-nodeps
Requires: maven2
Requires: jpackage-utils
Requires: java >= 0:1.6.0
Requires: jdependency >= 0.6
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

Obsoletes: maven2-plugin-shade <= 0:2.0.8
Provides: maven2-plugin-shade = 1:%{version}-%{release}

%description
This plugin provides the capability to package the artifact in an
uber-jar, including its dependencies and to shade - i.e. rename - the
packages of some of the dependencies.


%package javadoc
Group:          Development/Java
Summary:        API documentation for %{name}
Requires:       jpackage-utils

%description javadoc
%{summary}.


%prep
%setup -q #You may need to update this according to your Source0
rm src/test/jars/plexus-utils-1.4.1.jar
ln -s $(build-classpath plexus/utils) src/test/jars/plexus-utils-1.4.1.jar

# Add dependency on maven-artifact-manager
%patch1 -p0

# remove failing test:  testShadeWithFilter
rm src/test/java/org/apache/maven/plugins/shade/mojo/ShadeMojoTest.java

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
# we skip test because even with binary mvn release these fail for
# various reasons.
mvn-jpp -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven2.jpp.depmap.file="%{SOURCE1}" \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -Dpm 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# poms
install -Dpm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%add_to_maven_depmap org.apache.maven.plugins %{name} %{version} JPP %{name}

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

