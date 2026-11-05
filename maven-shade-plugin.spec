%bcond_with javadoc
Name:           maven-shade-plugin
Version:        3.6.2
Release:        1
Summary:        This plugin provides the capability to package the artifact in an uber-jar
Group:          Development/Java
License:        ASL 2.0
URL:            https://maven.apache.org/plugins/%{name}
Source0:        https://github.com/apache/maven-shade-plugin/archive/refs/tags/maven-shade-plugin-%{version}.tar.gz
BuildArch:      noarch
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven

BuildRequires:  maven-plugins-pom
BuildRequires:  maven-components
BuildRequires:  mvn(org.ow2.asm:asm) >= 9
BuildRequires:  mvn(org.ow2.asm:asm-commons) >= 9
BuildRequires:  mvn(org.jdom:jdom2)
BuildRequires:  jdependency >= 2.17
BuildRequires:  plexus-utils >= 3.6.0

Obsoletes:      maven2-plugin-shade <= 0:2.0.8
Provides:       maven2-plugin-shade = 1:%{version}-%{release}

%description
This plugin provides the capability to package the artifact in an
uber-jar, including its dependencies and to shade - i.e. rename - the
packages of some of the dependencies.


%if %{with javadoc}
%package javadoc
Summary:        API documentation for %{name}

%endif
%if %{with javadoc}
%description javadoc
%{summary}.

%endif
%prep
%setup -q -n maven-shade-plugin-maven-shade-plugin-%{version}

%files -f .mfiles
%doc LICENSE README.md

%if %{with javadoc}
%files javadoc -f .mfiles-javadoc
%doc LICENSE README.md

%endif
