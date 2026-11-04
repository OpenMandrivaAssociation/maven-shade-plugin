%bcond_with javadoc
Name:           maven-shade-plugin
Version:        3.6.2
Release:        1
Summary:        This plugin provides the capability to package the artifact in an uber-jar
License:        ASL 2.0
URL:            https://maven.apache.org/plugins/%{name}
Source0:        https://github.com/apache/maven-shade-plugin/archive/refs/tags/maven-shade-plugin-%{version}.tar.gz
BuildArch:      noarch
BuildSystem:	maven

BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-commons)
BuildRequires:  mvn(org.jdom:jdom2)
BuildRequires:  mvn(org.vafer:jdependency)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

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
